"""应届生求职网（51job 旗下）数据源采集器。

数据来源：https://m.yingjiesheng.com/ （移动端 SSR 页，结构稳定、数据真实）。

说明：
- 移动端首页由服务端渲染，含结构化职位条目（每个职位一个 jobdetail 深链）。
- 本采集器抓取并解析这些条目，提取 title/salary/company/city/tags 等元信息，
  投递深链指向真实职位详情页（含投递入口）。
- 遵循「索引层 + 深链」原则：只提取结构化元信息，不搬运职位描述正文。

数据筛选（重要）：
- 仅保留**校招/实习**岗位：通过 tags 中含「在校生/应届生」判定；其余（社招）丢弃。
- 符合项目定位，也满足用户「只要校招/实习信息」的需求。
"""
from __future__ import annotations

import re
import urllib.request
from typing import Any

from ..base import BaseCollector, utc_now
from ..normalize import clean_text, make_id

#: 目标页面：移动端首页（SSR 含职位列表）
TARGET_URL = "https://m.yingjiesheng.com/"

#: 移动端 UA（服务端据此返回相应链路的数据）
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)

HEADERS = {
    "User-Agent": MOBILE_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

#: 用于判定「校招/实习」的标签（在校生/应届生）
CAMPUS_TAGS = ("在校生", "应届生", "在校生/应届生", "熟悉")

#: 默认取自单个页面的条数上限
MAX_ITEMS = 60


def _is_campus(tags: list[str]) -> bool:
    """根据 tags 判断是否为校招/实习岗位。"""
    for tag in tags:
        if any(k in tag for k in ("在校生", "应届生")):
            return True
    return False


def _extract_items(html: str) -> list[dict[str, Any]]:
    """从 SSR HTML 中解析职位条目（每条一个 jobdetail 深链）。"""
    items: list[dict[str, Any]] = []
    # 以 jobdetail 深链为一条记录的分隔
    records = re.split(r'(?=<a href="https://m\.yingjiesheng\.com/jobdetail/)', html)

    for record in records:
        if "jobdetail" not in record:
            continue

        jid = re.search(r'jobdetail/(\d+)', record)
        title = re.search(r'class="job-title[^"]*"[^>]*>([^<]+)', record)
        salary = re.search(r'class="job-salary[^"]*"[^>]*>([^<]+)', record)
        comp = re.search(r'class="company-title[^"]*"[^>]*>([^<]+)', record)
        addr = re.search(r'class="company-address[^"]*"[^>]*>([^<]+)', record)
        tags = re.findall(r'class="job-tag[^"]*"[^>]*>([^<]+)', record)

        title_text = clean_text(title.group(1)) if title else ""
        if not title_text or not jid:
            continue

        appended = {
            "jobId": jid.group(1),
            "title": title_text,
            "salary": clean_text(salary.group(1)) if salary else "",
            "company": clean_text(comp.group(1)) if comp else "",
            "city": clean_text(addr.group(1)) if addr else "",
            "tags": [clean_text(t) for t in tags if clean_text(t)],
        }
        items.append(appended)

    return items


class YingjieShengCollector(BaseCollector):
    name = "yingjiesheng"

    def collect(self) -> list[dict[str, Any]]:
        html = self._fetch()
        raw_items = _extract_items(html)
        return self._to_schema(raw_items)

    def _fetch(self) -> str:
        req = urllib.request.Request(TARGET_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
        return raw.decode("utf-8", errors="ignore")

    def _to_schema(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """归一化为 schema 条目；仅保留校招/实习。"""
        collected = utc_now()
        out: list[dict[str, Any]] = []

        for item in raw_items[:MAX_ITEMS]:
            tags = item["tags"]
            if not _is_campus(tags):
                # 只保留校招/实习，跳过社招
                continue

            job_id = item["jobId"]
            city = item["city"] or "全国"
            # 学历从 tags 中提取（tags 第二项通常是学历）
            education = ""
            for tag in tags:
                if "本科" in tag or "硕士" in tag or "博士" in tag or "大专" in tag:
                    education = tag
                    break

            out.append(
                {
                    "id": make_id(self.name, job_id),
                    "company": item["company"],
                    "companyEn": "",
                    "title": item["title"],
                    "city": city,
                    "type": "campus",  # 校招/实习
                    "category": "其他",
                    "tags": [t for t in tags if not any(k in t for k in ("在校生", "应届生", "本科", "硕士", "博士", "大专"))][:5],
                    "summary": f"{item['salary']} {'· ' + education if education else ''}",
                    "applyUrl": f"https://m.yingjiesheng.com/jobdetail/{job_id}",
                    "sourceUrl": f"https://m.yingjiesheng.com/jobdetail/{job_id}",
                    "source": self.name,
                    "publishedAt": collected,
                    "collectedAt": collected,
                    "isActive": True,
                }
            )

        return out


yingjiesheng_collector = YingjieShengCollector()
