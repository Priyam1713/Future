import catalog from "./narrative-reference-v1.json";

export const NARRATIVE_EDITIONS = {
  1: "fate-western-natal-v1",
  2: "fate-jyotish-v1",
  3: "fate-bazi-reading-v1",
} as const;
export type NarrativeTechnique = keyof typeof NARRATIVE_EDITIONS;
type Edition = (typeof NARRATIVE_EDITIONS)[NarrativeTechnique];
export type Passage = {
  title: string;
  text: string;
  coverage: "direct" | "compositional";
  rules: string[];
};
export type ReadingSection = { id: string; title: string; passages: Passage[] };
export type Narrative = { technique: NarrativeTechnique; edition: Edition; sections: ReadingSection[] };
type RuleReference = { url: string; locator: string; edition: string; text: string; exceptions: string[] };

export const NARRATIVE_SECTIONS = {
  1: ["identity", "emotion", "communication", "work", "themes", "aspects", "chart-details"],
  2: ["lagna", "lunar", "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu", "periods"],
  3: ["day-master", "year", "month", "day", "hour"],
} as const;

export const narrativeScope = {
  1: "The natal reading uses the selected tropical house system and the pinned source edition. Its symbolic passages leave event outcomes and unsupported pair meanings open.",
  2: "Rashi and Navamsa describe separate symbolic frames. Period topics refer to their lords and natal houses. Calendar dates and UTC boundaries stay in the live reading.",
  3: "The clock convention and Four Pillars anchor the reading. Fixed hidden-stem membership and directional element relationships leave seasonal strength, transformations and luck timing open.",
};

export function narrativeRule(edition: Edition, id: string): RuleReference | undefined {
  const rules: Record<string, RuleReference> = catalog[edition];
  return Object.hasOwn(rules, id) ? rules[id] : undefined;
}

function exactObject(value: unknown, keys: string[]): value is Record<string, unknown> {
  return !!value && typeof value === "object" && !Array.isArray(value) &&
    Object.keys(value).length === keys.length && keys.every((key) => Object.hasOwn(value, key));
}

const prose = (value: unknown, limit: number): value is string =>
  typeof value === "string" && value.trim().length > 0 && value.length <= limit &&
  !/[\u0000-\u001f\u007f<>]/u.test(value);

export function validNarrative(value: unknown, oracle: number): value is Narrative {
  if (!exactObject(value, ["technique", "edition", "sections"]) ||
      (oracle !== 1 && oracle !== 2 && oracle !== 3) ||
      value.technique !== oracle || value.edition !== NARRATIVE_EDITIONS[oracle] ||
      !Array.isArray(value.sections)) return false;
  const order: readonly string[] = NARRATIVE_SECTIONS[oracle];
  const edition = NARRATIVE_EDITIONS[oracle];
  if (!value.sections.length || value.sections.length > order.length ||
      (oracle !== 1 && value.sections.length !== order.length)) return false;
  let previous = -1;
  return value.sections.every((section) => {
    if (!exactObject(section, ["id", "title", "passages"]) ||
        typeof section.id !== "string" || !prose(section.title, 100) ||
        !Array.isArray(section.passages) || !section.passages.length ||
        section.passages.length > 45) return false;
    const position = order.indexOf(section.id);
    if (position <= previous) return false;
    previous = position;
    return section.passages.every((passage) =>
      exactObject(passage, ["title", "text", "coverage", "rules"]) &&
      prose(passage.title, 120) && prose(passage.text, 1800) &&
      (passage.coverage === "direct" || passage.coverage === "compositional") &&
      Array.isArray(passage.rules) && passage.rules.length > 0 && passage.rules.length <= 8 &&
      new Set(passage.rules).size === passage.rules.length &&
      passage.rules.every((id) => typeof id === "string" && !!narrativeRule(edition, id)) &&
      (passage.coverage !== "direct" || (passage.rules.length === 1 &&
        narrativeRule(edition, passage.rules[0])?.text === passage.text))
    );
  });
}
