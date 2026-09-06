/**
 * 排序工具纯函数。
 */
import type { InternshipItem } from '../types/internship'
import { parseDate } from './date'

/** 薪资文本 → 元/年 的估算数值，用于排序。解析失败返回 -1（排最后）。 */
export function parseSalary(value: string | undefined): number {
  if (!value) return -1

  // 逐个数字 + 紧随单位 折算为元，再取区间中值（正确处理 "8千-1万" 等混合单位）
  const nums: number[] = []
  const re = /(\d+(?:\.\d+)?)(万|千|w|k)?/g
  let m: RegExpExecArray | null
  while ((m = re.exec(value)) !== null) {
    const n = parseFloat(m[1])
    const unit = m[2]
    if (unit === '万' || unit === 'w') nums.push(n * 10000)
    else if (unit === '千' || unit === 'k') nums.push(n * 1000)
    else nums.push(n)
  }
  if (nums.length === 0) return -1

  let annual: number
  if (value.includes('/年')) {
    // 已是年薪
    annual = nums.length > 1 ? (nums[0] + nums[nums.length - 1]) / 2 : nums[0]
  } else if (value.includes('/天')) {
    // 日薪 → 年（22 天/月 × 12 月）
    const daily = nums.length > 1 ? (nums[0] + nums[nums.length - 1]) / 2 : nums[0]
    annual = daily * 22 * 12
  } else {
    // 月薪 → 年
    const monthly = nums.length > 1 ? (nums[0] + nums[nums.length - 1]) / 2 : nums[0]
    annual = monthly * 12
  }

  return annual
}

/** 学历 → 排序权重（博士最高） */
const EDUCATION_RANK: Record<string, number> = {
  '博士': 5,
  '硕士': 4,
  '本科': 3,
  '大专': 2,
  '高中': 1,
}

export function educationRank(value: string | undefined): number {
  if (!value) return 0
  for (const [k, v] of Object.entries(EDUCATION_RANK)) {
    if (value.includes(k)) return v
  }
  return 0
}

export type SortKey = 'latest' | 'oldest' | 'salary_desc' | 'salary_asc' | 'education'

export const SORT_OPTIONS: Array<{ value: SortKey; label: string }> = [
  { value: 'latest', label: '最新发布' },
  { value: 'oldest', label: '最早发布' },
  { value: 'salary_desc', label: '薪资从高到低' },
  { value: 'salary_asc', label: '薪资从低到高' },
  { value: 'education', label: '学历从高到低' },
]

/** 按给定排序键返回新数组 */
export function sortInternships(items: InternshipItem[], key: SortKey): InternshipItem[] {
  const arr = [...items]
  switch (key) {
    case 'latest':
      return arr.sort((a, b) => (parseDate(b.publishedAt)?.getTime() ?? 0) - (parseDate(a.publishedAt)?.getTime() ?? 0))
    case 'oldest':
      return arr.sort((a, b) => (parseDate(a.publishedAt)?.getTime() ?? 0) - (parseDate(b.publishedAt)?.getTime() ?? 0))
    case 'salary_desc':
      return arr.sort((a, b) => parseSalary(b.summary) - parseSalary(a.summary))
    case 'salary_asc':
      return arr.sort((a, b) => parseSalary(a.summary) - parseSalary(b.summary))
    case 'education':
      return arr.sort((a, b) => educationRank(b.education) - educationRank(a.education))
    default:
      return arr
  }
}
