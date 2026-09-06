"""yingjiesheng 采集器解析逻辑单元测试。

测试对象是纯函数（HTML/字符串 → 数据），不发起真实网络请求，
保证「网站改版导致解析失效」这类最大风险能被测试尽早捕获。
"""
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 确保能以包方式导入
PACKAGE_ROOT = Path(__file__).resolve().parents[2]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from collector.sources.yingjiesheng import (  # noqa: E402
    _is_campus,
    _parse_pubdate,
    _extract_items,
)


def test_is_campus():
    """tags 含在校生/应届生视为校招/实习。"""
    assert _is_campus(["在校生/应届生", "本科"]) is True
    assert _is_campus(["在校生", "硕士"]) is True
    assert _is_campus(["应届生"]) is True
    assert _is_campus(["1年及以上", "本科"]) is False
    assert _is_campus([]) is False


def test_parse_pubdate_full_year():
    """完整年份格式：2026-09-03发布"""
    assert _parse_pubdate("2026-09-03发布") == "2026-09-03"


def test_parse_pubdate_month_day():
    """无年份 MM-DD 发布，用当前年推断。"""
    import datetime
    now = datetime.datetime.now()
    assert _parse_pubdate("09-03发布") == f"{now.year}-09-03"


def test_parse_pubdate_within_days():
    """X 天内发布 → 用当天推算近似日期。"""
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    approx = now - datetime.timedelta(days=3)
    assert _parse_pubdate("3天内发布") == f"{approx.year:04d}-{approx.month:02d}-{approx.day:02d}"


def test_parse_pubdate_empty():
    """空/无法解析 → None（前端不显示今日新增）。"""
    assert _parse_pubdate("") is None
    assert _parse_pubdate("随便一些文字") is None
    assert _parse_pubdate("") is None


def test_extract_items():
    """从职位卡片 HTML 片段解析出 title/salary/company/city/tags。"""
    sample = (
        '<a href="https://m.yingjiesheng.com/jobdetail/173231805?property=x">'
        '<span class="job-title ellipsis">物流培训生（青岛）MJ000298</span>'
        '<span class="job-salary">8千-1万</span>'
        '<span class="job-tag">在校生/应届生</span>'
        '<span class="job-tag">本科</span>'
        '<span class="company-title ellipsis">日邮物流（中国）</span>'
        '<span class="company-address ellipsis">青岛</span>'
        '</a>'
        '<a href="https://m.yingjiesheng.com/jobdetail/173508904?property=x">'
        '<span class="job-title ellipsis">系统设计岗</span>'
        '<span class="job-salary">2.9-3.5万</span>'
        '<span class="job-tag">在校生/应届生</span>'
        '<span class="job-tag">博士</span>'
        '<span class="company-title ellipsis">前锦网络信息技术（上海）</span>'
        '<span class="company-address ellipsis">贵阳</span>'
        '</a>'
    )
    items = _extract_items(sample)
    assert len(items) == 2
    assert items[0]["title"] == "物流培训生（青岛）MJ000298"
    assert items[0]["company"] == "日邮物流（中国）"
    assert items[0]["city"] == "青岛"
    assert items[0]["jobId"] == "173231805"
    assert items[1]["jobId"] == "173508904"


def test_extract_items_empty():
    """无职位条目 → 空列表。"""
    assert _extract_items("<html><body>无内容</body></html>") == []


def _run_all():
    """运行所有测试并返回是否全部通过。"""
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL  {t.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  ERROR {t.__name__}: {exc}")
    total = len(tests)
    print(f"\n{total - failures}/{total} 通过")
    return failures == 0


if __name__ == "__main__":
    sys.exit(0 if _run_all() else 1)
