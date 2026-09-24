import { create } from 'zustand'

const DEFAULT_FILTERS = {
  region: '全部',
  class: '全部',
  habitat: '全部',
  status: '全部',
}

export const useStore = create((set) => ({
  selected: null,
  setSelected: (animal) => set({ selected: animal, autoRotate: false }),
  clearSelected: () => set({ selected: null, autoRotate: true }),

  weather: { rain: false, snow: false, wind: false, sand: false },
  toggleWeather: (key) =>
    set((s) => ({ weather: { ...s.weather, [key]: !s.weather[key] } })),

  filters: { ...DEFAULT_FILTERS },
  setFilter: (key, value) =>
    set((s) => ({ filters: { ...s.filters, [key]: value } })),
  resetFilters: () => set({ filters: { ...DEFAULT_FILTERS } }),

  autoRotate: true,
  setAutoRotate: (v) => set({ autoRotate: v }),

  showPlants: true,
  togglePlants: () => set((s) => ({ showPlants: !s.showPlants })),
}))

export function matchFilters(animal, filters) {
  if (filters.region !== '全部' && animal.region !== filters.region) return false
  if (filters.class !== '全部' && animal.class !== filters.class) return false
  if (filters.habitat !== '全部' && animal.habitat !== filters.habitat) return false
  if (filters.status !== '全部' && animal.status !== filters.status) return false
  return true
}
