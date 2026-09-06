/**
 * 日期与展示相关工具纯函数。
 */

const DAY_MS = 24 * 60 * 60 * 1000

/** 将日期字符串解析为 Date，非法则返回 null */
export function parseDate(value: string): Date | null {
  const d = new Date(value)
  return Number.isNaN(d.getTime()) ? null : d
}

/** 相对当前时间的人类可读描述，如「3 天前」「2 小时前」 */
export function relativeTime(value: string): string {
  const d = parseDate(value)
  if (!d) return ''
  const diff = Date.now() - d.getTime()
  if (diff < 0) return '刚刚'
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes} 分钟前`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} 小时前`
  const days = Math.floor(hours / 24)
  if (days < 30) return `${days} 天前`
  return d.toLocaleDateString('zh-CN')
}

/** 是否为「今日新增」：与本地日期同日 */
export function isToday(value: string): boolean {
  const d = parseDate(value)
  if (!d) return false
  const now = new Date()
  return (
    d.getFullYear() === now.getFullYear() &&
    d.getMonth() === now.getMonth() &&
    d.getDate() === now.getDate()
  )
}

/** 是否为近 7 天内新增 */
export function isWithinDays(value: string, days: number): boolean {
  const d = parseDate(value)
  if (!d) return false
  return Date.now() - d.getTime() <= days * DAY_MS
}

/** 按发布时间倒序排序，返回新数组 */
export function sortByPublishedDesc<T extends { publishedAt: string }>(
  items: T[],
): T[] {
  return [...items].sort(
    (a, b) => parseDate(b.publishedAt)!.getTime() - parseDate(a.publishedAt)!.getTime(),
  )
}
