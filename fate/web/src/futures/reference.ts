import folios from "./folios-v1.json";
import type { Evidence } from "../codex/reference";
import type { FutureBookmark, Readout, Source, StudyId } from "./contracts";

const library = folios as Record<
  StudyId,
  { choices: Record<number, Readout>; sources: Source[] }
>;
export function savedStudy(s: FutureBookmark) {
  const item = library[s.oracle];
  return { view: item.choices[s.option], sources: item.sources };
}
export function futureEvidence(s: FutureBookmark): Evidence[] {
  const { view, sources } = savedStudy(s);
  return sources.slice(0, 4).map((source) => ({
    label: view.title,
    wording: view.lead,
    quote: view.lead,
    sourceId: source.id,
    url: source.url,
    locator: source.locator || source.title,
    alternative: true,
  }));
}
