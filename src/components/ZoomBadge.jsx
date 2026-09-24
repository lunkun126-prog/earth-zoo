import { useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'

const MIN_DIST = 108
const MAX_DIST = 500

function ZoomTracker({ valueRef }) {
  const { camera } = useThree()
  const lastWritten = useRef(-1)
  useFrame(() => {
    const d = camera.position.length()
    const k = (MAX_DIST - d) / (MAX_DIST - MIN_DIST)
    const pct = Math.round(Math.max(0, Math.min(1, k)) * 200 + 100)
    if (pct !== lastWritten.current && valueRef.current) {
      valueRef.current.textContent = `${pct}%`
      lastWritten.current = pct
    }
  })
  return null
}

export default function ZoomBadge() {
  const valueRef = useRef()
  return (
    <>
      <div className="zoom-badge">
        <span ref={valueRef}>100%</span>
      </div>
      <ZoomTracker valueRef={valueRef} />
    </>
  )
}

export { ZoomTracker, MIN_DIST, MAX_DIST }
