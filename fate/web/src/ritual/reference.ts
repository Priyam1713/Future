import data from "./reference-v1.json";
import type { Evidence } from "../codex/reference";
import { RITUAL_ROOMS, type RitualSnapshot } from "./contracts";

export const archive = data;
export const card = (id: string) => archive.cards.find((c) => c.id === id)!;
export const figure = (pattern: string) =>
  archive.geo.figures.find((f) => f.pattern === pattern)!;
export const motif = (id: string) =>
  archive.dream.motifs[id as keyof typeof archive.dream.motifs];
export const titleCase = (name: string) =>
  name.replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase());
export function passage(id: string, radius: number) {
  const page = archive.book.pages.find((page) =>
    page.passages.some((p) => p.sentence_id === id),
  )!;
  const i = page.passages.findIndex((p) => p.sentence_id === id);
  return {
    ...page.passages[i],
    context_before: page.passages.slice(Math.max(0, i - radius), i),
    context_after: page.passages.slice(i + 1, i + radius + 1),
  };
}
const evidence = (
  label: string,
  quote: string,
  source: { id: string; url?: string | null },
  locator: string,
  alternative = false,
): Evidence => ({
  label,
  quote,
  wording: quote,
  sourceId: source.id,
  url: source.url ?? "",
  locator,
  alternative,
});
export function ritualTitle(s: RitualSnapshot) {
  const v = s.values;
  switch (s.oracle) {
    case 17:
      return v.map((id) => card(id).name).join(" · ");
    case 20:
      return (
        (v[0] === "seeded" ? "Digital symbol · " : "Manual reading · ") +
        titleCase(v[1])
      );
    case 21:
    case 22:
      return RITUAL_ROOMS[s.oracle].title + " · Guide";
    case 23:
      return v.length
        ? v.map(titleCase).join(" · ")
        : "Dream reference bookmark";
    case 33:
      return "The shield · " + figure(v[14]).name;
    case 36:
      return v
        .slice(1)
        .map((id) => passage(id, 0).citation)
        .join(" · ");
  }
}
export function ritualEvidence(s: RitualSnapshot): Evidence[] {
  const v = s.values;
  switch (s.oracle) {
    case 17:
      return v.map((id) => {
        const c = card(id);
        return {
          ...evidence(
            c.name,
            c.meaning.text,
            archive.cardSource,
            c.meaning.locator,
          ),
          wording: c.meaning.text + " " + c.meaning.context,
        };
      });
    case 20:
      return archive.pendulum.rules.map((r) =>
        evidence(
          "Pendulum procedure",
          r.statement,
          archive.pendulum.source,
          r.locator,
          true,
        ),
      );
    case 21:
    case 22: {
      const guide = archive.guides[s.oracle];
      return [
        ...new Map(
          guide.steps
            .flatMap((step) => step.source_components)
            .map((row) => [row.id, row]),
        ).values(),
      ].map((row) =>
        evidence(
          "Historical guide",
          row.statement,
          guide.source,
          row.locator,
          true,
        ),
      );
    }
    case 23:
      return v.map((id) =>
        evidence(
          titleCase(id),
          motif(id).reference.definition,
          archive.dream.source,
          motif(id).reference.provenance.locator,
          true,
        ),
      );
    case 33:
      return [
        evidence(
          "Turner shield rule",
          "Four manual Mothers, four transposed Daughters, four Nieces, two Witnesses and the Judge.",
          archive.geo.source,
          archive.geo.locator,
          true,
        ),
      ];
    case 36:
      return v.slice(1).map((id) => {
        const row = passage(id, 0);
        return evidence(
          "Manually chosen text",
          row.text,
          { id: archive.book.source.id, url: row.source_url },
          row.citation,
          true,
        );
      });
  }
}
