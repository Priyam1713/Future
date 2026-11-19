export const BODY_NAMES = [
  "Sun",
  "Moon",
  "Mercury",
  "Venus",
  "Mars",
  "Jupiter",
  "Saturn",
  "Uranus",
  "Neptune",
  "Pluto",
] as const;
export const SIGNS = [
  "Aries",
  "Taurus",
  "Gemini",
  "Cancer",
  "Leo",
  "Virgo",
  "Libra",
  "Scorpio",
  "Sagittarius",
  "Capricorn",
  "Aquarius",
  "Pisces",
];
export const GLYPHS = ["☉", "☽", "☿", "♀", "♂", "♃", "♄", "♅", "♆", "♇"];
export const SIGN_GLYPHS = [
  "♈",
  "♉",
  "♊",
  "♋",
  "♌",
  "♍",
  "♎",
  "♏",
  "♐",
  "♑",
  "♒",
  "♓",
];
export const WESTERN_REFERENCE = "fate-western-reference-v1";
export type Houses =
  | "whole-sign"
  | "equal"
  | "porphyry"
  | "placidus"
  | "regiomontanus"
  | "campanus";
export interface WesternInput {
  local: string;
  zone: string;
  latitude: number;
  longitude: number;
  houses: Houses;
  fold: 0 | 1 | null;
}
export interface Planet {
  longitude: number;
  retrograde: boolean;
  house: number;
  sign: string;
  degree_in_sign: number;
  speed_degrees_per_day: number;
}
export interface Aspect {
  bodies: string[];
  angle: number;
  separation: number;
  orb: number;
}
export interface Component {
  id: string;
  version: number;
  tradition: string;
  text: string;
  url: string;
  author: string;
  locator: string;
  exceptions: string[];
}
export interface PlacementReading {
  planet: string;
  sign: string;
  house: number;
  coverage: string;
  components: Component[];
  missing_components: string[];
}
export interface Geometry {
  angles: { ascendant: number; midheaven: number };
  house_cusps: number[];
  planets: Record<string, Pick<Planet, "longitude" | "retrograde" | "house">>;
  aspects: Aspect[];
}
export interface WesternResult extends Geometry {
  technique_id: 1;
  settings: {
    houses: Houses;
    tradition: string;
    zodiac: string;
    rulership: string;
  };
  planets: Record<string, Planet>;
  birth: {
    local: string;
    zone: string;
    utc: string;
    latitude: number;
    longitude: number;
  };
  reading: {
    placements: PlacementReading[];
    aspects: {
      bodies: string[];
      angle: number;
      orb: number;
      components: Component[];
      direct_pair_coverage: string;
    }[];
    scope: string;
  };
  limitations: string[];
  conventions: unknown;
  reproducibility: unknown;
}
export interface WesternEnvelope {
  oracle_id: 1;
  result: WesternResult;
  receipt: string;
}
export interface WesternCommentary {
  themes: { id: string; reflection: string }[];
  provenance: { provider: string; model: string };
  coverage: string;
}
export interface WesternSnapshot {
  oracle: 1;
  profile: "modern-tropical-v1";
  houses: Houses;
  planets: [number, boolean, number][];
  angles: [number, number];
  cusps: number[];
  aspects: Aspect[];
}
export const signAt = (longitude: number) => SIGNS[Math.floor(longitude / 30)];
export const degree = (longitude: number) =>
  `${(Math.floor((longitude % 30) * 100) / 100).toFixed(2)}° ${signAt(longitude)}`;
export function westernSnapshot(r: WesternResult): WesternSnapshot {
  return {
    oracle: 1,
    profile: "modern-tropical-v1",
    houses: r.settings.houses,
    planets: BODY_NAMES.map((n) => [
      r.planets[n].longitude,
      r.planets[n].retrograde,
      r.planets[n].house,
    ]),
    angles: [r.angles.ascendant, r.angles.midheaven],
    cusps: [...r.house_cusps],
    aspects: r.aspects.map((a) => ({
      bodies: [...a.bodies],
      angle: a.angle,
      separation: a.separation,
      orb: a.orb,
    })),
  };
}
export function snapshotGeometry(s: WesternSnapshot): Geometry {
  return {
    angles: { ascendant: s.angles[0], midheaven: s.angles[1] },
    house_cusps: s.cusps,
    planets: Object.fromEntries(
      BODY_NAMES.map((n, i) => [
        n,
        {
          longitude: s.planets[i][0],
          retrograde: s.planets[i][1],
          house: s.planets[i][2],
        },
      ]),
    ),
    aspects: s.aspects,
  };
}
