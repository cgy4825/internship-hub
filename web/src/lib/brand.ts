/**
 * 公司品牌色工具：根据公司名生成稳定、美观的渐变/颜色。
 * 作为 logo 占位（无图片时的品牌化展示）。
 */
const PALETTE: Array<[string, string]> = [
  ['#6366f1', '#8b5cf6'], // indigo -> violet
  ['#0ea5e9', '#2563eb'], // sky -> blue
  ['#f59e0b', '#ef4444'], // amber -> red
  ['#10b981', '#14b8a6'], // emerald -> teal
  ['#ec4899', '#8b5cf6'], // pink -> violet
  ['#f97316', '#f43f5e'], // orange -> rose
  ['#22c55e', '#0ea5e9'], // green -> sky
  ['#a855f7', '#6366f1'], // purple -> indigo
]

function hashString(value: string): number {
  let hash = 0
  for (let i = 0; i < value.length; i++) {
    hash = (hash << 5) - hash + value.charCodeAt(i)
    hash |= 0
  }
  return Math.abs(hash)
}

/** 取公司名首字符，用于 logo 展示 */
export function companyInitial(company: string): string {
  const c = company.trim()
  return c ? c[0].toUpperCase() : '?'
}

/** 根据公司名生成稳定的渐变背景色对 (from, to) */
export function companyGradient(company: string): [string, string] {
  const idx = hashString(company) % PALETTE.length
  return PALETTE[idx]
}
