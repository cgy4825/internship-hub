"""采集器接口与公共工具定义。

所有数据源采集器都必须继承 :class:`BaseCollector` 并实现 ``collect``。
这样保证采集端可插拔、可单测、可单独运行（见 docs/architecture/collector.md）。
"""
from __future__ import annotations

import abc
from datetime import datetime, timezone
from typing import Any


class BaseCollector(abc.ABC):
    """数据源采集器抽象基类。

    子类需设置 :attr:`name`（对应 schema 的 ``source`` 字段），
    并实现 :meth:`collect` 返回符合 schema 的维度字典列表。
    """

    #: 来源标识，对应数据 schema 的 source 字段
    name: str = "base"

    @abc.abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        """抓取并返回当前来源的实习信息列表（未归一化的原始 dict）。"""
        raise NotImplementedError

    #: 若单个来源失败，是否允许整个流程继续（默认允许，容错原则）
    tolerant: bool = True


def utc_now() -> str:
    """当前 UTC 时间，ISO8601，用于 collectedAt / generatedAt。"""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
