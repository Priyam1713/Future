import edition from "./edition-v1.json";

export const RITUAL_REFERENCE = "fate-ritual-wing-v1";
export const RITUAL_ROOMS = {
  17: {
    slug: "oracle",
    name: "Oracle Cards",
    title: "The Cabinet of Signs",
    prompt:
      "Choose one, three, or five cards from the illustrated Lenormand collection.",
  },
  20: {
    slug: "pendulum",
    name: "Pendulum",
    title: "The Suspended Hour",
    prompt:
      "Explore a digital symbol or record the movement of a pendulum you observed yourself.",
  },
  21: {
    slug: "crystal",
    name: "Crystal Ball",
    title: "The Veil of Glass",
    prompt:
      "Rest your attention on the crystal. Record what you noticed, or leave the page empty.",
  },
  22: {
    slug: "mirror",
    name: "Mirror Scrying",
    title: "The Obsidian Gallery",
    prompt:
      "Look into the moving light, then put your own observations into words if you wish.",
  },
  23: {
    slug: "dream",
    name: "Dream Interpretation",
    title: "The House of Night",
    prompt:
      "Keep a fragment of your dream in this visit and choose which motifs to look up in Artemidorus.",
  },
  33: {
    slug: "geomancy",
    name: "Geomancy",
    title: "The Sand Court",
    prompt:
      "Set the four Mothers, row by row, and follow how the fifteen figures of the shield are formed.",
  },
  36: {
    slug: "bibliomancy",
    name: "Bibliomancy",
    title: "The Lantern Library",
    prompt:
      "Turn the pages of the pinned Ruth edition and choose a sentence to read in context.",
  },
} as const;
export type RitualId = keyof typeof RITUAL_ROOMS;
export type RitualSlug = (typeof RITUAL_ROOMS)[RitualId]["slug"];
const ids = [17, 20, 21, 22, 23, 33, 36] as const;
export function ritualId(slug: string) {
  return ids.find((id) => RITUAL_ROOMS[id].slug === slug);
}
export function isRitualId(id: number): id is RitualId {
  return ids.some((room) => id === room);
}
export type RitualSnapshot = {
  oracle: RitualId;
  profile: string;
  values: string[];
};
export function isRitualSnapshot(s: { oracle: number }): s is RitualSnapshot {
  return isRitualId(s.oracle);
}

export type GeomanticPosition = {
  position: number;
  role: string;
  pattern: string;
  rows: number[];
  parents: number[];
  operation: string;
  line_trace: {
    row?: number;
    parent?: number;
    parent_row?: number;
    dot_count?: number;
    inputs?: number[];
    sum?: number;
    result?: number;
  }[];
};
export type DreamCase = {
  id: string;
  historical_account: string;
  requires: Record<string, unknown>;
};
export type DreamReference = {
  motif_id: string;
  status: string;
  missing_context: string[];
  selected_cases: DreamCase[];
  reference: {
    definition: string;
    provenance: { locator: string };
    cases: DreamCase[];
  };
};
export type Passage = {
  sentence_id: string;
  text: string;
  citation: string;
  source_url: string;
};
export type RitualNative = {
  technique_id: number;
  profile: string;
  summary?: { text: string };
  outcome?: {
    symbolic_response: string;
    reasons: string[];
    resolved: boolean;
    conflicting: boolean;
  };
  reflection?: { text: string };
  journal?: unknown;
  journal_state?: string;
  motif_references?: DreamReference[];
  positions?: GeomanticPosition[];
  selections?: (Passage & {
    context_before: Passage[];
    context_after: Passage[];
  })[];
  limitations?: string[];
};
export type RitualEnvelope = { snapshot: RitualSnapshot; result: RitualNative };

export function validateRitual(
  s: Record<string, unknown>,
): s is RitualSnapshot {
  const { oracle, profile, values } = s;
  if (
    typeof oracle !== "number" ||
    !isRitualId(oracle) ||
    Object.keys(s).length !== 3 ||
    profile !==
      edition.profiles[String(oracle) as keyof typeof edition.profiles] ||
    !Array.isArray(values) ||
    !values.every((v) => typeof v === "string")
  )
    return false;
  const unique = new Set(values).size === values.length;
  switch (oracle) {
    case 17:
      return (
        [1, 3, 5].includes(values.length) &&
        unique &&
        values.every((id) => edition.cards.includes(id))
      );
    case 20:
      return (
        values.length === 2 &&
        ["manual", "seeded"].includes(values[0]) &&
        ["yes", "no", "unresolved"].includes(values[1])
      );
    case 21:
    case 22:
      return values.length === 0;
    case 23:
      return unique && values.every((id) => edition.motifs.includes(id));
    case 33:
      return (
        values.length === 15 &&
        values.every((v) => /^[12]{4}$/.test(v)) &&
        values.slice(4, 8).every(
          (p, i) =>
            p ===
            values
              .slice(0, 4)
              .map((m) => m[i])
              .join(""),
        ) &&
        edition.parents.every(
          ([a, b], i) =>
            values[i + 8] ===
            Array.from(values[a - 1] as string, (digit, j) =>
              (Number(digit) + Number(values[b - 1][j])) % 2 ? "1" : "2",
            ).join(""),
        )
      );
    case 36:
      return (
        values.length >= 2 &&
        values.length <= 33 &&
        ["0", "1", "2"].includes(values[0]) &&
        values.slice(1).every((id) => edition.sentences.includes(id))
      );
  }
}
