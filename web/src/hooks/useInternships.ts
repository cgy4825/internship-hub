/**
 * 加载实习数据 Hook。
 * 从静态 JSON（/data/internships.json）读取，符合「数据与展示解耦」原则。
 */
import { useEffect, useState } from 'react'
import type { InternshipDataset, InternshipItem } from '../types/internship'

const DATA_URL = '/data/internships.json'

interface UseInternshipsResult {
  items: InternshipItem[]
  dataset: InternshipDataset | null
  loading: boolean
  error: string | null
}

export function useInternships(): UseInternshipsResult {
  const [dataset, setDataset] = useState<InternshipDataset | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        const res = await fetch(DATA_URL)
        if (!res.ok) throw new Error(`加载数据失败：HTTP ${res.status}`)
        const json = (await res.json()) as InternshipDataset
        if (cancelled) return

        // 仅保留有效岗位，并按发布时间倒序
        const active = json.items.filter((it) => it.isActive)
        setDataset({ ...json, items: active })
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : '未知错误')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [])

  return { items: dataset?.items ?? [], dataset, loading, error }
}
