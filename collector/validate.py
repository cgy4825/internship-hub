"""schema 校验。

负责校验采集后的数据是否符合 docs/data/schema.md 定义的字段要求。
非法数据拒绝产出，保证前端不会拿到残缺/错误的记录。
"""
from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = [
    "id",
    "company",
    "title",
    "city",
    "type",
    "category",
    "applyUrl",
    "source",
    "publishedAt",
    "collectedAt",
    "isActive",
]

VALID_TYPES = {"internship", "campus", "other"}


class SchemaValidationError(Exception):
    """数据不符合 schema 时抛出。"""


def validate_item(item: dict[str, Any]) -> list[str]:
    """校验单条记录，返回错误列表（空即通过）。"""
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in item or item[field] in (None, ""):
            errors.append(f"缺少必填字段: {field}")

    if "type" in item and item["type"] not in VALID_TYPES:
        errors.append(f"type 取值非法: {item['type']}")

    if "applyUrl" in item and item["applyUrl"]:
        url = str(item["applyUrl"])
        if not (url.startswith("http://") or url.startswith("https://")):
            errors.append("applyUrl 必须为 http(s) 链接")

    if "id" in item and not str(item["id"]).startswith("nowcoder_") and not str(item["id"]).startswith("company_website_"):
        # id 前缀约定校验（可扩展，避免直接硬编码源）
        pass

    return errors


def validate_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """校验整批数据，返回通过校验的记录（不合法记录被剔除并记录日志）。"""
    valid: list[dict[str, Any]] = []
    for idx, item in enumerate(items):
        errors = validate_item(item)
        if errors:
            print(f"[validate] 第 #{idx} 条记录不通过: {errors}")
            continue
        valid.append(item)
    return valid


def check_unique_ids(items: list[dict[str, Any]]) -> list[str]:
    """检测重复 id，返回重复的 id 列表。"""
    seen: set[str] = set()
    duplicates: list[str] = []
    for item in items:
        id_ = str(item["id"])
        if id_ in seen:
            duplicates.append(id_)
        seen.add(id_)
    return duplicates
