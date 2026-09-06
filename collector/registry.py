"""数据源注册表（可插拔）。

新增数据源后在此登记，run.py 会遍历注册表运行所有源。
"""
from __future__ import annotations

from .base import BaseCollector
from .sources import nowcoder_collector, seed_collector, yingjiesheng_collector

#: 已注册的采集器列表，顺序即运行顺序。
#: 说明：
#: - yingjiesheng 是稳定可靠的真实校招/实习源（当前主力）。
#: - nowcoder / seed 已停用：nowcoder 讨论区噪声大且不稳定、seed 为演示占位。
#:   保留 import 以便回退（取消注释即可重新启用）。
COLLECTORS: list[BaseCollector] = [
    yingjiesheng_collector,
    # nowcoder_collector,
    # seed_collector,
]


def get_collectors() -> list[BaseCollector]:
    """返回所有已注册采集器。"""
    return COLLECTORS
