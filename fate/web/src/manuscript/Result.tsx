import { useState } from "react";
import type { Oracle } from "../hooks/useOracle";
import { chapterFor } from "../codex/records";
import { ResultLeaf } from "../components/ResultLeaf";
import {
  ROOMS,
  type Bookmark,
  type NativeResult,
  type View,
} from "./contracts";
import { bookmarkTitle, bookmarkViews } from "./reference";

export function ViewCard({ view }: { view: View }) {
  return (
    <ResultLeaf
      title={view.title}
      status={view.status}
      evidence={
        view.sources.length > 0 && (
          <details className="folio-depth">
            <summary>Open the source notes</summary>
            {view.sources.map((row, i) => (
              <figure key={i}>
                <blockquote>{row.text}</blockquote>
                <figcaption>
                  {row.url ? (
                    <a href={row.url} target="_blank" rel="noreferrer">
                      {row.locator}
                    </a>
                  ) : (
                    row.locator
                  )}
                </figcaption>
              </figure>
            ))}
          </details>
        )
      }
    >
      <p className="folio-lead">{view.lead}</p>
    </ResultLeaf>
  );
}

export function BookmarkPage({
  snapshot,
  compact = false,
}: {
  snapshot: Bookmark;
  compact?: boolean;
}) {
  return (
    <section className={`folio-bookmark folio-${ROOMS[snapshot.oracle][3]}`}>
      {compact ? (
        <div className="folio-bookmark-mark">
          <span aria-hidden="true">{snapshot.oracle === 40 ? "✥" : "◇"}</span>
          <strong>{bookmarkTitle(snapshot)}</strong>
        </div>
      ) : (
        <>
          <header className="folio-heading">
            <p className="eyebrow">
              {ROOMS[snapshot.oracle][1]} · Source bookmark
            </p>
            <h2 tabIndex={-1}>{bookmarkTitle(snapshot)}</h2>
          </header>
          {bookmarkViews(snapshot).map((view) => (
            <ViewCard key={view.title} view={view} />
          ))}
        </>
      )}
    </section>
  );
}

function exportNative(result: NativeResult, name: string) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(result, null, 2)], { type: "application/json" }),
  );
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `fate-${name}-native.json`;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

export function ResultActions({
  result,
  name,
  snapshot,
  oracle,
}: {
  result: NativeResult;
  name: string;
  snapshot?: Bookmark;
  oracle: Oracle;
}) {
  const [issue, setIssue] = useState(false);
  const chapter = snapshot && chapterFor(result, snapshot);
  const saved =
    chapter &&
    oracle.codex.chapters.some((candidate) => candidate.id === chapter.id);
  return (
    <div className="folio-actions">
      {chapter &&
        (saved ? (
          <button
            className="text-button"
            onClick={() => {
              oracle.codex.setSelectedId(chapter.id);
              oracle.navigate("codex");
            }}
          >
            Open in My Fate →
          </button>
        ) : (
          <button
            className="secondary"
            onClick={() => setIssue(!oracle.codex.save(chapter))}
          >
            Save source bookmark to this device
          </button>
        ))}
      <details className="folio-depth">
        <summary>Export and privacy</summary>
        <p>
          {chapter
            ? "My Fate keeps the selected source IDs. Local bookmarks are readable in this browser profile."
            : "Your inputs stay in this visit. The native download includes your supplied inputs."}
        </p>
        <button
          className="secondary"
          onClick={() => exportNative(result, name)}
        >
          Export full native result
        </button>
      </details>
      {issue && <p role="alert">My Fate could not save this bookmark.</p>}
    </div>
  );
}
