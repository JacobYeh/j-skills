#!/usr/bin/env python3
"""j-work notify — 走 push-hub

详细逻辑见 `_shared/notify_base.py`. 本文件只声明 SOURCE.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _shared.notify_base import run_with_source  # noqa: E402

SOURCE = "j-work"


if __name__ == "__main__":
    sys.exit(run_with_source(source=SOURCE))