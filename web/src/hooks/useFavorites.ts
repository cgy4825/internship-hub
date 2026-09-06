/**
 * 收藏 Hook：基于 localStorage，无需用户系统（见 ADR-0003）。
 */
import { useCallback, useState } from 'react'

const STORAGE_KEY = 'internship-hub:favorites'

function readInitial(): Set<string> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return new Set()
    const parsed: unknown = JSON.parse(raw)
    if (Array.isArray(parsed)) return new Set(parsed.map(String))
    return new Set()
  } catch {
    return new Set()
  }
}

export function useFavorites() {
  const [favorites, setFavorites] = useState<Set<string>>(() => readInitial())

  const persist = useCallback((next: Set<string>) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...next]))
  }, [])

  const toggle = useCallback(
    (id: string) => {
      setFavorites((prev) => {
        const next = new Set(prev)
        if (next.has(id)) next.delete(id)
        else next.add(id)
        persist(next)
        return next
      })
    },
    [persist],
  )

  const has = useCallback((id: string) => favorites.has(id), [favorites])

  return { favorites, toggle, has }
}
