import { useMemo } from "react";
import type { Oracle } from "../hooks/useOracle";
import type { Result } from "../types";
import type { NumberResult } from "../experiences/contracts";
import { chapterFor, tarotSnapshot, numberSnapshot } from "./records";
import { westernSnapshot, type WesternResult } from "../astrology/contracts";
import type { Narrative } from "./narrative";
type Props = { oracle: Oracle } & (
  | { kind: "tarot"; result: Result; narrative?: Narrative }
  | { kind: "numerology"; result: NumberResult; narrative?: Narrative }
  | { kind: "western"; result: WesternResult; narrative?: Narrative }
);
export function SaveChapter(props: Props) {
  const { oracle } = props;
  const narrative = props.narrative;
  const chapter = useMemo(
    () => chapterFor(
        props.result,
        props.kind === "western"
          ? westernSnapshot(props.result)
          : props.kind === "tarot"
            ? tarotSnapshot(props.result)
            : numberSnapshot(props.result),
        narrative,
      ),
    [props.kind, props.result, narrative],
  );
  const unavailable = !chapter.narrative;
  const saved = oracle.codex.chapters.some((c) => c.id === chapter.id);
  return (
    <section className="save-chapter" aria-labelledby={`save-${props.kind}`}>
      {props.kind !== "numerology" && <p className="eyebrow">A CHAPTER WORTH KEEPING</p>}
      <h2 id={`save-${props.kind}`}>
        {props.kind === "numerology" ? "Keep this reading" : <>Let this moment
        <br />
        <em>have a place.</em></>}
      </h2>
      <p>
        {props.kind === "western"
          ? "Save the natal passages, source references and calculated chart geometry. Celestial positions can reveal information about your birth moment."
          : props.kind === "numerology"
            ? "Save the calculated numbers, passages and sources. The Birthday passage includes the day of the month. The chosen calendar date, letter tokens and Y classifications stay outside the chapter."
            : "Save the cards in order, their orientations, the connected reading and its source references."}{" "}
        Names, entered dates and times, coordinates, timezone, questions and
        Gemini commentary are excluded.
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
          disabled={saved || unavailable}
          onClick={() =>
            oracle.codex.save({ ...chapter, savedAt: new Date().toISOString() })
          }
        >
          {saved ? "Saved to this device" : "Save to this device"}
          <span aria-hidden="true">○</span>
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
        {saved ? "A new chapter is waiting in My Fate."
          : unavailable ? "This interpretation edition is unavailable for saving."
          : oracle.codex.issue}
      </p>
    </section>
  );
}
