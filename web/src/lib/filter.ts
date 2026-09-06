/**
 * 通用数据过滤工具纯函数。
 */
import type { InternshipItem } from '../types/internship'

export interface FilterState {
  keyword: string
  city: string
  category: string
  type: string
  /** 仅看今日新增 */
  onlyToday: boolean
  /** 仅看已收藏 */
  onlyFavorites: boolean
}

export const EMPTY_FILTER: FilterState = {
  keyword: '',
  city: '',
  category: '',
  type: '',
  onlyToday: false,
  onlyFavorites: false,
}

/** 从数据中提取去重后的城市列表 */
export function extractCities(items: InternshipItem[]): string[] {
  const set = new Set<string>()
  for (const it of items) if (it.city) set.add(it.city)
  return [...set]
}

/** 核心过滤：关键字 + 城市 + 分类 + 类型 + 今日 + 收藏 */
export function filterInternships(
  items: InternshipItem[],
  filter: FilterState,
  favorites: Set<string>,
): InternshipItem[] {
  const kw = filter.keyword.trim().toLowerCase()

  return items.filter((it) => {
    if (filter.onlyFavorites && !favorites.has(it.id)) return false

    if (filter.onlyToday) {
      const d = new Date(it.publishedAt)
      const now = new Date()
      if (
        d.getFullYear() !== now.getFullYear() ||
        d.getMonth() !== now.getMonth() ||
        d.getDate() !== now.getDate()
      ) {
        return false
      }
    }

    if (filter.city && it.city !== filter.city) return false
    if (filter.category && it.category !== filter.category) return false
    if (filter.type && it.type !== filter.type) return false

    if (kw) {
      const haystack = [
        it.title,
        it.company,
        it.companyEn ?? '',
        it.city,
        it.category,
        ...(it.tags ?? []),
      ]
        .join(' ')
        .toLowerCase()
      if (!haystack.includes(kw)) return false
    }

    return true
  })
}

/** 一键提取全部公司列表（用于品牌化展示） */
export function extractCompanies(items: InternshipItem[]): string[] {
  const set = new Set<string>()
  for (const it of items) if (it.company) set.add(it.company)
  return [...set]
}
