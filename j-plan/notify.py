#!/usr/bin/env python3
"""j-plan notify — 走 push-hub

详细逻辑见 `_shared/notify_base.py`. 本文件只声明 SOURCE.
"""
import sys
from pathlib import Path

# 让 _shared 能被 import (无 __init__.py 也能用)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _shared.notify_base import run_with_source  # noqa: E402

SOURCE = "j-plan"


if __name__ == "__main__":
    sys.exit(run_with_source(source=SOURCE))