"""字段归一化工具。

将不同来源的原始字段统一为 schema（docs/data/schema.md）规定的标准字段。
多数公司名、城市、类型需要在采集后做清洗与归类。
"""
from __future__ import annotations

import hashlib
import re
from typing import Any


def clean_text(value: Any) -> str:
    """去除首尾空白与多余空白字符，转为字符串。"""
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_id(source: str, source_id: str) -> str:
    """生成全局唯一 id：``<source>_<hash>``，保证可回填。"""
    digest = hashlib.sha1(str(source_id).encode("utf-8")).hexdigest()[:10]
    return f"{source}_{digest}"


# 常见公司名 → 中文名 映射（可扩展）
_COMPANY_ALIAS: dict[str, str] = {
    "字节跳动": "字节跳动",
    "bytedance": "字节跳动",
    "腾讯": "腾讯",
    "tencent": "腾讯",
    "阿里巴巴": "阿里巴巴",
    "alibaba": "阿里巴巴",
    "美团": "美团",
    "meituan": "美团",
    "百度": "百度",
    "baidu": "百度",
    "京东": "京东",
    "jd": "京东",
}


def normalize_company(value: Any, company_en: Any = None) -> str:
    """归一化公司中文名。优先命中别名表，否则用原始值。"""
    cleaned = clean_text(value)
    for key, zh in _COMPANY_ALIAS.items():
        if key.lower() in cleaned.lower():
            return zh
    if company_en and clean_text(company_en).lower() in _COMPANY_ALIAS:
        return _COMPANY_ALIAS[clean_text(company_en).lower()]
    return cleaned


def normalize_city(value: Any) -> str:
    """归一化城市（去掉括号备注等，保留主城市名）。"""
    cleaned = clean_text(value)
    # 去掉「北京·海淀」中的后缀，取第一个字段
    if "·" in cleaned:
        return cleaned.split("·")[0].strip()
    return cleaned


def normalize_category(value: Any) -> str:
    """归一化岗位方向分类。将常见词映射到 schema 建议分类。

    映射表可扩展；无法判断时回退为 value（或“其他”）。
    """
    text = clean_text(value).lower()
    mapping = {
        "技术": "技术",
        "后端": "技术",
        "前端": "技术",
        "算法": "技术",
        "开发": "技术",
        "客户端": "技术",
        "产品": "产品",
        "运营": "运营",
        "设计": "设计",
        "ui": "设计",
        "市场": "市场",
        "数据": "数据",
        "数据分析": "数据",
        "职能": "职能",
        "hr": "职能",
    }
    for key, category in mapping.items():
        if key in text:
            return category
    return clean_text(value) or "其他"
