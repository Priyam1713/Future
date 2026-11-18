export type Quality = "cinematic" | "balanced" | "economy" | "low";
export const QUALITY = {
  cinematic: { dpr: 1.75, fps: 60, detail: 1, particles: 36 },
  balanced: { dpr: 1.25, fps: 60, detail: 1, particles: 24 },
  economy: { dpr: 1, fps: 60, detail: 0, particles: 18 },
  low: { dpr: 1, fps: 30, detail: 0, particles: 12 },
} as const;
export function initialQuality(): Quality {
  const device = navigator as Navigator & {
    deviceMemory?: number;
    connection?: { saveData?: boolean };
  };
  if (
    device.connection?.saveData ||
    (device.deviceMemory !== undefined && device.deviceMemory <= 4) ||
    (device.hardwareConcurrency > 0 && device.hardwareConcurrency <= 4)
  )
    return "low";
  return "cinematic";
}
export function resolutionFor(width: number, quality: Quality) {
  // Allocate pixels for the displayed size, never a fixed oversized phone buffer.
  return Math.max(
    0.35,
    Math.min(
      1.6,
      (Math.min(devicePixelRatio, QUALITY[quality].dpr) *
        Math.min(width, 600)) /
        600,
    ),
  );
}
export function percentile(samples: number[], fraction: number) {
  const sorted = [...samples].sort((a, b) => a - b);
  return (
    sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * fraction))] ??
    0
  );
}
