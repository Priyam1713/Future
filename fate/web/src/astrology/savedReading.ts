import type { NatalPassage, NatalReading } from "./contracts";
import { NARRATIVE_EDITIONS, type Narrative, type Passage, type ReadingSection } from "../codex/narrative";

export function westernNarrative(reading: NatalReading): Narrative | undefined {
  if (reading.profile !== NARRATIVE_EDITIONS[1] || !reading.chapters.length) return;
  const passage = (p: NatalPassage): Passage => ({
    title: p.title,
    text: p.body,
    coverage: p.coverage === "direct" ? "direct" : "compositional",
    rules: [...p.rule_ids],
  });
  const sections: ReadingSection[] = reading.chapters.map(({ id, title, passages }) =>
    ({ id, title, passages: passages.map(passage) }));
  const directIds = new Set(sections.flatMap(({ passages }) =>
    passages.filter((p) => p.coverage === "direct").flatMap((p) => p.rules)));
  const extra = Object.values(reading.focuses).flatMap((focus) => focus.passages)
    .filter((p) => {
      if (p.rule_ids.every((id) => directIds.has(id))) return false;
      p.rule_ids.forEach((id) => directIds.add(id));
      return true;
    }).map(passage);
  const ruler = reading.chart_ruler;
  if (ruler) extra.unshift({
    title: "Chart ruler",
    text: `${ruler.body} · ${ruler.sign} · House ${ruler.house}.`,
    coverage: "compositional",
    rules: [...ruler.rule_ids],
  });
  if (extra.length) sections.push({ id: "chart-details", title: "Chart details", passages: extra });
  return { technique: 1, edition: NARRATIVE_EDITIONS[1], sections };
}
