/** Degrees are ecliptic longitude, increasing counter-clockwise; Ascendant is left. */
export const point = (lon: number, r: number, origin: number) => {
  const a = ((180 + (lon - origin)) * Math.PI) / 180;
  return { x: 300 + r * Math.cos(a), y: 300 - r * Math.sin(a) };
};
