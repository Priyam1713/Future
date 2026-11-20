import catalog from "./catalog-v1.json";

export const ROOMS = {
  5: ["horary", "Horary", "The Question at Court", "court"],
  6: ["mundane", "Mundane Astrology", "The Almanac of Cycles", "court"],
  7: ["astrocartography", "Astrocartography", "The Meridian Atlas", "court"],
  8: ["palmistry", "Palmistry", "The Hand in Ink", "manuscript"],
  9: ["face-reading", "Face Reading", "The Portrait Index", "manuscript"],
  10: ["phrenology", "Phrenology", "The Numbered Plates", "manuscript"],
  11: ["moleosophy", "Moleosophy", "Fontaine’s Marginalia", "manuscript"],
  12: ["podomancy", "Podomancy", "The Sole Folio", "manuscript"],
  13: ["graphology", "Graphology", "The Script Cabinet", "manuscript"],
  14: ["aura", "Aura", "The Colour Lantern", "manuscript"],
  15: ["iridology", "Iridology", "The Lindlahr Plates", "manuscript"],
  40: ["compass", "Feng Shui", "The Compass Chamber", "compass"],
} as const;
export const ENVIRONMENTS = {
  court: "Celestial Court",
  manuscript: "Human Manuscript",
  compass: "Compass Chamber",
};
export type Id = keyof typeof ROOMS;
export type ArchiveId = Exclude<Id, 5 | 6 | 7 | 40>;
export type BookmarkId = ArchiveId | 40;
export type Slug = (typeof ROOMS)[Id][0];
export const ids = Object.keys(ROOMS).map(Number) as Id[];
export function isRoom(id: number): id is Id {
  return Object.hasOwn(ROOMS, id);
}
export function roomId(slug: string) {
  return ids.find((id) => ROOMS[id][0] === slug);
}
export type View = {
  title: string;
  status: string;
  lead: string;
  sources: { text: string; locator: string; sourceId: string; url: string }[];
};
export type Bookmark = {
  oracle: BookmarkId;
  profile: "fate-manuscript-reference-v1";
  entries: string[];
};
export const EDITION = "fate-manuscript-reference-v1";
export const mountains = catalog.mountains;
export const options = catalog.options as Record<
  BookmarkId,
  [string, string, string][]
>;
export function isBookmark(s: { oracle: number }): s is Bookmark {
  return isRoom(s.oracle) && s.oracle >= 8;
}
export function validateBookmark(s: Record<string, unknown>): s is Bookmark {
  if (
    Object.keys(s).length !== 3 ||
    typeof s.oracle !== "number" ||
    !isBookmark({ oracle: s.oracle }) ||
    s.profile !== EDITION ||
    !Array.isArray(s.entries)
  )
    return false;
  const allowed = options[s.oracle as BookmarkId];
  return (
    s.entries.length >= 1 &&
    s.entries.length <= (s.oracle === 40 ? 24 : 1) &&
    new Set(s.entries).size === s.entries.length &&
    s.entries.every((key: unknown) => allowed.some(([id]) => id === key))
  );
}

export type NativeResult = { [key: string]: unknown; technique_id: number };
export type Envelope<T extends NativeResult = NativeResult> = {
  result: T;
  view?: View;
  reference?: string;
  mountainViews?: View[];
  references?: string[];
};
