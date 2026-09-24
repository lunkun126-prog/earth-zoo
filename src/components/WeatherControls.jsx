import { useStore } from '../store/useStore.js'

const ITEMS = [
  { key: 'rain', label: '雨', emoji: '🌧️', activeColor: '#5b9bff' },
  { key: 'snow', label: '雪', emoji: '❄️', activeColor: '#ffffff' },
  { key: 'wind', label: '风', emoji: '💨', activeColor: '#b8d4e8' },
  { key: 'sand', label: '沙', emoji: '🌪️', activeColor: '#e8a35a' },
]

export default function WeatherControls() {
  const weather = useStore((s) => s.weather)
  const toggleWeather = useStore((s) => s.toggleWeather)

  return (
    <div className="weather-controls">
      <span className="wc-label">天气</span>
      {ITEMS.map((it) => {
        const active = weather[it.key]
        return (
          <button
            key={it.key}
            className={`wc-chip ${active ? 'active' : ''}`}
            onClick={() => toggleWeather(it.key)}
            style={active ? { borderColor: it.activeColor, color: it.activeColor } : undefined}
          >
            <span className="wc-emoji">{it.emoji}</span>
            <span>{it.label}</span>
          </button>
        )
      })}
    </div>
  )
}
