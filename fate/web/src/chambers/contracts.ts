import edition from "./edition-v1.json";
import { isSignId, SIGNS } from "../signs/contracts";
import { isRitualId, RITUAL_ROOMS } from "../ritual/contracts";

export const CHAMBER_REFERENCE = "fate-four-chambers-v1";
export const ROOMS = {
  2: {
    slug: "vedic",
    name: "Vedic Astrology",
    title: "The Navagraha Observatory",
    index: "Sidereal charts & lunar periods",
    prompt:
      "Trace the nine grahas through the sidereal sky, then follow the Moon’s birth star into the Vimshottari periods.",
  },
  3: {
    slug: "bazi",
    name: "Chinese BaZi",
    title: "The Jade Hall",
    index: "Four Pillars & the Day Master",
    prompt:
      "Open four jade pillars for your recorded birth moment. The day stem anchors a reading of elements and their relationships.",
  },
  18: {
    slug: "iching",
    name: "I Ching",
    title: "The Book of Changes",
    index: "Three coins & six lines",
    prompt:
      "Cast three coins for each line. Read the figure from the bottom up, then watch its changing lines reveal a second perspective.",
  },
  19: {
    slug: "runes",
    name: "Runes",
    title: "The Runestone Clearing",
    index: "Elder Futhark · one or three",
    prompt:
      "Turn a stone to read a sign from the Elder Futhark. Explore its historical record and a modern reflection beside it.",
  },
} as const;
export type ChamberId = keyof typeof ROOMS;
export type ChamberSlug = (typeof ROOMS)[ChamberId]["slug"];
const ids = [2, 3, 18, 19] as const;
export function isChamberId(id: number): id is ChamberId {
  return ids.some((value) => value === id);
}
export function chamberId(slug: string) {
  return ids.find((id) => ROOMS[id].slug === slug);
}
export type Period = [lord: string, start: string, end: string];
export type VedicSnapshot = {
  oracle: 2;
  profile: "parashari-core-lahiri1956-mean-node";
  asc: [number, number];
  d9Asc: [number, number];
  planets: [number, number, number, number, number, number][];
  mansion: [index: number, pada: number, sensitive: boolean];
  year: "pvr-2000-savana" | "solar-365.2425";
  main: Period[];
  sub: Period[];
  active: number;
};
export type BaziSnapshot = {
  oracle: 3;
  profile: "civil-zi23" | "civil-split-zi" | "standard-zi23";
  pairs: [number, number, number, number];
};
export type CoinSnapshot = {
  oracle: 18;
  profile: "legge-1882-scan-text-v1";
  values: number[];
  figures: [number, number];
};
export type RuneSnapshot = {
  oracle: 19;
  profile: "elder24-page-facts-snapshot-v1";
  runes: string[];
};
export type ChamberSnapshot =
  | VedicSnapshot
  | BaziSnapshot
  | CoinSnapshot
  | RuneSnapshot;
export function isChamberSnapshot(s: { oracle: number }): s is ChamberSnapshot {
  return isChamberId(s.oracle);
}
export function oracleLabel(id: number) {
  if (isSignId(id)) return SIGNS[id].name;
  if (isRitualId(id)) return RITUAL_ROOMS[id].name;
  return isChamberId(id)
    ? ROOMS[id].name
    : id === 1
      ? "Astrology"
      : id === 16
        ? "Tarot"
        : "Numerology";
}
export type ChamberEnvelope = {
  snapshot: ChamberSnapshot;
  result: {
    technique_id: ChamberId;
    limitations?: string[];
    replay?: { casting?: { raw: number[][] } };
  };
  receipt: string;
};
export function validChamber(s: Record<string, unknown>): s is ChamberSnapshot {
  const keys = (...names: string[]) =>
    Object.keys(s).length === names.length + 2 &&
    names.every((key) => Object.hasOwn(s, key));
  const integer = (value: unknown, min: number, max: number) =>
    typeof value === "number" &&
    Number.isInteger(value) &&
    value >= min &&
    value <= max;
  const longitude = (value: unknown) =>
    typeof value === "number" &&
    Number.isFinite(value) &&
    value >= 0 &&
    value < 360;
  const array = (x: unknown, n: number): x is unknown[] =>
    Array.isArray(x) && x.length === n;
  const utcDay = (x: unknown): x is string =>
    typeof x === "string" &&
    /^\d{4}-\d{2}-\d{2}$/.test(x) &&
    Number.isFinite(Date.parse(x)) &&
    new Date(x).toISOString().slice(0, 10) === x;
  const periods = (rows: unknown, n: number) =>
    array(rows, n) &&
    rows.every(
      (row, i) =>
        array(row, 3) &&
        typeof row[0] === "string" &&
        edition.lords.includes(row[0]) &&
        utcDay(row[1]) &&
        utcDay(row[2]) &&
        row[1] <= row[2] &&
        (!i || (rows[i - 1] as Period)[2] === row[1]),
    );
  if (s.oracle === 2) {
    const point = (p: unknown) =>
      array(p, 2) && longitude(p[0]) && integer(p[1], 0, 11);
    return (
      s.profile === edition.profiles["2"] &&
      keys(
        "asc",
        "d9Asc",
        "planets",
        "mansion",
        "year",
        "main",
        "sub",
        "active",
      ) &&
      point(s.asc) &&
      point(s.d9Asc) &&
      array(s.planets, 9) &&
      s.planets.every(
        (row) =>
          array(row, 6) &&
          longitude(row[0]) &&
          integer(row[1], 0, 11) &&
          integer(row[2], 1, 12) &&
          longitude(row[3]) &&
          integer(row[4], 0, 11) &&
          integer(row[5], 1, 12),
      ) &&
      array(s.mansion, 3) &&
      integer(s.mansion[0], 0, 26) &&
      integer(s.mansion[1], 1, 4) &&
      typeof s.mansion[2] === "boolean" &&
      typeof s.year === "string" &&
      ["pvr-2000-savana", "solar-365.2425"].includes(s.year) &&
      periods(s.main, 10) &&
      periods(s.sub, 9) &&
      integer(s.active, 0, 8)
    );
  }
  if (s.oracle === 3)
    return (
      typeof s.profile === "string" &&
      edition.profiles["3"].includes(s.profile) &&
      keys("pairs") &&
      array(s.pairs, 4) &&
      s.pairs.every((i) => integer(i, 0, 59))
    );
  if (s.oracle === 18) {
    const values = s.values,
      figures = s.figures;
    if (
      s.profile !== edition.profiles["18"] ||
      !keys("values", "figures") ||
      !array(values, 6) ||
      !values.every((i) => integer(i, 6, 9)) ||
      !array(figures, 2) ||
      !figures.every((i) => integer(i, 1, 64))
    )
      return false;
    return figures.every((id, state) =>
      edition.patterns[Number(id) - 1].every((bit, i) => {
        const value = Number(values[i]);
        return (
          bit ===
          (state && (value === 6 || value === 9) ? 1 - (value % 2) : value % 2)
        );
      }),
    );
  }
  return (
    s.oracle === 19 &&
    s.profile === edition.profiles["19"] &&
    keys("runes") &&
    Array.isArray(s.runes) &&
    (s.runes.length === 1 || s.runes.length === 3) &&
    new Set(s.runes).size === s.runes.length &&
    s.runes.every(
      (id) => typeof id === "string" && edition.runeIds.includes(id),
    )
  );
}
