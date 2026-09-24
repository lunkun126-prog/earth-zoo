import { useMemo } from 'react'
import { Billboard } from '@react-three/drei'
import { Text } from '@react-three/drei'
import { GLOBE_RADIUS } from './Earth.jsx'
import { useStore } from '../store/useStore.js'

const PLANT_EMOJIS = ['🌳', '🌲', '🌴', '🌵', '🌿', '🌾', '🪴', '🌷', '🌻', '🌼', '🌺', '🍀']

function fibonacciSphere(n, radius) {
  const pts = []
  const offset = 2 / n
  const increment = Math.PI * (3 - Math.sqrt(5))
  for (let i = 0; i < n; i++) {
    const y = i * offset - 1 + offset / 2
    const r = Math.sqrt(1 - y * y)
    const phi = i * increment
    pts.push([
      Math.cos(phi) * r * radius,
      y * radius,
      Math.sin(phi) * r * radius,
    ])
  }
  return pts
}

export default function Plants({ count = 120 }) {
  const showPlants = useStore((s) => s.showPlants)
  const items = useMemo(() => {
    const positions = fibonacciSphere(count, GLOBE_RADIUS + 1.6)
    return positions.map((p, i) => ({
      pos: p,
      emoji: PLANT_EMOJIS[i % PLANT_EMOJIS.length],
      size: 2.5 + ((i * 37) % 10) * 0.18,
    }))
  }, [count])

  if (!showPlants) return null

  return (
    <>
      {items.map((it, i) => (
        <Billboard key={i} position={it.pos}>
          <Text
            fontSize={it.size}
            anchorX="center"
            anchorY="middle"
            fillOpacity={0.85}
          >
            {it.emoji}
          </Text>
        </Billboard>
      ))}
    </>
  )
}
