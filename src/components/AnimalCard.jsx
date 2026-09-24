import { useEffect, useState } from 'react'
import { useStore } from '../store/useStore.js'
import { playSound, stopSound } from '../lib/sound.js'

const STATUS_LABEL = {
  LC: '无危',
  NT: '近危',
  VU: '易危',
  EN: '濒危',
  CR: '极危',
}

const STATUS_LEVEL = { LC: 1, NT: 2, VU: 3, EN: 4, CR: 5 }

const DIET_LABEL = {
  carnivore: '肉食',
  herbivore: '草食',
  omnivore: '杂食',
  insectivore: '食虫',
  piscivore: '食鱼',
}

const DIET_COLOR = {
  carnivore: '#ff7a6e',
  herbivore: '#7cd17c',
  omnivore: '#ffc14a',
  insectivore: '#a78bfa',
  piscivore: '#5eb0ff',
}

export default function AnimalCard() {
  const selected = useStore((s) => s.selected)
  const clearSelected = useStore((s) => s.clearSelected)
  const [playing, setPlaying] = useState(false)

  // 关闭卡片或切换动物时,停掉正在播的叫声并复位播放按钮
  // (hooks 必须放在下面的 early return 之前)
  useEffect(() => {
    stopSound()
    setPlaying(false)
  }, [selected])

  if (!selected) return null

  const dietColor = DIET_COLOR[selected.diet] ?? '#aaa'
  const level = STATUS_LEVEL[selected.status] ?? 0
  const hasSound = !!selected.sound

  const onPlay = () => {
    const started = playSound(selected.id, selected.sound, () => setPlaying(false))
    setPlaying(started)
  }

  return (
    <div className="card">
      <button className="card-close" onClick={clearSelected} aria-label="关闭">✕</button>
      <div className="card-img-wrap">
        <img src={`/animals/${selected.id}.png`} alt={selected.name_cn} />
        {hasSound && (
          <button
            className={`sound-btn ${playing ? 'playing' : ''}`}
            onClick={onPlay}
            title={playing ? '停止' : '播放叫声'}
            aria-label="播放叫声"
          >
            {playing ? '⏸' : '🔊'}
          </button>
        )}
      </div>
      <div className="name-row">
        <span className="name-cn">{selected.name_cn}</span>
        <span className={`status ${selected.status}`}>
          {STATUS_LABEL[selected.status] ?? selected.status}
        </span>
      </div>
      <div className="latin">{selected.name_latin}</div>
      <div className="desc">{selected.desc}</div>

      <div className="viz-row">
        <div className="viz-label">食性</div>
        <div className="viz-bar">
          <div
            className="viz-fill"
            style={{ width: '100%', background: dietColor }}
          />
          <span className="viz-text" style={{ color: dietColor }}>
            {DIET_LABEL[selected.diet] ?? selected.diet}
          </span>
        </div>
      </div>

      <div className="viz-row">
        <div className="viz-label">濒危</div>
        <div className="status-bar">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className={`status-seg ${i <= level ? 'on' : ''} lvl-${i}`}
            />
          ))}
        </div>
      </div>

      <div className="meta">
        {selected.class} · {selected.habitat} · {selected.region}
      </div>
    </div>
  )
}
