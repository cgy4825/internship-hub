"""collector 作为模块运行入口：`python -m collector`。"""
from .run import main

if __name__ == "__main__":
    raise SystemExit(main())
