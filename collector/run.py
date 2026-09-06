"""采集器可执行入口。

运行方式（在项目根目录或 collector 目录下）：

    python collector/run.py

流程：注册表所有源 -> collect -> 合并去重 -> 归一化 -> 校验 -> 写 data/internships.json
单个源失败不影响其他源（容错原则，见 docs/architecture/collector.md）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# 将项目根目录加入 sys.path，使 collector 可作为包导入（兼容脚本方式运行）
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from collector.base import utc_now  # noqa: E402
from collector.normalize import (  # noqa: E402
    clean_text,
    normalize_category,
    normalize_city,
    normalize_company,
)
from collector.registry import get_collectors  # noqa: E402
from collector.rss import generate_feed  # noqa: E402
from collector.validate import check_unique_ids, validate_items  # noqa: E402

#: schema 版本，需与 docs/data/schema.md 及前端 types 一致
SCHEMA_VERSION = "1.0.0"


def build_dataset() -> dict:
    """运行所有采集器，合并、去重、归一化，返回完整数据集 dict。"""
    collected = utc_now()
    merged: list[dict] = []
    used_sources: list[str] = []
    # 记录每个来源的抓取数量，用于「空源告警」
    source_counts: dict[str, int] = {}

    for collector in get_collectors():
        try:
            raw_items = collector.collect()
            count = len(raw_items)
            print(f"[collect] {collector.name}: 抓到 {count} 条")
        except Exception as exc:  # noqa: BLE001
            if not collector.tolerant:
                raise
            print(f"[collect] {collector.name}: 失败，已跳过 ({exc})")
            continue

        used_sources.append(collector.name)
        source_counts[collector.name] = count
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            # 归一化关键字段（容错地在各源基础上再统一一次口径）
            item["company"] = normalize_company(item.get("company"), item.get("companyEn"))
            item["city"] = normalize_city(item.get("city"))
            item["category"] = normalize_category(item.get("category"))
            item["title"] = clean_text(item.get("title"))
            item["isActive"] = bool(item.get("isActive", True))
            merged.append(item)

    # 按 id 去重（保留首次出现）
    seen: set[str] = set()
    deduped: list[dict] = []
    for item in merged:
        id_ = str(item.get("id", ""))
        if not id_ or id_ in seen:
            continue
        seen.add(id_)
        deduped.append(item)

    # 校验
    valid = validate_items(deduped)
    dups = check_unique_ids(valid)
    if dups:
        print(f"[validate] 警告：存在重复 id {len(dups)} 个，已保留首个。")

    # 空源告警：若主采集源抓到 0 条（可能网站改版/解析失效），在输出中标记，
    # 供 CI 工作流检测并告警，避免"静默失效"。
    empty_sources = [name for name, cnt in source_counts.items() if cnt == 0]
    if empty_sources:
        print(f"[alert] 警告：数据源抓取到 0 条（可能解析失效）：{', '.join(empty_sources)}")
    elif not valid:
        print("[alert] 警告：本次采集未产出任何有效岗位，请检查采集器是否失效。")

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": collected,
        "sources": used_sources,
        "items": valid,
        "stats": {
            "sourceCounts": source_counts,
            "total": len(valid),
            "emptySources": empty_sources,
            "alert": bool(empty_sources) or not valid,
        },
    }


def write_json(dataset: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"[output] 已写入 {path}（{len(dataset['items'])} 条）")


def write_rss(dataset: dict, path: Path) -> None:
    """生成并写入 RSS 订阅源。"""
    xml = generate_feed(dataset)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(xml)
    print(f"[rss] 已写入 {path}")


def main() -> int:
    dataset = build_dataset()

    # 1) 主产物：项目根 data/internships.json（单一事实来源 / 数据版本管理）
    write_json(dataset, ROOT / "data" / "internships.json")

    # 2) 同步到前端可服务路径 web/public/data/internships.json
    #    使静态站点（fetch /data/internships.json）能读取到采集产物
    write_json(dataset, ROOT / "web" / "public" / "data" / "internships.json")

    # 3) 生成 RSS 订阅源（提醒功能），同步到前端可服务路径
    write_rss(dataset, ROOT / "data" / "feed.xml")
    write_rss(dataset, ROOT / "web" / "public" / "feed.xml")

    # 4) 空源/无数据告警：以非零退出码标记，供 CI 检测（collect-daily.yml）
    stats = dataset.get("stats", {})
    if stats.get("alert"):
        print("[alert] 本次采集异常，退出码记为 1（供 CI 告警检测）。")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
