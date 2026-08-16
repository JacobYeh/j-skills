#!/usr/bin/env python3
"""check_missing_weeks.py — 检测 j-plan history-index.md 缺失的周报, 推到飞书.

每次跑:
  1. 解析 history-index.md 的周计划表
  2. 找出状态为 占位/待补 的周 (近 8 周窗口)
  3. 推一条 phc 提醒到飞书群

用法 (cron 每日):
  0 22 * * *  python3 /home/ubuntu/projects/j-skills/j-plan/check_missing_weeks.py
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

J_PLAN_DIR = Path.home() / "projects" / "j-skills" / "j-plan"
HISTORY = J_PLAN_DIR / "history-index.md"


def load_history():
    """读 history-index.md, 返近 8 周表 (周号, 日期, 主题, 状态)."""
    if not HISTORY.exists():
        return []
    lines = HISTORY.read_text(encoding="utf-8").split("\n")
    weeks = []
    in_weekly = False
    for line in lines:
        if line.startswith("| Week") and "Date" in line:
            in_weekly = True
            continue
        if in_weekly and line.startswith("|------"):
            continue
        if in_weekly and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4 and parts[0].startswith("W") and parts[0][1:].isdigit():
                weeks.append({
                    "week": parts[0],
                    "date_range": parts[1],
                    "topic": parts[2],
                    "status": parts[3],
                })
        elif in_weekly and line.startswith("##"):
            # 进入下一节 (如关键转折点)
            break
    return weeks


def find_missing(weeks: list) -> list:
    """状态含'占位'/'待补'/'缺'/'当前周' 的视为缺失."""
    bad_keywords = ("占位", "待补", "缺", "_当前")
    missing = []
    for w in weeks:
        if any(kw in w["status"] for kw in bad_keywords):
            missing.append(w)
    return missing


def build_alert(missing: list) -> str:
    today = date.today().isoformat()
    if not missing:
        return None
    lines = [f"⚠️ j-plan 周报缺失提醒 ({today})"]
    lines.append(f"近 8 周窗口有 {len(missing)} 周未完成:")
    for w in missing:
        lines.append(f"  • {w['week']} ({w['date_range']}) — {w['status']}")
    lines.append("\n请手动补录: 编辑 planning.md + 更新 history-index.md")
    lines.append("或运行: jp --text '<周内容>' 推一次 push 提醒")
    return "\n".join(lines)


def main():
    weeks = load_history()
    missing = find_missing(weeks)
    if not missing:
        print(f"✅ j-plan 周报完整 (近 8 周窗口)")
        return 0

    alert = build_alert(missing)
    print(alert)

    # 推送到飞书 (HIGH 优先级)
    try:
        import os
        push_hub = Path.home() / "projects" / "push-hub" / "scripts"
        if str(push_hub) not in sys.path:
            sys.path.insert(0, str(push_hub))
        from loader import push, Priority
        push(alert, priority=Priority.HIGH, source="j-plan")
        print(f"\n✅ 已推送到飞书 (priority HIGH)")
    except Exception as e:
        print(f"\n⚠️ 推送失败: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())