import archive from "../codex/reference-v1.json";
import type { Card, Meaning } from "../types";

export const TAROT_EDITION = "fate-waite-connected-v1";
export const TAROT_PROFILE = "waite-1922-text-v1";
export const spreadPositions = ["What you carry", "Where you stand", "What to consider"] as const;
export const tarotSections = ["overview", "position-1", "position-2", "position-3", "relationships", "closing"] as const;
type Orientation = "upright" | "reversed";
export type TarotSnapshot = {
  oracle: 16;
  profile: typeof TAROT_PROFILE;
  spread: "one" | "three";
  cards: { id: string; orientation: Orientation }[];
};
export interface ReferenceCard extends Card {
  meanings: Record<Orientation, Meaning>;
  additional_meanings: { text: string; locator: string; page: number } | null;
  qualifications: string[];
}
const cards: Record<string, ReferenceCard> = archive.tarot.cards;
export const cardReference = (id: string) => cards[id];
export const tarotPage = (page: number) =>
  `https://en.wikisource.org/wiki/Page:The_Pictorial_Key_to_the_Tarot.pdf/${page + 13}`;

const edition = "A. E. Waite · The Pictorial Key to the Tarot · 1922";
export const sequenceRule = "tarot.waite1922.sequence";
export const recurrence = {
  "two-2": "accord",
  "two-3": "security",
  "three-2": "calm",
  "three-3": "unity",
} as const;
export const recurrenceId = (key: keyof typeof recurrence) => `tarot.waite1922.recurrence.${key}.upright`;
const reference = (text: string, url: string, locator: string, exceptions: string[]) =>
  ({ text, url, locator, edition, exceptions });
const flags: Record<string, string> = {
  alternative_or_conflicting_source_readings: "Waite preserves competing readings.",
  source_conditions_not_automatically_evaluated: "This edition leaves the source conditions unevaluated.",
  primary_section_has_no_reversed_entry_explicit_section4_gap_fill: "The main entry omits a reversal. This wording comes from the additional account in §4.",
};
const rules: Record<string, ReturnType<typeof reference>> = {
  [sequenceRule]: reference("", tarotPage(294), "Part III §4, p. 294", [
    "Waite observes that placement can modify meanings. The one- and three-card roles and their connections are FATE’s editorial frames.",
  ]),
  ...Object.fromEntries(Object.entries(recurrence).map(([key, motif]) => {
    const [rank, count] = key.split("-");
    const name = rank === "two" ? "Twos" : "Threes";
    return [recurrenceId(key as keyof typeof recurrence), reference(
      `Waite’s recurrence table associates ${count} upright ${name} with ${motif}.`,
      tarotPage(296), "Part III §5, p. 296 · natural position", [
        "This historical rank entry is shown separately from the individual cards. FATE applies it only in an entirely upright spread.",
      ])];
  })),
  ...Object.fromEntries(Object.values(cards).flatMap((card) =>
    Object.values(card.meanings).map((m) => [m.rule_id,
      reference(m.text, m.page_url, m.locator, [...m.flags.map((flag) => flags[flag] ?? flag),
        ...(m.symbolic_focus.startsWith("unchanged:") ? ["Waite marks this meaning as unchanged in reversal."] : [])]),
    ]))),
};
export const tarotRule = (id: string) => Object.hasOwn(rules, id) ? rules[id] : undefined;
