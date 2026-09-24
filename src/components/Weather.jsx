import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useStore } from '../store/useStore.js'

const GLOBE_RADIUS = 100

function randomSpherePoint(rMin, rMax) {
  const phi = Math.acos(2 * Math.random() - 1)
  const theta = 2 * Math.PI * Math.random()
  const r = rMin + Math.random() * (rMax - rMin)
  return [
    r * Math.sin(phi) * Math.cos(theta),
    r * Math.cos(phi),
    r * Math.sin(phi) * Math.sin(theta),
  ]
}

function FallingParticles({
  count,
  rOuter,
  rInner,
  speed,
  size,
  color,
  opacity,
  drift = 0,
}) {
  const ref = useRef()
  const positions = useMemo(() => {
    const arr = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const [x, y, z] = randomSpherePoint(rInner, rOuter)
      arr[i * 3] = x
      arr[i * 3 + 1] = y
      arr[i * 3 + 2] = z
    }
    return arr
  }, [count, rInner, rOuter])

  useFrame((_, delta) => {
    const obj = ref.current
    if (!obj) return
    const pos = obj.geometry.attributes.position.array
    const d = Math.min(delta, 0.05)
    for (let i = 0; i < count; i++) {
      let x = pos[i * 3]
      let y = pos[i * 3 + 1]
      let z = pos[i * 3 + 2]
      const r = Math.sqrt(x * x + y * y + z * z)
      const newR = r - speed * d
      if (newR <= rInner) {
        const [nx, ny, nz] = randomSpherePoint(rOuter - 4, rOuter)
        pos[i * 3] = nx
        pos[i * 3 + 1] = ny
        pos[i * 3 + 2] = nz
      } else {
        const k = newR / r
        pos[i * 3] = x * k + (Math.random() - 0.5) * drift * d
        pos[i * 3 + 1] = y * k
        pos[i * 3 + 2] = z * k + (Math.random() - 0.5) * drift * d
      }
    }
    obj.geometry.attributes.position.needsUpdate = true
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={size}
        transparent
        opacity={opacity}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}

function OrbitingParticles({
  count,
  rOuter,
  rInner,
  speed,
  size,
  color,
  opacity,
}) {
  const ref = useRef()
  const data = useMemo(() => {
    const positions = new Float32Array(count * 3)
    const params = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const phi = Math.acos(2 * Math.random() - 1)
      const theta = 2 * Math.PI * Math.random()
      const r = rInner + Math.random() * (rOuter - rInner)
      params[i * 3] = phi
      params[i * 3 + 1] = theta
      params[i * 3 + 2] = r
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta)
      positions[i * 3 + 1] = r * Math.cos(phi)
      positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta)
    }
    return { positions, params }
  }, [count, rInner, rOuter])

  useFrame((_, delta) => {
    const obj = ref.current
    if (!obj) return
    const pos = obj.geometry.attributes.position.array
    const { params } = data
    const d = Math.min(delta, 0.05)
    for (let i = 0; i < count; i++) {
      params[i * 3 + 1] += speed * d
      const phi = params[i * 3]
      const theta = params[i * 3 + 1]
      const r = params[i * 3 + 2]
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta)
      pos[i * 3 + 1] = r * Math.cos(phi)
      pos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta)
    }
    obj.geometry.attributes.position.needsUpdate = true
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={data.positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={size}
        transparent
        opacity={opacity}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}

export default function Weather() {
  const weather = useStore((s) => s.weather)
  return (
    <>
      {weather.rain && (
        <FallingParticles
          count={2200}
          rInner={GLOBE_RADIUS + 1}
          rOuter={GLOBE_RADIUS + 40}
          speed={28}
          size={0.55}
          color="#9ec5ff"
          opacity={0.85}
          drift={1.5}
        />
      )}
      {weather.snow && (
        <FallingParticles
          count={1500}
          rInner={GLOBE_RADIUS + 1}
          rOuter={GLOBE_RADIUS + 35}
          speed={5}
          size={1.0}
          color="#ffffff"
          opacity={0.9}
          drift={4}
        />
      )}
      {weather.wind && (
        <OrbitingParticles
          count={1200}
          rInner={GLOBE_RADIUS + 5}
          rOuter={GLOBE_RADIUS + 25}
          speed={0.9}
          size={0.45}
          color="#e0f0ff"
          opacity={0.55}
        />
      )}
      {weather.sand && (
        <FallingParticles
          count={1000}
          rInner={GLOBE_RADIUS + 1}
          rOuter={GLOBE_RADIUS + 18}
          speed={3}
          size={0.7}
          color="#e8a35a"
          opacity={0.7}
          drift={6}
        />
      )}
    </>
  )
}
