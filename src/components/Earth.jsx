import { useMemo, useRef } from 'react'
import * as THREE from 'three'
import { Billboard, useTexture } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useStore, matchFilters } from '../store/useStore.js'

export const GLOBE_RADIUS = 100
const EARTH_TEXTURE = 'https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg'
const BUMP_TEXTURE = 'https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png'

export function lonLatToVec3(lon, lat, r = GLOBE_RADIUS) {
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lon + 180) * (Math.PI / 180)
  return [
    -r * Math.sin(phi) * Math.cos(theta),
    r * Math.cos(phi),
    r * Math.sin(phi) * Math.sin(theta),
  ]
}

function AnimalImage({ animal, dim, highlighted }) {
  const texture = useTexture(`/animals/${animal.id}.png`)
  const setSelected = useStore((s) => s.setSelected)
  const meshRef = useRef()

  let size = 9
  if (dim) size = 5
  else if (highlighted) size = 16

  useFrame((_, delta) => {
    if (!meshRef.current || !highlighted) return
    const m = meshRef.current
    m.rotation.z += delta * 0.6
  })

  return (
    <mesh
      ref={meshRef}
      onClick={(e) => {
        if (dim) return
        e.stopPropagation()
        setSelected(animal)
      }}
      onPointerOver={() => !dim && (document.body.style.cursor = 'pointer')}
      onPointerOut={() => (document.body.style.cursor = 'auto')}
    >
      <planeGeometry args={[size, size]} />
      <meshBasicMaterial
        map={texture}
        transparent
        opacity={dim ? 0.18 : 1}
        depthWrite={false}
        side={THREE.DoubleSide}
      />
    </mesh>
  )
}

function AnimalSprite({ animal, offset = 5, dim, highlighted }) {
  const pos = useMemo(
    () => lonLatToVec3(animal.lon, animal.lat, GLOBE_RADIUS + offset),
    [animal.lon, animal.lat, offset],
  )

  return (
    <Billboard position={pos}>
      <AnimalImage animal={animal} dim={dim} highlighted={highlighted} />
    </Billboard>
  )
}

function Globe() {
  const [earthMap, bumpMap] = useTexture([EARTH_TEXTURE, BUMP_TEXTURE])
  return (
    <>
      <mesh>
        <sphereGeometry args={[GLOBE_RADIUS, 64, 64]} />
        <meshStandardMaterial
          map={earthMap}
          bumpMap={bumpMap}
          bumpScale={0.6}
          roughness={0.85}
          metalness={0.05}
        />
      </mesh>
      <mesh>
        <sphereGeometry args={[GLOBE_RADIUS * 1.04, 48, 48]} />
        <meshBasicMaterial
          color="#5eb0ff"
          transparent
          opacity={0.12}
          side={THREE.BackSide}
        />
      </mesh>
    </>
  )
}

export default function Earth({ animals }) {
  const filters = useStore((s) => s.filters)
  const selected = useStore((s) => s.selected)
  return (
    <>
      <Globe />
      {animals.map((a) => (
        <AnimalSprite
          key={a.id}
          animal={a}
          dim={!matchFilters(a, filters)}
          highlighted={selected?.id === a.id}
        />
      ))}
    </>
  )
}
