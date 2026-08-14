#!/usr/bin/env python3
"""notify_base.py — 3 个 j-skill 共享的 notify 逻辑

用法 (在每个 skill 的 notify.py 中):
    from _shared.notify_base import build_parser, run_with_source

    if __name__ == "__main__":
        run_with_source(SOURCE="j-plan")

或直接用 build_parser() + main() 自定义行为.
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path


def _load_push_hub():
    """用 importlib 加载 push-hub (避免跟 skill 的 scripts/ 冲突)."""
    ph_scripts = Path.home() / "projects" / "push-hub" / "scripts" / "__init__.py"
    if not ph_scripts.exists():
        raise ImportError("push-hub 不存在: " + str(ph_scripts))
    spec = importlib.util.spec_from_file_location("push_hub_scripts", ph_scripts)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["push_hub_scripts"] = mod
    spec.loader.exec_module(mod)
    return mod


def build_parser(description: str) -> argparse.ArgumentParser:
    """构造标准的 argparse (3 个 skill 通用)."""
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--text", help="文字内容")
    p.add_argument("--file", help="从文件读 (markdown)")
    p.add_argument("--title", help="卡片标题 (file 模式)")
    p.add_argument("--priority", default="normal",
                   choices=["critical", "high", "normal", "low"])
    p.add_argument("--dry-run", action="store_true", help="只 print, 不真发")
    return p


def run_with_source(source: str, description: str | None = None) -> int:
    """CLI 入口 — 加载 push-hub, parse args, 推送.

    Args:
        source: 来源标签 (j-plan / j-work / yijing-fengshui)
        description: argparse description (默认: "{source} 通知 (走 push-hub)")
    """
    if description is None:
        description = f"{source} 通知 (走 push-hub)"

    # 重要: 必须先 parse args, 这样 --dry-run 能在加载 push-hub 前设 env var.
    # push-hub 在 import 时读 DRY_RUN env, 加载顺序不能换.
    args = build_parser(description).parse_args()

    if args.dry_run:
        os.environ["Mavis_PUSH_DRY_RUN"] = "1"

    try:
        _ph = _load_push_hub()
        push = _ph.push
        push_card = _ph.push_card
        Priority = _ph.Priority
    except Exception as e:
        print("[WARN] push-hub 不可用: " + str(e))
        return 1

    pri = Priority[args.priority.upper()]

    if args.file:
        body = Path(args.file).read_text(encoding="utf-8")
        title = args.title or Path(args.file).name
        ok = push_card(title=title, body=body, priority=pri, source=source)
    elif args.text:
        ok = push(args.text, priority=pri, source=source)
    else:
        print("错误: --text 或 --file 必填")
        return 1

    return 0 if ok else 2