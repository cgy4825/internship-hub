import { useEffect, useState } from 'react'
import type { InternshipItem } from '../types/internship'
import { TYPE_LABEL } from '../types/internship'
import { relativeTime, isToday } from '../lib/date'
import { companyGradient, companyInitial } from '../lib/brand'
import { FavoriteButton } from './FavoriteButton'

/** 来源标识 -> 中文名 */
const SOURCE_LABEL: Record<string, string> = {
  nowcoder: '牛客网',
  company_website: '公司官网',
  seed: '演示数据',
  yingjiesheng: '应届生求职网',
}

function sourceLabel(source: string): string {
  return SOURCE_LABEL[source] ?? source
}

interface InternCardProps {
  item: InternshipItem
  favorite: boolean
  onToggleFavorite: () => void
}

/** 单个实习信息卡片，点击整卡深链跳转到投递渠道 */
export function InternCard({ item, favorite, onToggleFavorite }: InternCardProps) {
  const [gradient, setGradient] = useState<[string, string]>(
    companyGradient(item.company),
  )

  useEffect(() => {
    setGradient(companyGradient(item.company))
  }, [item.company])

  const today = isToday(item.publishedAt)

  return (
    <a
      href={item.applyUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="group relative flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:border-indigo-200 hover:shadow-xl hover:shadow-indigo-100/60"
    >
      {/* 卡片右上角日期+收藏 */}
      <div className="absolute right-4 top-4 flex items-center gap-2">
        {today && (
          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-600">
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500" />
            </span>
            今日新增
          </span>
        )}
        <FavoriteButton active={favorite} onToggle={onToggleFavorite} />
      </div>

      {/* 公司 logo + 公司名 */}
      <div className="flex items-center gap-3 pr-16">
        <div
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-lg font-bold text-white shadow-sm"
          style={{
            background: `linear-gradient(135deg, ${gradient[0]}, ${gradient[1]})`,
          }}
        >
          {companyInitial(item.company)}
        </div>
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold text-slate-800">
            {item.company}
            {item.companyEn && (
              <span className="ml-1.5 text-xs font-normal text-slate-400">
                {item.companyEn}
              </span>
            )}
          </div>
          <div className="mt-0.5 flex items-center gap-1.5 text-xs text-slate-400">
            {item.city && (
              <span className="inline-flex items-center gap-0.5">
                <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={2}>
                  <path d="M12 21s-7-5.1-7-11a7 7 0 0 1 14 0c0 5.9-7 11-7 11z" />
                  <circle cx="12" cy="10" r="2.5" />
                </svg>
                {item.city}
              </span>
            )}
            {item.city && (
              <span>·</span>
            )}
            {relativeTime(item.publishedAt) && (
              <span className="inline-flex items-center gap-0.5">
                <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={2}>
                  <circle cx="12" cy="12" r="9" />
                  <path d="M12 7v5l3 2" />
                </svg>
                {relativeTime(item.publishedAt)}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* 岗位标题 */}
      <h3 className="mt-4 line-clamp-2 text-base font-semibold leading-snug text-slate-900 transition-colors group-hover:text-indigo-600">
        {item.title}
      </h3>

      {/* 关键元信息：薪资/学历/实习时长/公司规模 */}
      {(item.summary || item.education || item.workDuration || item.companyType) && (
        <div className="mt-2.5 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs">
          {item.summary && (
            <span className="inline-flex items-center font-medium text-amber-600">
              {item.summary}
            </span>
          )}
          {item.workDuration && (
            <span className="inline-flex items-center gap-0.5 text-slate-400">
              <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" />
                <path d="M16 2v4M8 2v4M3 10h18" />
              </svg>
              {item.workDuration}
            </span>
          )}
          {item.companyType && (
            <span className="inline-flex items-center gap-0.5 text-slate-400">
              <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 21V8l7-4v3M10 21V7l8 4v10M3 21h18" />
              </svg>
              {item.companyType}
            </span>
          )}
        </div>
      )}

      {/* 标签 */}
      <div className="mt-2.5 flex flex-wrap gap-1.5">
        <span className="inline-flex items-center rounded-md bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-600">
          {TYPE_LABEL[item.type]}
        </span>
        {item.category && (
          <span className="inline-flex items-center rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
            {item.category}
          </span>
        )}
        {item.education && (
          <span className="inline-flex items-center rounded-md bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-600">
            {item.education}
          </span>
        )}
        {(item.tags ?? []).slice(0, 3).map((tag) => (
          <span
            key={tag}
            className="inline-flex items-center rounded-md bg-slate-50 px-2 py-0.5 text-xs text-slate-500 ring-1 ring-inset ring-slate-200"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* 摘要 */}
      {item.summary && (
        <p className="mt-3 line-clamp-2 text-sm leading-relaxed text-slate-500">
          {item.summary}
        </p>
      )}

      {/* 底部：投递按钮（深链） */}
      <div className="mt-auto flex items-center justify-between pt-4">
        <span className="text-xs text-slate-400">
          来源：{sourceLabel(item.source)}
        </span>
        <span className="inline-flex items-center gap-1 rounded-lg bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white transition-colors group-hover:bg-indigo-600">
          立即投递
          <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
            <path d="M7 17L17 7M7 7h10v10" />
          </svg>
        </span>
      </div>
    </a>
  )
}
