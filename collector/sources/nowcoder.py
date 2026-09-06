"""牛客网数据源采集器。

说明：
- 牛客网（nowcoder.com）是大厂实习/校招信息最集中的平台。
- 本采集器通过 HTTPS 抓取其公开页面，提取结构化元信息（索引层），
  剪裁出 title/company/city/type/category/applyUrl 等字段，点击深链到官方投递。
- 遵循「索引层 + 深链」原则：不搬运职位描述正文。

稳健性设计（重要）：
- 牛客 `/discuss` 是讨论区，混有大量「面经/笔试/面试体验」等非招聘内容。
  因此本解析器采用**保守过滤**：只保留看起来是「招聘/实习/校招」的条目，
  过滤明显是经验分享/闲聊的噪声，避免把非岗位信息灌进站点。
"""
from __future__ import annotations

import re
import urllib.request
from typing import Any

from ..base import BaseCollector, utc_now
from ..normalize import (
    clean_text,
    make_id,
    normalize_category,
)

#: 目标页面：牛客讨论/求职区
TARGET_URL = "https://www.nowcoder.com/discuss?type=2"

#: 请求头，模拟浏览器
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

#: 噪声关键词：命中任一即视为非招聘内容（经验分享、闲聊、考试等）
NOISE_KEYWORDS = [
    "面经", "笔经", "笔试", "面试经验", "面试感受", "面试体验", "一面", "二面", "三面",
    "吐槽", "求建议", "offer", "离职", "入职", "薪资", "背调", "简历", "春招",
    "秋招复盘", "很无语", "记录", "总结", "上岸", "转正", "校招倒计时",
    "遇到", "怎么办", "求助", "HR", "双非", "一本", "硕士", "实习转正",
]

#: 招聘特征启发：命中任一强特征才算「岗位/招聘」信息
JOB_HINTS = ["招聘", "实习", "校招", "社招", "岗位", "急招", "内推", "补录", "开启", "计划"]


def _is_job_post(title: str) -> bool:
    """判断是否为招聘/实习/校招类内容（保守策略）。"""
    low = title.lower()
    if any(n in low for n in NOISE_KEYWORDS):
        return False
    # 需命中强招聘特征
    if any(h in low for h in JOB_HINTS):
        return True
    return False


def _extract_company(title: str) -> str:
    """从标题中提取公司名（启发式）。

    常见大厂名 + 开头两个汉字（用于「某公司-xxx」风格）。
    """
    low = title.lower()
    known = [
        "字节跳动", "字节", "腾讯", "阿里巴巴", "阿里", "美团", "百度",
        "京东", "拼多多", "网易", "小红书", "哔哩哔哩", "b站", "快手",
        "滴滴", "华为", "小米", "蚂蚁", "得物", "bigo", "携程", "360",
    ]
    for k in known:
        if k in low:
            return {"b站": "哔哩哔哩", "字节": "字节跳动", "阿里": "阿里巴巴"}.get(k, k)
    # 兜底：取标题首个公司名片段（如「滴滴9.6笔试」→ 滴滴）
    m = re.match(r"^([\u4e00-\u9fa5]{2,6})", title)
    return m.group(1) if m else "未知公司"


class NowcoderCollector(BaseCollector):
    name = "nowcoder"

    def collect(self) -> list[dict[str, Any]]:
        html = self._fetch()
        return self._parse_page(html)

    def _fetch(self) -> str:
        req = urllib.request.Request(TARGET_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
        return raw.decode("utf-8", errors="ignore")

    def _parse_page(self, html: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        collected = utc_now()

        # 抓取链接 + 锚文本
        links = re.findall(r'href="(/discuss/\d+[^"]*)"[^>]*>(.*?)</a>', html, re.S)
        seen: set[str] = set()

        for href, text in links:
            title = clean_text(re.sub(r"<[^>]+>", "", text))
            if len(title) < 5:
                continue
            # 去掉常见前缀噪声
            title = re.sub(r"^【.*?】", "", title).strip()
            if len(title) < 5:
                continue

            if not _is_job_post(title):
                continue

            if href in seen:
                continue
            seen.add(href)

            company = _extract_company(title)
            items.append(
                {
                    "id": make_id(self.name, href),
                    "company": company,
                    "companyEn": "",
                    "title": title,
                    "city": "",  # 牛客讨论页未必含城市，置空由前端展示
                    "type": "internship" if ("实习" in title) else "campus",
                    "category": normalize_category(title),
                    "tags": [],
                    "summary": "",
                    "applyUrl": f"https://www.nowcoder.com{href}",
                    "sourceUrl": f"https://www.nowcoder.com{href}",
                    "source": self.name,
                    "publishedAt": collected,
                    "collectedAt": collected,
                    "isActive": True,
                }
            )

        return items


nowcoder_collector = NowcoderCollector()
