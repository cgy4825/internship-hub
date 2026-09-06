"""数据源注册表（可插拔）。

新增数据源后在此登记，run.py 会遍历注册表运行所有源。
"""
from __future__ import annotations

from .base import BaseCollector
from .sources import nowcoder_collector, seed_collector

#: 已注册的采集器列表，顺序即运行顺序
COLLECTORS: list[BaseCollector] = [
    nowcoder_collector,
    seed_collector,
]


def get_collectors() -> list[BaseCollector]:
    """返回所有已注册采集器。"""
    return COLLECTORS
