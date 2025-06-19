export const isBright = (hex: string) => {
  var hex = hex.substring(1)
  var rgb = parseInt(hex, 16)
  var r = (rgb >> 16) & 0xff
  var g = (rgb >> 8) & 0xff
  var b = (rgb >> 0) & 0xff

  var luma = 0.2126 * r + 0.7152 * g + 0.0722 * b // per ITU-R BT.709

  return luma > 127
}

export function timeAgo(isoDateString: string, currentTime: Date | null = null): string {
  const diffInSeconds = secondsPassed(isoDateString)
  if (isNaN(diffInSeconds)) return 'Invalid date'

  const units = [
    { name: 'year', seconds: 31536000 },
    { name: 'month', seconds: 2592000 },
    { name: 'day', seconds: 86400 },
    { name: 'hour', seconds: 3600 },
    { name: 'minute', seconds: 60 },
    { name: 'second', seconds: 1 },
  ]

  for (const unit of units) {
    const interval = Math.floor(diffInSeconds / unit.seconds)
    if (interval >= 1) {
      return `${interval} ${unit.name}${interval !== 1 ? 's' : ''} ago`
    }
  }

  return 'just now'
}
export function secondsPassed(isoDateString: string, currentTime: Date | null = null): number {
  if (currentTime === null) {
    currentTime = new Date()
  }
  const past = new Date(isoDateString)
  const diffInSeconds = Math.floor((currentTime.getTime() - past.getTime()) / 1000)
  return diffInSeconds
}

export function getBarColor(
  value: number,
  red: number,
  orange: number,
  yellow: number = -1,
  invert = false,
): string {
  if (value === null || value === undefined) {
    return '!grey-500'
  }

  // Define thresholds and their corresponding colors.
  // The order here is important for sorting: from most critical to least critical (or vice-versa if inverted)
  const thresholds = [
    { threshold: red, color: '!bg-red-500' },
    { threshold: orange, color: '!bg-orange-500' },
  ]

  if (yellow !== -1) {
    // Only add yellow if it's a valid threshold
    thresholds.push({ threshold: yellow, color: '!bg-yellow-500' })
  }

  // Sort thresholds based on invert flag
  // If invert is false, we want to check from lowest threshold to highest (e.g., 0-20 red, 20-50 orange, etc.)
  // So, sort ascending by threshold value
  if (!invert) {
    thresholds.sort((a, b) => a.threshold - b.threshold)
  } else {
    // If invert is true, we want to check from highest threshold to lowest (e.g., 100-80 red, 80-50 orange, etc.)
    // So, sort descending by threshold value
    thresholds.sort((a, b) => b.threshold - a.threshold)
  }

  for (const item of thresholds) {
    if ((!invert && value <= item.threshold) || (invert && value >= item.threshold)) {
      return item.color
    }
  }

  // If no threshold is met, it's the "good" color
  return '!bg-green-500'
}
