let currentAudio = null
let currentId = null

export function playSound(id, ext, onEnd) {
  if (!ext) return false
  const url = `/sounds/${id}.${ext}`
  if (currentAudio && currentId === id && !currentAudio.paused) {
    currentAudio.pause()
    currentAudio.currentTime = 0
    currentAudio = null
    currentId = null
    return false
  }
  if (currentAudio) {
    currentAudio.pause()
    currentAudio.currentTime = 0
  }
  const audio = new Audio(url)
  audio.volume = 0.85
  // 播放自然结束时复位模块状态,并通知调用方(否则 playing 状态永不复位)
  audio.addEventListener('ended', () => {
    // 只在仍是当前音频时清状态,避免误清后来切换的新音频
    if (currentAudio === audio) {
      currentAudio = null
      currentId = null
    }
    if (onEnd) onEnd()
  })
  audio.play().catch((err) => {
    console.warn('audio play failed:', err)
  })
  currentAudio = audio
  currentId = id
  return true
}

export function stopSound() {
  if (currentAudio) {
    currentAudio.pause()
    currentAudio.currentTime = 0
    currentAudio = null
    currentId = null
  }
}
