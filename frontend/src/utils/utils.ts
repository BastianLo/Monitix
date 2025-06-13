export const isBright = (hex: string) => {
    var hex = hex.substring(1);
    var rgb = parseInt(hex, 16);
    var r = (rgb >> 16) & 0xff;
    var g = (rgb >> 8) & 0xff;
    var b = (rgb >> 0) & 0xff;

    var luma = 0.2126 * r + 0.7152 * g + 0.0722 * b; // per ITU-R BT.709

    return luma > 127
}

export function timeAgo(isoDateString: string): string {
  const diffInSeconds = secondsPassed(isoDateString);
  if (isNaN(diffInSeconds)) return "Invalid date";

  const units = [
    { name: "year", seconds: 31536000 },
    { name: "month", seconds: 2592000 },
    { name: "day", seconds: 86400 },
    { name: "hour", seconds: 3600 },
    { name: "minute", seconds: 60 },
    { name: "second", seconds: 1 },
  ];

  for (const unit of units) {
    const interval = Math.floor(diffInSeconds / unit.seconds);
    if (interval >= 1) {
      return `${interval} ${unit.name}${interval !== 1 ? "s" : ""} ago`;
    }
  }

  return "just now";
}
export function secondsPassed(isoDateString: string): number {
  const now = new Date();
  const past = new Date(isoDateString);
  const diffInSeconds = Math.floor((now.getTime() - past.getTime()) / 1000);
  return diffInSeconds
}

