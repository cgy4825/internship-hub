# 实习信息数据模型（schema）

> 本文件是数据结构的**权威定义**。采集器产物与前端渲染都必须遵循本 schema。
> 变更字段必须同步更新此文件，并更新采集器与前端，三者保持一致。

## 1. 顶层对象

```json
{
  "schemaVersion": "1.0.0",
  "generatedAt": "2025-01-01T08:00:00Z",
  "sources": ["nowcoder", "company_website"],
  "items": [ /* InternshipItem[] */ ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schemaVersion` | string | 是 | schema 版本。当前 `"1.0.0"` |
| `generatedAt` | string (ISO8601) | 是 | 本批数据生成时间（UTC） |
| `sources` | string[] | 是 | 参与生成的数据源标识 |
| `items` | InternshipItem[] | 是 | 实习岗位列表 |

## 2. InternshipItem

```json
{
  "id": "nowcoder_20250101_001",
  "company": "字节跳动",
  "companyEn": "ByteDance",
  "title": "后端开发实习生",
  "city": "北京",
  "type": "internship",
  "category": "技术",
  "tags": ["go", "后端", "实习"],
  "summary": "负责 xx 业务后端服务开发。",
  "applyUrl": "https://jobs.bytedance.com/...",
  "sourceUrl": "https://www.nowcoder.com/...",
  "source": "nowcoder",
  "publishedAt": "2025-01-01T00:00:00+08:00",
  "collectedAt": "2025-01-01T08:00:00Z",
  "isActive": true
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 全局唯一 id。约定 `<source>_<sourceId>` |
| `company` | string | 是 | 公司中文名 |
| `companyEn` | string | 否 | 公司英文名 |
| `title` | string | 是 | 岗位名称 |
| `city` | string | 是 | 城市 |
| `type` | enum | 是 | 岗位类型：`internship` / `campus` / `other` |
| `category` | string | 是 | 岗位方向大类（技术/产品/运营/设计/市场/职能…） |
| `tags` | string[] | 否 | 标签，用于筛选与搜索 |
| `summary` | string | 否 | 一句话摘要（非正文，符合索引层原则） |
| `applyUrl` | string | 是 | 投递跳转链接（深链，指向官方渠道） |
| `sourceUrl` | string | 否 | 信息原始页面链接 |
| `source` | string | 是 | 来源标识，如 `nowcoder`、`company_website` |
| `publishedAt` | string | 否 | 发布日期。**来源能提供真实发布日时填写；否则留空**，此时前端不显示「今日新增」、不伪造时间 |
| `collectedAt` | string | 是 | 采集时间（UTC） |
| `isActive` | boolean | 是 | 是否仍有效（下架可置 false） |

## 3. 枚举取值

### type
- `internship` —— 实习
- `campus` —— 校招
- `other` —— 其他

### category（建议但可扩展）
`技术` / `产品` / `运营` / `设计` / `市场` / `数据` / `职能` / `其他`

### source
- `yingjiesheng` —— 应届生求职网（51job 旗下，校招/实习主要来源）
- `nowcoder` —— 牛客网（当前已停用：讨论区噪声大、接口不稳定）
- `company_website` —— 公司官方校招网站
- `seed` —— 演示数据（已停用：接入真实源后不再参与采集）
- 自定义：新增源需在 [`architecture/collector.md`](../architecture/collector.md) 登记。

## 4. 校验规则

- `items` 中每个元素必须满足上述「必填」字段齐全，且类型匹配。
- `id` 不得重复，否则视为采集器 bug。
- `applyUrl` 必须以 `http://` 或 `https://` 开头。
- 「今日新增」由前端基于 `publishedAt` 的本地时间逐日判定，不依赖后端。
