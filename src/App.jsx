import { Suspense, useMemo, useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import Earth from './components/Earth.jsx'
import Weather from './components/Weather.jsx'
import Plants from './components/Plants.jsx'
import AnimalCard from './components/AnimalCard.jsx'
import WeatherControls from './components/WeatherControls.jsx'
import FilterControls from './components/FilterControls.jsx'
import CameraRig, { HOME_DISTANCE } from './components/CameraRig.jsx'
import { ZoomTracker, MIN_DIST, MAX_DIST } from './components/ZoomBadge.jsx'
import animals from './data/animals.json'
import { useStore, matchFilters } from './store/useStore.js'

export default function App() {
  const orbitRef = useRef()
  const zoomRef = useRef()
  const filters = useStore((s) => s.filters)
  const selected = useStore((s) => s.selected)
  const showPlants = useStore((s) => s.showPlants)
  const togglePlants = useStore((s) => s.togglePlants)
  const matchCount = useMemo(
    () => animals.filter((a) => matchFilters(a, filters)).length,
    [filters],
  )

  return (
    <div className="app">
      <div className="title">
        <h1>如果地球是一座动物园</h1>
        <p>
          {matchCount} / {animals.length} 种动物 · 真实栖息地
        </p>
      </div>

      <div className="top-right">
        <div className="zoom-badge">
          <span ref={zoomRef}>100%</span>
        </div>
        <button
          className={`tr-btn ${showPlants ? 'on' : ''}`}
          onClick={togglePlants}
          title="切换植物剪影"
        >
          🌿 植物
        </button>
      </div>

      <Canvas
        camera={{ position: [0, 0, HOME_DISTANCE], fov: 50, near: 0.1, far: 2000 }}
        gl={{ antialias: true, alpha: false }}
      >
        <color attach="background" args={['#02030a']} />
        <ambientLight intensity={0.6} />
        <directionalLight position={[100, 50, 100]} intensity={1.2} />
        <Stars radius={600} depth={120} count={6000} factor={4} fade speed={0.6} />
        <Suspense fallback={null}>
          <Earth animals={animals} />
          <Plants />
        </Suspense>
        <Weather />
        <OrbitControls
          ref={orbitRef}
          enablePan={false}
          minDistance={MIN_DIST}
          maxDistance={MAX_DIST}
          autoRotate={!selected}
          autoRotateSpeed={0.25}
          rotateSpeed={0.5}
          zoomSpeed={0.8}
        />
        <CameraRig orbitRef={orbitRef} />
        <ZoomTracker valueRef={zoomRef} />
      </Canvas>

      <AnimalCard />
      <FilterControls />
      <WeatherControls />
      <div className="hint">拖拽旋转 · 滚轮缩放 · 点击动物飞行查看</div>
    </div>
  )
}
