import { useMemo, useState } from 'react'
import { useInternships } from './hooks/useInternships'
import { useFavorites } from './hooks/useFavorites'
import { FilterBar } from './components/FilterBar'
import { InternCard } from './components/InternCard'
import { SortSelect } from './components/SortSelect'
import { EMPTY_FILTER, extractCities, filterInternships } from './lib/filter'
import { sortInternships } from './lib/sort'
import type { SortKey } from './lib/sort'

type View = 'all' | 'favorites'

/** 从 URL ?_view= 读取初始视图（支持深链到收藏页） */
function initialView(): View {
  if (typeof window !== 'undefined') {
    const p = new URLSearchParams(window.location.search)
    if (p.get('_view') === 'favorites') return 'favorites'
  }
  return 'all'
}

export default function App() {
  const { items, dataset, loading, error } = useInternships()
  const { favorites, toggle } = useFavorites()

  const [view, setView] = useState<View>(initialView)
  const [filter, setFilter] = useState(EMPTY_FILTER)
  const [onlyFavorites, setOnlyFavorites] = useState(false)
  const [sort, setSort] = useState<SortKey>('latest')

  const cities = useMemo(() => extractCities(items), [items])

  // 收藏页视图：仅看已收藏（不套用筛选栏条件，独立完整展示）
  const favoriteItems = useMemo(() => {
    const favs = items.filter((it) => favorites.has(it.id))
    return sortInternships(favs, sort)
  }, [items, favorites, sort])

  // 全部页视图：套用筛选 + 排序
  const visible = useMemo(() => {
    const f = { ...filter, onlyFavorites }
    const filtered = filterInternships(items, f, favorites)
    return sortInternships(filtered, sort)
  }, [items, filter, onlyFavorites, favorites, sort])

  const sourcesLabel = dataset?.sources.join(' · ') ?? ''
  const count = view === 'favorites' ? favoriteItems.length : items.length

  const resetAll = () => {
    setFilter(EMPTY_FILTER)
    setOnlyFavorites(false)
  }

  const NavTab = ({ id, label }: { id: View; label: string }) => (
    <button
      type="button"
      onClick={() => setView(id)}
      className={`inline-flex h-9 items-center rounded-lg px-4 text-sm font-medium transition ${
        view === id ? 'bg-indigo-600 text-white shadow' : 'text-slate-600 hover:bg-slate-100'
      }`}
    >
      {label}
    </button>
  )

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

          {/* 视图切换 */}
          <nav className="flex items-center gap-1 rounded-xl bg-slate-100 p-1">
            <NavTab id="all" label="全部岗位" />
            <NavTab id="favorites" label={`我的收藏 ${favorites.size > 0 ? `(${favorites.size})` : ''}`} />
          </nav>

          {!loading && !error && (
            <span className="hidden text-sm text-slate-500 md:block">
              共 <span className="font-semibold text-indigo-600">{count}</span> 个机会
            </span>
          )}
        </div>
      </header>

      {/* 主体 */}
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        {/* 主视觉 (仅全部页显示) */}
        {view === 'all' && (
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
        )}

        {/* 筛选 + 排序栏 (仅全部页) */}
        {view === 'all' && (
          <div className="mb-6">
            <FilterBar
              filter={filter}
              cities={cities}
              onChange={setFilter}
              favoritesActive={onlyFavorites}
              onToggleFavoritesOnly={() => setOnlyFavorites((v) => !v)}
            />
          </div>
        )}

        {/* 收藏页标题 */}
        {view === 'favorites' && (
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-800">我的收藏</h2>
              <p className="mt-1 text-sm text-slate-400">已收藏 {favoriteItems.length} 个校招/实习机会，收藏保存在本机浏览器。</p>
            </div>
            <SortSelect value={sort} onChange={setSort} />
          </div>
        )}

        {/* 全部页排序栏 */}
        {view === 'all' && !loading && !error && visible.length > 0 && (
          <div className="mb-4 flex items-center justify-end">
            <SortSelect value={sort} onChange={setSort} />
          </div>
        )}

        {/* 状态提示 */}
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {/* 列表 */}
        {!loading && !error && view === 'all' && (
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
            <EmptyState hasFilters={Object.values(filter).some(Boolean) || onlyFavorites} hasFavorites={false} onReset={resetAll} />
          )
        )}

        {!loading && !error && view === 'favorites' && (
          favoriteItems.length > 0 ? (
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {favoriteItems.map((item) => (
                <InternCard
                  key={item.id}
                  item={item}
                  favorite={favorites.has(item.id)}
                  onToggleFavorite={() => toggle(item.id)}
                />
              ))}
            </div>
          ) : (
            <EmptyState hasFilters={false} hasFavorites={true} onReset={() => setView('all')} />
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

function EmptyState({ hasFilters, hasFavorites, onReset }: { hasFilters: boolean; hasFavorites: boolean; onReset: () => void }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center">
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-2xl">🔍</div>
      <p className="mt-4 text-sm font-semibold text-slate-700">
        {hasFavorites ? '还没有收藏任何岗位' : '没有找到匹配的校招/实习机会'}
      </p>
      <p className="mt-1 text-sm text-slate-400">
        {hasFavorites
          ? '在岗位卡片右上角点击爱心即可收藏，方便随时查看。'
          : hasFilters
            ? '试试调整筛选条件，或清空后重新搜索。'
            : '数据正在更新中，请稍后再来。'}
      </p>
      {(hasFavorites || hasFilters) && (
        <button
          type="button"
          onClick={onReset}
          className="mt-5 inline-flex h-10 items-center rounded-xl bg-indigo-600 px-5 text-sm font-semibold text-white transition hover:bg-indigo-700"
        >
          {hasFavorites ? '去看看全部岗位' : '清除筛选条件'}
        </button>
      )}
    </div>
  )
}
