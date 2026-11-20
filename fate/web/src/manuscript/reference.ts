import edition from "./reference-v1.json";
import type { Evidence } from "../codex/reference";
import { type Bookmark, type BookmarkId, type View } from "./contracts";

const archive = edition as Record<BookmarkId, Record<string, View>>;
export function bookmarkViews(s: Bookmark) {
  return s.entries.map((key) => archive[s.oracle][key]);
}
export function bookmarkTitle(s: Bookmark) {
  return bookmarkViews(s)
    .map(({ title }) => title)
    .join(" · ");
}
export function bookmarkEvidence(s: Bookmark): Evidence[] {
  return bookmarkViews(s).flatMap((view) =>
    view.sources.map((source) => ({
      label: view.title,
      quote: source.text,
      wording: source.text,
      url: source.url,
      locator: source.locator,
      sourceId: source.sourceId,
      alternative: true,
    })),
  );
}
