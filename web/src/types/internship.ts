/**
 * 实习信息数据模型
 * 与 docs/data/schema.md 保持一致。本文件是前端类型的权威定义。
 */

export type InternshipType = 'internship' | 'campus' | 'other'

export type DataSource =
  | 'nowcoder'
  | 'company_website'
  | string

/** 单个实习岗位（对应 schema 的 InternshipItem） */
export interface InternshipItem {
  id: string
  company: string
  companyEn?: string
  title: string
  city: string
  type: InternshipType
  category: string
  tags?: string[]
  summary?: string
  /** 学历要求（如 本科/硕士/博士/大专） */
  education?: string
  /** 实习周期/时长（如 `5天/周·3个月`） */
  workDuration?: string
  /** 公司类型/规模/行业（如 `民营·1000-5000人·制药/生物工程`） */
  companyType?: string
  applyUrl: string
  sourceUrl?: string
  source: DataSource
  publishedAt: string // ISO8601（含时区）
  collectedAt: string // UTC
  isActive: boolean
  /** 可选：公司 logo 标识（用于前端展示，如首字母或自定义 key） */
  logoKey?: string
}

/** 顶层数据结构（对应 schema 顶层对象） */
export interface InternshipDataset {
  schemaVersion: string
  generatedAt: string
  sources: DataSource[]
  items: InternshipItem[]
}

/** 常用岗位方向分类（用于筛选，需与 schema 建议分类一致） */
export const CATEGORIES = [
  '技术',
  '产品',
  '运营',
  '设计',
  '市场',
  '数据',
  '职能',
  '其他',
] as const

/** 岗位类型中文名映射 */
export const TYPE_LABEL: Record<InternshipType, string> = {
  internship: '实习',
  campus: '校招',
  other: '其他',
}
