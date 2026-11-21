import { isFutureBookmark } from "../futures/contracts";
import { savedStudy, futureEvidence } from "../futures/reference";
import { isBookmark } from "../manuscript/contracts";
import { bookmarkEvidence, bookmarkTitle } from "../manuscript/reference";
import reference from "./reference-v1.json";
import type { Chapter, Snapshot } from "./records";
import { snapshotGeometry, signAt } from "../astrology/contracts";
import { sourcePlacements } from "../astrology/source";
import { dateLabel } from "../turning/contracts";
import { transitRule } from "../turning/snapshot";
import { isChamberSnapshot } from "../chambers/contracts";
import { chamberEvidence, chapterName } from "../chambers/reference";
import { isSign } from "../signs/contracts";
import { signTitle, signEvidence } from "../signs/reference";
import { isRitualSnapshot } from "../ritual/contracts";
import { ritualEvidence, ritualTitle } from "../ritual/reference";
import { narrativeRule } from "./narrative";
import { cardReference, spreadPositions } from "../experiences/tarotEdition";
export { cardReference };
export interface Evidence {
  label: string;
  quote: string;
  wording: string;
  sourceId: string;
  url: string;
  locator: string;
  alternative: boolean;
  rules?: { id: string; edition: string; url: string; locator: string; exceptions: string[] }[];
}
export function chapterTitle(chapter: Chapter) {
  if (isFutureBookmark(chapter.snapshot))
    return savedStudy(chapter.snapshot).view.title;
  if (isBookmark(chapter.snapshot)) return bookmarkTitle(chapter.snapshot);
  if (isSign(chapter.snapshot)) return signTitle(chapter.snapshot);
  if (isRitualSnapshot(chapter.snapshot)) return ritualTitle(chapter.snapshot);
  if (isChamberSnapshot(chapter.snapshot)) return chapterName(chapter.snapshot);
  if (chapter.snapshot.profile === "turning-sky-v1") {
    const [a, b] = chapter.snapshot.window,
      first = new Date(a).getUTCFullYear(),
      last = new Date(b).getUTCFullYear();
    return `The Turning Sky · ${dateLabel(a)}${first !== last ? `, ${first}` : ""}–${dateLabel(b)}, ${last}`;
  }
  if (chapter.snapshot.oracle === 1)
    return `${signAt(chapter.snapshot.planets[0][0])} Sun · ${signAt(chapter.snapshot.planets[1][0])} Moon`;
  return chapter.snapshot.oracle === 16
    ? chapter.snapshot.cards.map((p) => cardReference(p.id).name).join(" · ")
    : `A ${chapter.snapshot.expression} / ${chapter.snapshot.personalYear} constellation`;
}
export function evidenceFor(snapshot: Snapshot): Evidence[] {
  if (isFutureBookmark(snapshot)) return futureEvidence(snapshot);
  if (isBookmark(snapshot)) return bookmarkEvidence(snapshot);
  if (isSign(snapshot)) return signEvidence(snapshot);
  if (isRitualSnapshot(snapshot)) return ritualEvidence(snapshot);
  if (isChamberSnapshot(snapshot)) return chamberEvidence(snapshot);
  if (snapshot.profile === "turning-sky-v1") {
    const matched = new Map<number, string>();
    snapshot.configs.forEach((c) => {
      c[6].forEach((i) =>
        matched.set(i, "Documented symbolic pair under matched conditions"),
      );
      c[7].forEach((i) => {
        if (!matched.has(i)) matched.set(i, "Separate symbolic component");
      });
    });
    snapshot.events.forEach((e) => {
      e[9].forEach((i) =>
        matched.set(i, "Documented symbolic pair under matched conditions"),
      );
      e[10].forEach((i) => {
        if (!matched.has(i)) matched.set(i, "Separate symbolic component");
      });
    });
    return [...matched].map(([i, label]) => {
      const r = transitRule(i);
      return {
        label: `Turning Sky · ${label}`,
        quote: r.text,
        wording: r.text,
        sourceId: r.rule_id,
        url: r.source,
        locator: r.locator,
        alternative: false,
      };
    });
  }
  if (snapshot.oracle === 1)
    return sourcePlacements(snapshotGeometry(snapshot))
      .slice(0, 3)
      .flatMap((row) =>
        row.components.map((r) => ({
          label: `${row.planet} · ${row.sign} · House ${row.house} · separate component`,
          quote: r.text,
          wording: r.text,
          sourceId: r.id,
          url: r.url,
          locator: r.locator,
          alternative: false,
        })),
      );
  if (snapshot.oracle === 16)
    return snapshot.cards.map((pick, i) => {
      const card = cardReference(pick.id),
        meaning = card.meanings[pick.orientation];
      return {
        label: `${snapshot.spread === "one" ? "Focus" : spreadPositions[i]} · ${card.name} · ${pick.orientation}`,
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
export function chapterEvidence(chapter: Chapter): Evidence[] {
  const { narrative } = chapter;
  if (!narrative) return evidenceFor(chapter.snapshot);
  return narrative.sections.flatMap((section) => section.passages.map((passage) => {
    const rules = passage.rules.map((id) => {
      const { edition, url, locator, exceptions } = narrativeRule(narrative.edition, id)!;
      return { id, edition, url, locator, exceptions };
    });
    return {
      label: `${section.title} · ${passage.title} · ${passage.coverage}`,
      quote: passage.text,
      wording: passage.text,
      sourceId: rules[0].id,
      url: rules[0].url,
      locator: rules[0].locator,
      alternative: passage.coverage === "calculated" || passage.coverage === "unsupported",
      rules,
    };
  }));
}
export function exportChapters(chapters: Chapter[]) {
  const narratives = chapters.some((chapter) => chapter.narrative);
  return {
    schemaVersion: narratives ? 2 : 1,
    application: "FATE · Living Codex",
    scope: narratives
      ? "Saved interpretations, calculated context and versioned sources. Chart geometry and pillar combinations can reveal inferred birth information."
      : "Minimal saved chapters and their versioned source references. Original inputs, replay seeds and Gemini commentary are excluded.",
    chapters: chapters.map((chapter) => ({
      ...chapter,
      source_readings: chapterEvidence(chapter),
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
