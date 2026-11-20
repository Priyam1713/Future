import edition from "./edition-v1.json";

export const SIGN_REFERENCE = "fate-world-of-signs-v1";
export const SIGNS = {
  28: {
    slug: "tea-leaves",
    name: "Tasseography",
    title: "The Tea Leaf Cup",
    stage: "table",
    prompt:
      "Mark the part of the cup where you noticed a shape, then choose the shape yourself.",
    action: "Read my cup marks",
  },
  29: {
    slug: "coffee-grounds",
    name: "Coffee Grounds",
    title: "The Coffee Saucer",
    stage: "table",
    prompt:
      "Choose the vessel you examined and name the grounds you identified.",
    action: "Compare my grounds",
  },
  30: {
    slug: "candle-lore",
    name: "Pyromancy",
    title: "The Candle Lens",
    stage: "elemental",
    prompt:
      "Compare a past record or a hypothetical flame with the published conditions. The display uses no physical flame.",
    action: "Compare the flame record",
  },
  31: {
    slug: "water-signs",
    name: "Hydromancy",
    title: "The Water Basin",
    stage: "elemental",
    prompt:
      "Place your observation within its own context, from reflections to subjective imagery.",
    action: "Open the water reference",
  },
  32: {
    slug: "weather-lore",
    name: "Aeromancy",
    title: "The Wind Dial",
    stage: "elemental",
    prompt:
      "Mark a direction you observed and compare it with its regional weather-lore account.",
    action: "Compare my sky note",
  },
  34: {
    slug: "stone-table",
    name: "Lithomancy",
    title: "The Stone Plan",
    stage: "table",
    prompt:
      "Keep the lodestone at the center, then place one chosen stone at its observed relative position.",
    action: "Read my stone placement",
  },
  35: {
    slug: "bone-archive",
    name: "Osteomancy",
    title: "The Inscription Archive",
    stage: "omens",
    prompt:
      "Open a published Shang case or compare a documented pair of charges.",
    action: "Open the documentary record",
  },
  37: {
    slug: "letter-lot",
    name: "Cleromancy",
    title: "The Letter Cabinet",
    stage: "table",
    prompt:
      "Select the Greek letter you already have or explicitly choose an example for study.",
    action: "Open this letter account",
  },
  38: {
    slug: "bird-signs",
    name: "Augury",
    title: "The Bird-Sign Loggia",
    stage: "omens",
    prompt:
      "Declare a bird label, behavior and side relative to you, then compare the Cicero source accounts.",
    action: "Compare my bird record",
  },
  39: {
    slug: "roman-cases",
    name: "Haruspicy",
    title: "The Roman Casebook",
    stage: "omens",
    prompt:
      "Compare details from a written account with the Roman references. This is a documentary exercise.",
    action: "Compare the written account",
  },
} as const;
export const ENVIRONMENTS = {
  table: "Divination Table",
  elemental: "Elemental Observatory",
  omens: "Chamber of Omens",
};
export type SignId = keyof typeof SIGNS;
export type SignSlug = (typeof SIGNS)[SignId]["slug"];
export const SIGN_IDS = [28, 29, 30, 31, 32, 34, 35, 37, 38, 39] as const;
export function signId(slug: string) {
  return SIGN_IDS.find((id) => SIGNS[id].slug === slug);
}
export function isSignId(id: number): id is SignId {
  return SIGN_IDS.some((key) => key === id);
}
export type SignSnapshot = {
  oracle: SignId;
  profile: string;
  values: string[];
};
export function isSign(s: { oracle: number }): s is SignSnapshot {
  return isSignId(s.oracle);
}

type Field = { label: string; options: string[][] };
const schema = {
  fields: edition.fields as Record<string, Field[]>,
  profiles: edition.profiles as Record<string, string>,
};
const air = edition.air as Record<string, Record<string, string>>;
export function fields(id: SignId) {
  return schema.fields[id];
}
export function options(id: SignId, index: number, values: string[]) {
  if (id === 32 && index === 1) return Object.entries(air[values[0]] ?? {});
  return fields(id)[index].options;
}
export function validValues(id: SignId, values: string[]) {
  return (
    values.length === fields(id).length &&
    values.every((value, i) =>
      options(id, i, values).some(([v]) => v === value),
    )
  );
}
export function validateSign(s: Record<string, unknown>): s is SignSnapshot {
  return (
    Object.keys(s).length === 3 &&
    typeof s.oracle === "number" &&
    isSignId(s.oracle) &&
    s.profile === schema.profiles[s.oracle] &&
    Array.isArray(s.values) &&
    s.values.every((value) => typeof value === "string") &&
    validValues(s.oracle, s.values) &&
    !(s.oracle === 30 && s.values[2] === "hazard")
  );
}
export type SignView = {
  status: string;
  lead: string;
  metric: { distanceSquared: number; direction: string[] } | null;
  excerpts: {
    text: string;
    locator: string;
    url: string | null;
    sourceId: string;
    status: string;
  }[];
};
export type SignEnvelope = {
  result: object;
  view: SignView;
  snapshot: SignSnapshot | null;
};
export function choicesTitle(s: { oracle: SignId; values: string[] }) {
  const selected = (i: number) =>
    options(s.oracle, i, s.values).find(([id]) => id === s.values[i])?.[1] ??
    "";
  return s.oracle === 28 || s.oracle === 29
    ? selected(1)
    : s.oracle === 38
      ? selected(0) + " · " + selected(2)
      : selected(0);
}
