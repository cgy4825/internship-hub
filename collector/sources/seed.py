"""种子数据源：提供一份符合 schema 的示例数据。

用途：
- 作为流水线的兜底/演示数据源，保证任何时候站点都有内容可展示。
- 在真实采集源尚未连通或反爬时，站点不至于空白。

注意：真实上线应依赖 nowcoder/company_site 等真实源；seed 仅作兜底与演示。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from ..base import BaseCollector, utc_now
from ..normalize import make_id

# 时区：中国标准时间
_CST = timezone(timedelta(hours=8))


def _iso(dt: datetime) -> str:
    """转 ISO8601 含 +08:00 时区的字符串。"""
    return dt.isoformat()


class SeedCollector(BaseCollector):
    name = "seed"

    def collect(self) -> list[dict[str, Any]]:
        collected = utc_now()
        now = datetime.now(_CST)

        # (标题, 公司, 公司英, 城市, 类型, 分类, 标签, 摘要, 投递链接, 几天前发布)
        seeds = [
            (
                "后端开发实习生（推荐系统方向）", "字节跳动", "ByteDance", "北京",
                "internship", "技术", ["Go", "后端", "推荐系统"],
                "参与推荐系统服务端核心模块开发，与资深工程师并肩工作。",
                "https://jobs.bytedance.com/experienced/position/example-001", 0,
            ),
            (
                "前端开发实习生（微信生态）", "腾讯", "Tencent", "深圳",
                "internship", "技术", ["React", "前端", "微信"],
                "负责微信生态相关产品前端开发与体验优化。",
                "https://careers.tencent.com/jobdesc.html?postId=example-002", 0,
            ),
            (
                "算法工程师实习生（大模型方向）", "阿里巴巴", "Alibaba", "杭州",
                "internship", "技术", ["大模型", "算法", "Python"],
                "参与大模型训练与推理优化项目，探索前沿 AI 应用。",
                "https://talent.alibaba.com/off-campus/position-detail?lang=zh&positionId=example-003", 1,
            ),
            (
                "数据分析实习生", "美团", "Meituan", "北京",
                "internship", "数据", ["SQL", "数据分析", "Python"],
                "负责业务数据洞察与指标体系建设，支撑决策。",
                "https://zhaopin.meituan.com/web/position/detail?jobSequence=example-004", 1,
            ),
            (
                "产品经理实习生（B端）", "拼多多", "Pinduoduo", "上海",
                "internship", "产品", ["产品经理", "B端"],
                "参与供应链 B 端产品设计与需求分析。",
                "https://careers.pinduoduo.com/jobs/detail/example-005", 2,
            ),
            (
                "游戏客户端开发实习生", "网易", "NetEase", "杭州",
                "internship", "技术", ["Unity", "游戏", "客户端"],
                "参与自研游戏引擎客户端功能开发。",
                "https://game.163.com/recruitment/internship/detail/example-006", 3,
            ),
            (
                "运营实习生（电商增长）", "京东", "JD", "北京",
                "internship", "运营", ["运营", "增长"],
                "负责电商活动运营与用户增长策略落地。",
                "https://zhaopin.jd.com/web/job/internship/detail/example-007", 4,
            ),
            (
                "视觉算法实习生", "百度", "Baidu", "北京",
                "internship", "技术", ["CV", "算法", "深度学习"],
                "参与计算机视觉算法研究与落地。",
                "https://talent.baidu.com/jobs/detail/example-008", 5,
            ),
            (
                "UI 设计实习生", "小红书", "Xiaohongshu", "上海",
                "internship", "设计", ["UI", "设计"],
                "参与产品界面设计与视觉规范建设。",
                "https://job.xiaohongshu.com/jobs/detail/example-009", 6,
            ),
            (
                "市场品牌实习生", "哔哩哔哩", "Bilibili", "上海",
                "internship", "市场", ["市场", "品牌"],
                "参与品牌营销活动策划与执行。",
                "https://jobs.bilibili.com/social/position/detail/example-010", 7,
            ),
            (
                "数据分析实习生（商业化）", "快手", "Kuaishou", "北京",
                "internship", "数据", ["SQL", "指标", "商业化"],
                "负责商业化业务数据分析与策略支持。",
                "https://zhaopin.kuaishou.cn/recruit/e/#/jobDetail/example-011", 8,
            ),
            (
                "后端开发实习生（服务端）", "滴滴", "Didi", "北京",
                "internship", "技术", ["Java", "后端"],
                "参与出行服务端系统开发与稳定性建设。",
                "https://talent.didiglobal.com/jobs/detail/example-012", 9,
            ),
        ]

        items: list[dict[str, Any]] = []
        for idx, seed in enumerate(seeds):
            (
                title, company, company_en, city, type_, category, tags,
                summary, apply_url, days_ago,
            ) = seed
            published = (now - timedelta(days=days_ago)).isoformat()
            items.append(
                {
                    "id": make_id(self.name, title),
                    "company": company,
                    "companyEn": company_en,
                    "title": title,
                    "city": city,
                    "type": type_,
                    "category": category,
                    "tags": tags,
                    "summary": summary,
                    "applyUrl": apply_url,
                    "sourceUrl": "",
                    "source": self.name,
                    "publishedAt": published,
                    "collectedAt": collected,
                    "isActive": True,
                }
            )
        return items


seed_collector = SeedCollector()
