interface FavoriteButtonProps {
  active: boolean
  onToggle: () => void
}

/** 收藏按钮：实现「收藏/取消收藏」即时反馈 */
export function FavoriteButton({ active, onToggle }: FavoriteButtonProps) {
  return (
    <button
      type="button"
      onClick={(e) => {
        e.preventDefault()
        e.stopPropagation()
        onToggle()
      }}
      aria-label={active ? '取消收藏' : '收藏'}
      title={active ? '取消收藏' : '收藏'}
      className={`group inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full transition ${
        active
          ? 'bg-rose-50 text-rose-500'
          : 'text-slate-400 hover:bg-slate-100 hover:text-rose-400'
      }`}
    >
      <svg
        viewBox="0 0 24 24"
        className="h-5 w-5"
        fill={active ? 'currentColor' : 'none'}
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
      </svg>
    </button>
  )
}
