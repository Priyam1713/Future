import reference from "./reference-v1.json";
import type { Card } from "../types";
import type { Chapter, Snapshot } from "./records";
interface SourceMeaning {
  symbolic_focus: string;
  text: string;
  rule_id: string;
  locator: string;
  page_url: string;
  flags: string[];
}
export interface ReferenceCard extends Card {
  meanings: Record<"upright" | "reversed", SourceMeaning>;
  additional_meanings: { text: string; locator: string } | null;
}
const cards = reference.tarot.cards as unknown as Record<string, ReferenceCard>;
export interface Evidence {
  label: string;
  quote: string;
  wording: string;
  sourceId: string;
  url: string;
  locator: string;
  alternative: boolean;
}
export function cardReference(id: string) {
  return cards[id];
}
export function chapterTitle(chapter: Chapter) {
  return chapter.snapshot.oracle === 16
    ? chapter.snapshot.cards.map((p) => cards[p.id].name).join(" · ")
    : `A ${chapter.snapshot.expression} / ${chapter.snapshot.personalYear} constellation`;
}
export function evidenceFor(snapshot: Snapshot): Evidence[] {
  if (snapshot.oracle === 16)
    return snapshot.cards.map((pick, i) => {
      const card = cards[pick.id],
        meaning = card.meanings[pick.orientation];
      return {
        label: `${snapshot.spread === "one" ? "Focus" : ["What you carry", "Where you stand", "What to consider"][i]} · ${card.name} · ${pick.orientation}`,
        quote: meaning.symbolic_focus,
        wording: meaning.text,
        sourceId: meaning.rule_id,
        url: meaning.page_url,
        locator: meaning.locator,
        alternative: meaning.symbolic_focus.includes(" OR "),
      };
    });
  return ["expression", "year"].map((key, i) => {
    const table = reference.numerology[key as "expression" | "year"];
    const number = i === 0 ? snapshot.expression : snapshot.personalYear;
    const text = (table.meanings as Record<string, string>)[String(number)];
    return {
      label: `${i === 0 ? "Expression" : "Personal Year"} ${number}`,
      quote: text,
      wording: text,
      sourceId: table.source_id,
      url: table.url,
      locator: table.locator,
      alternative: false,
    };
  });
}
export function exportChapters(chapters: Chapter[]) {
  return {
    schemaVersion: 1,
    application: "FATE · Living Codex",
    scope:
      "Minimal saved chapters and their versioned source references. Original inputs, replay seeds and Gemini commentary are excluded.",
    chapters: chapters.map((chapter) => ({
      ...chapter,
      source_readings: evidenceFor(chapter.snapshot),
    })),
  };
}
export function downloadChapters(
  chapters: Chapter[],
  name = "fate-codex.json",
) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(exportChapters(chapters), null, 2)], {
      type: "application/json",
    }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
