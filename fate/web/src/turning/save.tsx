import { useMemo, useState } from "react";
import { chapterFor } from "../codex/records";
import { transitSnapshot } from "./snapshot";
import type { TurningResult } from "./contracts";
import type { Oracle } from "../hooks/useOracle";
export function SaveTransit({
  result,
  oracle,
}: {
  result: TurningResult;
  oracle: Oracle;
}) {
  const [error, setError] = useState("");
  const chapter = useMemo(() => {
    try {
      return chapterFor(result, transitSnapshot(result));
    } catch {
      return null;
    }
  }, [result]);
  const saved =
    !!chapter && oracle.codex.chapters.some((c) => c.id === chapter.id);
  return (
    <section className="save-chapter">
      <p className="eyebrow">A DATED CHAPTER / YOUR CHOICE</p>
      <h2>
        Keep this
        <br />
        <em>turn of the sky.</em>
      </h2>
      <p>
        Save the dated contacts, native daily samples, orb intervals and matched
        source references. Birth inputs, location, natal-session proof and
        Gemini commentary are excluded.
      </p>
      <p className="save-privacy">
        Derived sky geometry and dates are still personal and can reveal
        information about a birth moment. Stored unencrypted in this browser
        profile, without automatic backup or sync. The 65,536-character Codex
        limit can fill before 50 chapters, especially for longer windows.
      </p>
      <div className="save-actions">
        <button
          className="primary"
          disabled={saved || !chapter}
          onClick={() => {
            if (chapter) {
              const ok = oracle.codex.save({
                ...chapter,
                savedAt: new Date().toISOString(),
              });
              if (!ok)
                setError(
                  "The chapter could not be saved. Your live reading and full native export remain available.",
                );
            }
          }}
        >
          {saved
            ? "Saved to this device"
            : "Save transit chapter to this device"}{" "}
          ○
        </button>
        {saved && (
          <button
            className="text-button"
            onClick={() => {
              oracle.codex.setSelectedId(chapter!.id);
              oracle.navigate("codex");
            }}
          >
            Open in My Fate →
          </button>
        )}
      </div>
      <p role="status">
        {error ||
          oracle.codex.issue ||
          (!chapter
            ? "This source edition cannot save the report; use the full native export instead."
            : "")}
      </p>
    </section>
  );
}
