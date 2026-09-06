# 数据采集器架构

> 描述 `collector/` 数据采集端的设计。

## 1. 定位

采集器负责把分散在牛客网、各公司官方校招网站的实习信息，抓取、清洗、归一化为符合 `docs/data/schema.md` 的标准 JSON。

## 2. 设计原则

1. **可插拔数据源**：每个来源是独立模块，拥有统一接口，实现独立运行。
2. **索引层原则**：只提取标题、公司、城市、类型、摘要、日期、链接等结构化字段，不搬运职位描述正文，点击深链到官方渠道。
3. **容错**：单个来源失败不影响其他来源；失败需记录并可感知。
4. **schema 校验**：输出前校验必填字段与枚举，非法数据不产出。

## 3. 模块结构

```
collector/
├── base.py               # 采集器基类/抽象接口 + 公共工具
├── normalize.py          # 字段归一化（公司名、城市、类型、category 推断）
├── validate.py           # schema 校验
├── registry.py           # 数据源注册表（可插拔）
├── sources/
│   ├── nowcoder.py       # 牛客网采集器
│   ├── company_site.py   # 大厂官网采集器（可多个）
│   └── __init__.py       # 导出所有源
├── run.py                # 入口：运行所有源 → 产出 data/internships.json
└── requirements.txt
```

## 4. 采集器接口约定（建议）

每个源实现统一接口，例如：

```python
class BaseCollector:
    name: str  # 来源标识（对应 schema source 字段）

    def collect(self) -> list[dict]:
        """返回符合 schema 的 InternshipItem 列表"""
        raise NotImplementedError
```

`run.py` 读取 `registry.py` 中注册的源，逐个 `collect()`，合并 → `normalize` → `validate` → 写 `data/internships.json`，并附上顶层 `sources`、`generatedAt`。

## 5. 新增一个数据源

1. 在 `sources/` 新增 `xxx.py`，实现 `BaseCollector` 并导出 `collector` 实例。
2. 在 `registry.py` 登记。
3. 在 `docs/data/schema.md` 的 `source` 枚举登记来源标识。
4. 运行 `python collector/run.py` 验证输出符合 schema。

## 6. 合规与稳健

- 遵守「索引层 + 深链」原则，仅提取结构化元信息。
- 抓取时控制频率、加 UA、尊重 robots/平台条款；MVP 阶段以牛客网这类集中源为主。
- 对反爬、网站改版导致的失败做好捕获，记录并提示（后续可接入告警）。
