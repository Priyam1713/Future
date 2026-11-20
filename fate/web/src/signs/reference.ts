import archive from "./reference-v1.json";
import type { Evidence } from "../codex/reference";
import { choicesTitle, type SignSnapshot, type SignView } from "./contracts";

const records = archive as Record<string, Record<string, SignView>>;
export function archivedView(s: SignSnapshot) {
  return records[s.oracle][s.values.join("|")];
}
export function signEvidence(s: SignSnapshot): Evidence[] {
  return archivedView(s).excerpts.map((e) => ({
    label: e.status,
    quote: e.text,
    wording: e.text,
    sourceId: e.sourceId,
    url: e.url ?? "",
    locator: e.locator,
    alternative: true,
  }));
}
export const signTitle = choicesTitle;
