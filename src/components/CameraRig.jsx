import { useEffect, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { useStore } from '../store/useStore.js'
import { lonLatToVec3 } from './Earth.jsx'

const HOME_DISTANCE = 280
const FLY_DISTANCE = 175

export default function CameraRig({ orbitRef }) {
  const { camera } = useThree()
  const selected = useStore((s) => s.selected)
  const target = useRef(null)
  const tStart = useRef(0)

  useEffect(() => {
    const oc = orbitRef.current
    if (!oc) return
    if (selected) {
      const [x, y, z] = lonLatToVec3(selected.lon, selected.lat, FLY_DISTANCE)
      target.current = new THREE.Vector3(x, y, z)
      oc.enabled = false
      oc.autoRotate = false
      tStart.current = performance.now()
    } else {
      target.current = null
      oc.enabled = true
      oc.autoRotate = true
    }
  }, [selected, orbitRef])

  useFrame(() => {
    if (!target.current) return
    const t = (performance.now() - tStart.current) / 1200
    const k = Math.min(1, t)
    const ease = 1 - Math.pow(1 - k, 3)
    camera.position.lerp(target.current, 0.08 * (1 + ease))
    camera.lookAt(0, 0, 0)
    if (k >= 1 && camera.position.distanceTo(target.current) < 0.5) {
      const oc = orbitRef.current
      if (oc) {
        oc.enabled = true
        oc.autoRotate = false
        oc.update()
      }
      target.current = null
    }
  })

  return null
}

export { HOME_DISTANCE, FLY_DISTANCE }
