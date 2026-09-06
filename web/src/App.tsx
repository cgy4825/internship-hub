import { useMemo, useState } from 'react'
import { useInternships } from './hooks/useInternships'
import { useFavorites } from './hooks/useFavorites'
import { FilterBar } from './components/FilterBar'
import { InternCard } from './components/InternCard'
import { EMPTY_FILTER, extractCities, filterInternships } from './lib/filter'
import { sortByPublishedDesc } from './lib/date'

export default function App() {
  const { items, dataset, loading, error } = useInternships()
  const { favorites, toggle } = useFavorites()

  const [filter, setFilter] = useState(EMPTY_FILTER)
  const [onlyFavorites, setOnlyFavorites] = useState(false)

  const cities = useMemo(() => extractCities(items), [items])

  const visible = useMemo(() => {
    const f = { ...filter, onlyFavorites }
    const filtered = filterInternships(items, f, favorites)
    return sortByPublishedDesc(filtered)
  }, [items, filter, onlyFavorites, favorites])

  const sourcesLabel = dataset?.sources.join(' · ') ?? ''

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 顶部导航 */}
      <header className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/80 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow">🏢</div>
            <div>
              <h1 className="text-base font-bold leading-tight text-slate-900">校招实习信息聚合</h1>
              <p className="text-xs leading-tight text-slate-400">汇聚名企校招 · 每日更新</p>
            </div>
          </div>
          {!loading && !error && (
            <span className="hidden text-sm text-slate-500 sm:block">
              共 <span className="font-semibold text-indigo-600">{items.length}</span> 个校招/实习机会
            </span>
          )}
        </div>
      </header>

      {/* 主体 */}
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        {/* 主视觉 */}
        <section className="relative mb-8 overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-500 via-violet-500 to-fuchsia-500 p-8 text-white shadow-xl shadow-indigo-200/60 sm:p-12">
          <div className="relative z-10 max-w-2xl">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-white/20 px-3 py-1 text-xs font-medium backdrop-blur">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-300" />
              {sourcesLabel || '数据源聚合'}
            </span>
            <h2 className="mt-4 text-3xl font-bold leading-tight sm:text-4xl">
              汇聚校招实习机会
              <br />
              让投递一步到位
            </h2>
            <p className="mt-3 max-w-xl text-sm leading-relaxed text-indigo-50/90">
              集中展示各大公司公开的校招与实习信息（含知名大厂及其他优质用人单位），支持搜索、筛选、收藏，点击卡片即可跳转官方投递渠道。
            </p>
          </div>
          <div className="pointer-events-none absolute -right-16 -top-16 h-64 w-64 rounded-full bg-white/10 blur-2xl" />
          <div className="pointer-events-none absolute -bottom-20 right-24 h-48 w-48 rounded-full bg-fuchsia-300/20 blur-2xl" />
        </section>

        {/* 筛选栏 */}
        <div className="mb-6">
          <FilterBar
            filter={filter}
            cities={cities}
            onChange={setFilter}
            favoritesActive={onlyFavorites}
            onToggleFavoritesOnly={() => setOnlyFavorites((v) => !v)}
          />
        </div>

        {/* 状态提示 */}
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {/* 列表 */}
        {!loading && !error && (
          visible.length > 0 ? (
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {visible.map((item) => (
                <InternCard
                  key={item.id}
                  item={item}
                  favorite={favorites.has(item.id)}
                  onToggleFavorite={() => toggle(item.id)}
                />
              ))}
            </div>
          ) : (
            <EmptyState hasFilters={Object.values(filter).some(Boolean) || onlyFavorites} onReset={() => { setFilter(EMPTY_FILTER); setOnlyFavorites(false) }} />
          )
        )}
      </main>

      <footer className="border-t border-slate-200 py-8">
        <div className="mx-auto max-w-6xl px-4 text-center text-xs text-slate-400 sm:px-6">
          本站为校招/实习信息聚合索引页，仅展示结构化元信息，点击将跳转至对应公司官方投递渠道。
          <br />
          数据每日更新，仅供参考，以官方发布为准。
        </div>
      </footer>
    </div>
  )
}

function LoadingState() {
  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="h-56 animate-pulse rounded-2xl border border-slate-200 bg-white p-5">
          <div className="flex gap-3">
            <div className="h-11 w-11 rounded-xl bg-slate-200" />
            <div className="flex-1 space-y-2">
              <div className="h-4 w-2/3 rounded bg-slate-200" />
              <div className="h-3 w-1/2 rounded bg-slate-100" />
            </div>
          </div>
          <div className="mt-4 h-4 w-3/4 rounded bg-slate-200" />
          <div className="mt-3 space-y-2">
            <div className="h-3 w-full rounded bg-slate-100" />
            <div className="h-3 w-5/6 rounded bg-slate-100" />
          </div>
        </div>
      ))}
    </div>
  )
}

function ErrorState({ message }: { message: string }) {
  return (
    <div className="rounded-2xl border border-rose-200 bg-rose-50 p-8 text-center">
      <p className="text-sm font-semibold text-rose-600">加载失败</p>
      <p className="mt-1 text-sm text-rose-500">{message}</p>
      <p className="mt-2 text-xs text-rose-400">请刷新页面重试。</p>
    </div>
  )
}

function EmptyState({ hasFilters, onReset }: { hasFilters: boolean; onReset: () => void }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center">
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-2xl">🔍</div>
      <p className="mt-4 text-sm font-semibold text-slate-700">没有找到匹配的实习机会</p>
      <p className="mt-1 text-sm text-slate-400">{hasFilters ? '试试调整筛选条件，或清空后重新搜索。' : '数据正在更新中，请稍后再来。'}</p>
      {hasFilters && (
        <button
          type="button"
          onClick={onReset}
          className="mt-5 inline-flex h-10 items-center rounded-xl bg-indigo-600 px-5 text-sm font-semibold text-white transition hover:bg-indigo-700"
        >
          清除筛选条件
        </button>
      )}
    </div>
  )
}
