"""应届生求职网（51job 旗下）数据源采集器。

数据来源：
- 移动端首页 https://m.yingjiesheng.com/ （SSR 推荐流）
- 多个分类关键词搜索页 https://m.yingjiesheng.com/searchresult/k<关键词>

说明：
- 移动端页面由服务端渲染，含结构化职位条目（每个职位一个 jobdetail 深链）。
- 本采集器抓取多个页面并**合并、按 jobid 去重**，稳定扩充数据量。
- 提取 title/salary/company/city/tags 等元信息，投递深链指向真实职位详情页（含投递入口）。
- 遵循「索引层 + 深链」原则：只提取结构化元信息，不搬运职位描述正文。

数据筛选（重要）：
- 仅保留**校招/实习**岗位：通过 tags 中含「在校生/应届生」判定；其余（社招）丢弃。
- 符合项目定位，也满足用户「只要校招/实习信息」的需求。
"""
from __future__ import annotations

import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any

from ..base import BaseCollector, utc_now
from ..normalize import clean_text, make_id

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

#: 目标页面：移动端首页（SSR 推荐流）
HOME_URL = "https://m.yingjiesheng.com/"

#: 职位详情页前缀（用于抓取真实发布日期）
DETAIL_URL_PREFIX = "https://m.yingjiesheng.com/jobdetail/"

#: 分类关键词搜索页（各返回一页，合并后扩充数据量）
SEARCH_KEYWORDS = ["实习", "校招", "校园招聘", "管培生", "应届生"]

#: 单个搜索页最大抓取条数
MAX_PER_PAGE = 60

#: 总条数上限（防止一次抓太多）
MAX_TOTAL = 120

#: 是否抓取职位详情页以获取真实发布日期（若关闭，publishedAt 留空，前端不显示"今日新增"）
FETCH_DETAIL_PUBDATE = True

#: 详情页请求之间的最小间隔（秒），降低反爬风险
DETAIL_DELAY_SECONDS = 0.5


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
        comp_type = re.search(r'class="company-type[^"]*"[^>]*>([^<]+)', record)
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
            "companyType": clean_text(comp_type.group(1)) if comp_type else "",
            "tags": [clean_text(t) for t in tags if clean_text(t)],
        }
        items.append(appended)

    return items


def _parse_pubdate(text: str) -> str | None:
    """从详情页 jobInfo-update 文本中解析发布时间。

    支持格式：
    - `2026-09-03发布`  / `2026/9/3发布`
    - `09-03发布`（无年份，用当前年推断）
    - `30天内发布`（用当天 - N 天计算近似日期）

    解析失败返回 None（表示发布日未知，前端据此不显示"今日新增"）。
    """
    text = clean_text(text)
    if not text:
        return None

    now = datetime.now(timezone.utc)

    # 1) 含完整年份的日期
    m = re.search(r'(20\d{2})[-/](\d{1,2})[-/](\d{1,2})发布', text)
    if m:
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    # 2) 无年份的 MM-DD发布（用当前年）
    m = re.search(r'[-/]?(\d{1,2})[-/](\d{1,2})发布', text)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        return f"{now.year:04d}-{month:02d}-{day:02d}"

    # 3) X天内发布（用当天推算近似日期）
    m = re.search(r'(\d+)\s*天内发布', text)
    if m:
        days = int(m.group(1))
        approx = now - timedelta(days=days)
        return f"{approx.year:04d}-{approx.month:02d}-{approx.day:02d}"

    return None


def _extract_pubdate_from_detail(html: str) -> str | None:
    """从详情页 HTML 提取 jobInfo-update 元素的发布时间。"""
    m = re.search(r'class="jobInfo-update[^"]*"[^>]*>([^<]+)', html)
    if not m:
        return None
    return _parse_pubdate(m.group(1))


class YingjieShengCollector(BaseCollector):
    name = "yingjiesheng"

    def collect(self) -> list[dict[str, Any]]:
        # 1) 首页推荐流
        raw_items: list[dict[str, Any]] = []
        try:
            home_html = self._fetch(HOME_URL)
            raw_items.extend(_extract_items(home_html))
        except Exception as exc:  # noqa: BLE001
            print(f"[yingjiesheng] 首页抓取失败，跳过 ({exc})")

        # 2) 多个分类关键词搜索页
        for kw in SEARCH_KEYWORDS:
            url = "https://m.yingjiesheng.com/searchresult/k" + urllib.parse.quote(kw)
            try:
                html = self._fetch(url)
                raw_items.extend(_extract_items(html))
            except Exception as exc:  # noqa: BLE001
                print(f"[yingjiesheng] 关键词「{kw}」抓取失败，跳过 ({exc})")

        # 3) 按 jobId 去重（保留首次出现）
        seen: set[str] = set()
        deduped: list[dict[str, Any]] = []
        for item in raw_items:
            jid = item["jobId"]
            if jid in seen:
                continue
            seen.add(jid)
            deduped.append(item)

        return self._to_schema(deduped)

    def _fetch(self, url: str) -> str:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
        return raw.decode("utf-8", errors="ignore")

    def _to_schema(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """归一化为 schema 条目；仅保留校招/实习。"""
        collected = utc_now()
        out: list[dict[str, Any]] = []

        for item in raw_items[:MAX_TOTAL]:
            tags = item["tags"]
            if not _is_campus(tags):
                # 只保留校招/实习，跳过社招
                continue

            job_id = item["jobId"]
            city = item["city"] or "全国"
            # 从 tags 中提取学历与实习时长
            education = ""
            work_duration = ""
            for tag in tags:
                if not education and ("本科" in tag or "硕士" in tag or "博士" in tag or "大专" in tag):
                    education = tag
                if not work_duration and re.search(r'\d+天/\s*周', tag):
                    work_duration = tag

            # 公司类型/规模/行业（列表页字段）
            company_type = clean_text(item.get("companyType", ""))

            # 发布日期：优先抓详情页真实发布日，抓不到则留空（前端不显示"今日新增"）
            published_at = ""
            if FETCH_DETAIL_PUBDATE:
                try:
                    pub_html = self._fetch(f"{DETAIL_URL_PREFIX}{job_id}")
                    pub = _extract_pubdate_from_detail(pub_html)
                    if pub:
                        published_at = pub
                except Exception as exc:  # noqa: BLE001
                    print(f"[yingjiesheng] 职位 {job_id} 详情页解析失败 ({exc})")
                # 控制请求频率，降低反爬风险
                if DETAIL_DELAY_SECONDS:
                    import time

                    time.sleep(DETAIL_DELAY_SECONDS)

            # 摘要保留薪资；学历单独作为 education 字段展示
            summary = item["salary"]
            if education:
                summary = f"{summary} · {education}"

            out.append(
                {
                    "id": make_id(self.name, job_id),
                    "company": item["company"],
                    "companyEn": "",
                    "title": item["title"],
                    "city": city,
                    "type": "campus",  # 校招/实习
                    "category": "其他",
                    "tags": [t for t in tags if not any(k in t for k in ("在校生", "应届生", "本科", "硕士", "博士", "大专")) and not re.search(r'\d+天/\s*周', t)][:5],
                    "summary": summary,
                    "education": education,
                    "workDuration": work_duration,
                    "companyType": company_type,
                    "applyUrl": f"https://m.yingjiesheng.com/jobdetail/{job_id}",
                    "sourceUrl": f"https://m.yingjiesheng.com/jobdetail/{job_id}",
                    "source": self.name,
                    "publishedAt": published_at,
                    "collectedAt": collected,
                    "isActive": True,
                }
            )

        return out


yingjiesheng_collector = YingjieShengCollector()
