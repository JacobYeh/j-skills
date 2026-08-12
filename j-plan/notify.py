#!/usr/bin/env python3
"""
notify.py - j-plan 通知脚本 (用 push-hub)

用法:
    python3 notify.py --text "Hello"
    python3 notify.py --file report.md --title "周报"
    python3 notify.py --priority high --text "Important"

调 push-hub v0.1 (importlib 方式, 避免 scripts/ 冲突)
"""
import argparse
import importlib.util
import os
import sys
from pathlib import Path


def _load_push_hub():
    """用 importlib 加载 push-hub."""
    ph_scripts = Path.home() / "projects" / "push-hub" / "scripts" / "__init__.py"
    if not ph_scripts.exists():
        raise ImportError("push-hub 不存在: " + str(ph_scripts))
    spec = importlib.util.spec_from_file_location("push_hub_scripts", ph_scripts)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["push_hub_scripts"] = mod
    spec.loader.exec_module(mod)
    return mod


# 加载 push-hub
try:
    _ph = _load_push_hub()
    push = _ph.push
    push_card = _ph.push_card
    Priority = _ph.Priority
    DRY_RUN = _ph.DRY_RUN
    PUSH_HUB_AVAILABLE = True
except Exception as e:
    PUSH_HUB_AVAILABLE = False
    DRY_RUN = False
    Priority = None
    print("[WARN] push-hub 不可用: " + str(e))


SOURCE = "j-plan"


def main():
    p = argparse.ArgumentParser(description="j-plan 通知 (走 push-hub)")
    p.add_argument("--text", help="文字内容")
    p.add_argument("--file", help="从文件读 (markdown)")
    p.add_argument("--title", help="卡片标题 (file 模式)")
    p.add_argument("--priority", default="normal",
                   choices=["critical", "high", "normal", "low"])
    p.add_argument("--dry-run", action="store_true", help="只 print, 不真发")
    args = p.parse_args()

    if args.dry_run:
        os.environ["Mavis_PUSH_DRY_RUN"] = "1"
        try:
            mod = _load_push_hub()
            globals()["push"] = mod.push
            globals()["push_card"] = mod.push_card
            globals()["Priority"] = mod.Priority
            globals()["DRY_RUN"] = mod.DRY_RUN
        except Exception as e:
            print("[ERROR] 切 dry-run 失败: " + str(e))
            sys.exit(1)

    if not PUSH_HUB_AVAILABLE:
        print("[ERROR] push-hub 不可用, 没法推")
        sys.exit(1)

    pri = Priority[args.priority.upper()]

    if args.file:
        body = Path(args.file).read_text(encoding="utf-8")
        title = args.title or Path(args.file).name
        ok = push_card(title=title, body=body, priority=pri, source=SOURCE)
    elif args.text:
        ok = push(args.text, priority=pri, source=SOURCE)
    else:
        print("错误: --text 或 --file 必填")
        sys.exit(1)

    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
