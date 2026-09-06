import type { FilterState } from '../lib/filter'
import { CATEGORIES, TYPE_LABEL } from '../types/internship'
import type { InternshipType } from '../types/internship'

interface FilterBarProps {
  filter: FilterState
  cities: string[]
  onChange: (next: FilterState) => void
  favoritesActive: boolean
  onToggleFavoritesOnly: () => void
}

const selectBase =
  'h-10 appearance-none rounded-xl border border-slate-200 bg-white pl-3.5 pr-9 text-sm text-slate-700 shadow-sm outline-none transition focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100'

/** 搜索 + 筛选栏 */
export function FilterBar({
  filter,
  cities,
  onChange,
  favoritesActive,
  onToggleFavoritesOnly,
}: FilterBarProps) {
  const set = (patch: Partial<FilterState>) => onChange({ ...filter, ...patch })

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        {/* 搜索框 */}
        <div className="relative flex-1">
          <svg
            viewBox="0 0 24 24"
            className="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="11" cy="11" r="7" />
            <path d="m21 21-4.3-4.3" />
          </svg>
          <input
            type="search"
            value={filter.keyword}
            onChange={(e) => set({ keyword: e.target.value })}
            placeholder="搜索公司 / 岗位 / 城市 / 标签…"
            className="h-10 w-full rounded-xl border border-slate-200 bg-white pl-11 pr-4 text-sm text-slate-700 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {/* 城市 */}
          <div className="relative">
            <select value={filter.city} onChange={(e) => set({ city: e.target.value })} className={selectBase}>
              <option value="">全部城市</option>
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
            <ChevronDown />
          </div>

          {/* 岗位方向 */}
          <div className="relative">
            <select value={filter.category} onChange={(e) => set({ category: e.target.value })} className={selectBase}>
              <option value="">全部方向</option>
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
            <ChevronDown />
          </div>

          {/* 类型 */}
          <div className="relative">
            <select value={filter.type} onChange={(e) => set({ type: e.target.value })} className={selectBase}>
              <option value="">全部类型</option>
              {(Object.keys(TYPE_LABEL) as InternshipType[]).map((t) => (
                <option key={t} value={t}>
                  {TYPE_LABEL[t]}
                </option>
              ))}
            </select>
            <ChevronDown />
          </div>

          {/* 今日新增开关 */}
          <button
            type="button"
            onClick={() => set({ onlyToday: !filter.onlyToday })}
            className={`inline-flex h-10 items-center gap-1.5 rounded-xl border px-3.5 text-sm font-medium shadow-sm transition ${
              filter.onlyToday
                ? 'border-emerald-300 bg-emerald-50 text-emerald-600'
                : 'border-slate-200 bg-white text-slate-600 hover:border-emerald-200'
            }`}
          >
            <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="4" />
              <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
            </svg>
            今日新增
          </button>

          {/* 收藏开关 */}
          <button
            type="button"
            onClick={onToggleFavoritesOnly}
            className={`inline-flex h-10 items-center gap-1.5 rounded-xl border px-3.5 text-sm font-medium shadow-sm transition ${
              favoritesActive
                ? 'border-rose-300 bg-rose-50 text-rose-600'
                : 'border-slate-200 bg-white text-slate-600 hover:border-rose-200'
            }`}
          >
            <svg viewBox="0 0 24 24" className="h-4 w-4" fill={favoritesActive ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
            </svg>
            已收藏
          </button>
        </div>
      </div>
    </div>
  )
}

function ChevronDown() {
  return (
    <svg
      viewBox="0 0 24 24"
      className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  )
}
