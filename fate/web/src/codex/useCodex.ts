import { useEffect, useState } from "react";
import {
  STORAGE_KEY,
  readDocument,
  saveChapter,
  deleteChapter,
  type Chapter,
} from "./records";
const unavailable =
  "This browser could not change the Codex. Storage may be blocked or full. Your reading is still available; export it to keep a copy.";
export function useCodex() {
  const [chapters, setChapters] = useState<Chapter[]>([]),
    [issue, setIssue] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  function refresh() {
    try {
      setChapters(readDocument(localStorage).chapters);
      setIssue("");
    } catch (e) {
      setChapters([]);
      setIssue(
        e instanceof Error
          ? e.message
          : "This browser’s local storage is unavailable.",
      );
    }
  }
  useEffect(() => {
    refresh();
    const change = (event: StorageEvent) => {
      if (event.key === STORAGE_KEY || event.key === null) refresh();
    };
    addEventListener("storage", change);
    return () => removeEventListener("storage", change);
  }, []);
  function save(chapter: Chapter) {
    try {
      const next = saveChapter(localStorage, chapter);
      setChapters(next.chapters);
      setIssue("");
      return true;
    } catch (e) {
      setIssue(
        e instanceof Error && e.message.includes("Codex")
          ? e.message
          : unavailable,
      );
      return false;
    }
  }
  function remove(id: string) {
    try {
      const next = deleteChapter(localStorage, id);
      setChapters(next.chapters);
      setIssue("");
      return true;
    } catch {
      setIssue(unavailable);
      return false;
    }
  }
  function clear() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      setChapters([]);
      setSelectedId(null);
      setIssue("");
      return true;
    } catch {
      setIssue(unavailable);
      return false;
    }
  }
  return { chapters, issue, selectedId, setSelectedId, save, remove, clear };
}
export type Codex = ReturnType<typeof useCodex>;
