import { useMemo } from "react";
import type { Chapter } from "../codex/records";
import type { TransitSnapshot } from "./contracts";
import { restoreTransit } from "./snapshot";
import { TurningExperience } from "./TurningSky";
import { chapterTitle } from "../codex/reference";
export function TransitChapter({
  chapter,
  index,
}: {
  chapter: Chapter & { snapshot: TransitSnapshot };
  index: number;
}) {
  const result = useMemo(
    () => restoreTransit(chapter.snapshot),
    [chapter.snapshot],
  );
  return (
    <>
      <header className="folio-heading">
        <p className="eyebrow">
          CHAPTER {String(index + 1).padStart(2, "0")} · THE TURNING SKY
        </p>
        <h2 tabIndex={-1}>{chapterTitle(chapter)}</h2>
        <p>Kept {new Date(chapter.savedAt).toLocaleDateString()}</p>
      </header>
      <div className="transit-folio">
        <TurningExperience result={result} saved />
      </div>
      <p className="folio-scope">
        Saved native samples, exact contacts, intervals and source identities ·{" "}
        {chapter.reference}. No new ephemeris or birth reconstruction. Original
        inputs, session proof and commentary are excluded; derived chart
        geometry remains personal.
      </p>
    </>
  );
}
