import { useMemo } from "react";
import type { Oracle } from "../hooks/useOracle";
import type { Result } from "../types";
import type { NumberResult } from "../experiences/contracts";
import { chapterFor, tarotSnapshot, numberSnapshot } from "./records";
type Props = { oracle: Oracle } & (
  | { kind: "tarot"; result: Result }
  | { kind: "numerology"; result: NumberResult }
);
export function SaveChapter(props: Props) {
  const { oracle } = props;
  const chapter = useMemo(
    () =>
      chapterFor(
        props.result,
        props.kind === "tarot"
          ? tarotSnapshot(props.result)
          : numberSnapshot(props.result),
      ),
    [props.kind, props.result],
  );
  const saved = oracle.codex.chapters.some((c) => c.id === chapter.id);
  return (
    <section className="save-chapter" aria-labelledby={`save-${props.kind}`}>
      <p className="eyebrow">A CHAPTER WORTH KEEPING</p>
      <h2 id={`save-${props.kind}`}>
        Let this moment
        <br />
        <em>have a place.</em>
      </h2>
      <p>
        Save the symbols and numbers to your personal Codex on this device.
        Names, entered dates, questions and Gemini commentary are excluded.
      </p>
      <p className="save-privacy">
        Saved readings are still personal. They are stored unencrypted in this
        browser profile, without a backup or cloud sync. Clearing site data or
        using private browsing can erase them. The app and its artwork must be
        available to reopen them.
      </p>
      <div className="save-actions">
        <button
          className="primary"
          disabled={saved}
          onClick={() =>
            oracle.codex.save({ ...chapter, savedAt: new Date().toISOString() })
          }
        >
          {saved ? "Saved to this device" : "Save to this device"}
          <span aria-hidden="true">✧</span>
        </button>
        {saved && (
          <button
            className="text-button"
            onClick={() => {
              oracle.codex.setSelectedId(chapter.id);
              oracle.navigate("codex");
            }}
          >
            Open in My Fate →
          </button>
        )}
      </div>
      <p role="status" className="save-status">
        {saved ? "A new chapter is waiting in My Fate." : oracle.codex.issue}
      </p>
    </section>
  );
}
