"""RSS 订阅源生成器。

用途：满足「提醒/订阅」需求。将采集到的实习信息生成标准 RSS 2.0 订阅源，
用户可通过任意 RSS 阅读器订阅，从而在新岗位发布时收到更新提醒（无需用户系统/邮件服务）。

生成内容遵循「索引层 + 深链」原则：每条只含结构化元信息，link 指向投递渠道。
输出路径由 run.py 调配。
"""
from __future__ import annotations

import html
from datetime import datetime, timezone
from typing import Any

SITE_TITLE = "大厂实习信息聚合"
SITE_LINK = "https://example.internship-hub"  # 上线后替换为实际域名
SITE_DESC = "汇聚各大互联网/科技公司实习机会，一键直达官方投递渠道，每日更新。"


def _rfc2822(value: str) -> str:
    """把 ISO8601 字符串转成 RFC 2822（RSS 需要）。"""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")


def generate_feed(dataset: dict[str, Any], limit: int = 50) -> str:
    """根据数据集生成 RSS 2.0 XML 字符串。"""
    items = dataset.get("items", [])[:limit]

    out: list[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<rss version="2.0">')
    out.append("  <channel>")
    out.append(f"    <title>{html.escape(SITE_TITLE)}</title>")
    out.append(f"    <link>{html.escape(SITE_LINK)}</link>")
    out.append(f"    <description>{html.escape(SITE_DESC)}</description>")
    out.append(
        f"    <lastBuildDate>{_rfc2822(dataset.get('generatedAt', ''))}</lastBuildDate>"
    )
    out.append(f"    <generator>internship-hub</generator>")
    out.append(f"    <ttl>60</ttl>")

    for item in items:
        title = f"{item.get('company', '')} · {item.get('title', '')}"
        desc = item.get("summary") or f"{item.get('category', '')} · {item.get('city', '')}"
        link = item.get("applyUrl", "") or item.get("sourceUrl", "") or SITE_LINK
        pub = _rfc2822(item.get("publishedAt", ""))
        out.append("    <item>")
        out.append(f"      <title>{html.escape(title)}</title>")
        out.append(f"      <link>{html.escape(link)}</link>")
        out.append(f"      <guid isPermaLink=\"false\">{html.escape(item.get('id', ''))}</guid>")
        out.append(f"      <pubDate>{pub}</pubDate>")
        out.append(f"      <description>{html.escape(desc)}</description>")
        out.append("    </item>")

    out.append("  </channel>")
    out.append("</rss>")
    return "\n".join(out)
