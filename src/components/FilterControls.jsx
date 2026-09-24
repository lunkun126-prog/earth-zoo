import { useMemo } from 'react'
import { useStore } from '../store/useStore.js'
import animals from '../data/animals.json'

const STATUS_OPTIONS = [
  { v: '全部', label: '全部' },
  { v: 'LC', label: '无危', color: '#81c784' },
  { v: 'NT', label: '近危', color: '#ffd54f' },
  { v: 'VU', label: '易危', color: '#ffb74d' },
  { v: 'EN', label: '濒危', color: '#e57373' },
  { v: 'CR', label: '极危', color: '#ef5350' },
]

function uniq(arr) {
  return Array.from(new Set(arr))
}

export default function FilterControls() {
  const filters = useStore((s) => s.filters)
  const setFilter = useStore((s) => s.setFilter)
  const resetFilters = useStore((s) => s.resetFilters)

  const options = useMemo(
    () => ({
      region: ['全部', ...uniq(animals.map((a) => a.region))],
      class: ['全部', ...uniq(animals.map((a) => a.class))],
      habitat: ['全部', ...uniq(animals.map((a) => a.habitat))],
    }),
    [],
  )

  const isDirty =
    filters.region !== '全部' ||
    filters.class !== '全部' ||
    filters.habitat !== '全部' ||
    filters.status !== '全部'

  return (
    <div className="filter-controls">
      <FilterRow
        label="区域"
        options={options.region}
        value={filters.region}
        onChange={(v) => setFilter('region', v)}
      />
      <FilterRow
        label="分类"
        options={options.class}
        value={filters.class}
        onChange={(v) => setFilter('class', v)}
      />
      <FilterRow
        label="栖息地"
        options={options.habitat}
        value={filters.habitat}
        onChange={(v) => setFilter('habitat', v)}
      />
      <div className="fc-row">
        <span className="fc-label">保护</span>
        <div className="fc-chips">
          {STATUS_OPTIONS.map((s) => {
            const active = filters.status === s.v
            return (
              <button
                key={s.v}
                className={`fc-chip ${active ? 'active' : ''}`}
                onClick={() => setFilter('status', s.v)}
                style={active && s.color ? { borderColor: s.color, color: s.color } : undefined}
              >
                {s.label}
              </button>
            )
          })}
        </div>
        {isDirty && (
          <button className="fc-reset" onClick={resetFilters}>
            清空
          </button>
        )}
      </div>
    </div>
  )
}

function FilterRow({ label, options, value, onChange }) {
  return (
    <div className="fc-row">
      <span className="fc-label">{label}</span>
      <div className="fc-chips">
        {options.map((opt) => (
          <button
            key={opt}
            className={`fc-chip ${value === opt ? 'active' : ''}`}
            onClick={() => onChange(opt)}
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  )
}
