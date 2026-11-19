import { useEffect, useRef, useState } from "react";
import type { Oracle } from "../hooks/useOracle";
import { CelestialBook } from "../codex/CelestialBook";
import { ComparePerspectives } from "../codex/ComparePerspectives";
import { chapterTitle, downloadChapters } from "../codex/reference";
export default function CodexScreen({ oracle }: { oracle: Oracle }) {
  const { codex } = oracle;
  const [comparison, setComparison] = useState<string[]>([]),
    [comparing, setComparing] = useState(false);
  const [deleteId, setDeleteId] = useState<string | null>(null),
    [clearAll, setClearAll] = useState(false);
  const confirm = useRef<HTMLDialogElement>(null);
  const a = codex.chapters.find((c) => c.id === comparison[0]),
    b = codex.chapters.find((c) => c.id === comparison[1]);
  const selected =
    codex.chapters.find((c) => c.id === codex.selectedId) ?? codex.chapters[0];
  useEffect(() => {
    if (comparing)
      document.getElementById("compare-title")?.focus({ preventScroll: true });
  }, [comparing]);
  useEffect(() => {
    if (comparing && (!a || !b)) setComparing(false);
  }, [a, b, comparing]);
  function requestDelete(id: string | null) {
    setDeleteId(id);
    setClearAll(id === null);
    confirm.current?.showModal();
  }
  return (
    <div className="codex-room page-enter">
      <div className="codex-heading">
        <p className="eyebrow">YOUR PERSONAL ATLAS · ON THIS DEVICE</p>
        <h1 ref={oracle.heading} tabIndex={-1}>
          A constellation
          <br />
          of <em>your own.</em>
        </h1>
        <p>Small moments of wonder, bound into something you can return to.</p>
      </div>
      {codex.issue && (
        <p className="codex-error" role="alert">
          {codex.issue}
        </p>
      )}
      {comparing && a && b ? (
        <ComparePerspectives
          left={a}
          right={b}
          onClose={() => setComparing(false)}
        />
      ) : (
        <CelestialBook
          oracle={oracle}
          onCompare={(id) => {
            setComparison([id]);
            document.getElementById("choose-perspectives")?.scrollIntoView({
              behavior: oracle.reduced || oracle.paused ? "instant" : "smooth",
              block: "start",
            });
          }}
        />
      )}
      {codex.chapters.length > 0 && (
        <section className="codex-tools" aria-label="Manage saved chapters">
          <div>
            <p className="eyebrow">YOUR CHAPTERS, YOUR CHOICE</p>
            <p>Keep a copy beyond this browser, or let a chapter go.</p>
          </div>
          <button
            className="secondary"
            onClick={() => downloadChapters(codex.chapters)}
          >
            Export Codex
          </button>
          {selected && (
            <>
              <button
                className="text-button"
                onClick={() =>
                  downloadChapters([selected], "fate-chapter.json")
                }
              >
                Export this chapter
              </button>
              <button
                className="text-button"
                onClick={() => requestDelete(selected.id)}
              >
                Delete this chapter
              </button>
            </>
          )}
        </section>
      )}
      {!comparing && (
        <section className="perspective-picker" id="choose-perspectives">
          <p className="eyebrow">A CONVERSATION BETWEEN CHAPTERS</p>
          <h2>
            Two chapters.
            <br />
            <em>A wider view.</em>
          </h2>
          <p>
            Choose two saved chapters to notice shared language and different
            emphases. Each tradition keeps its own voice.
          </p>
          {codex.chapters.length < 2 ? (
            <p className="scope-note">
              Save two readings to begin. A Tarot reading and a Numerology
              reading can make an interesting pair.
            </p>
          ) : (
            <>
              <fieldset>
                <legend>Choose two chapters</legend>
                {codex.chapters.map((chapter, i) => (
                  <label key={chapter.id}>
                    <input
                      type="checkbox"
                      checked={comparison.includes(chapter.id)}
                      disabled={
                        comparison.length === 2 &&
                        !comparison.includes(chapter.id)
                      }
                      onChange={(e) =>
                        setComparison((p) =>
                          e.target.checked
                            ? [...p, chapter.id]
                            : p.filter((id) => id !== chapter.id),
                        )
                      }
                    />
                    <span>
                      {String(i + 1).padStart(2, "0")} ·{" "}
                      {chapter.snapshot.oracle === 16 ? "Tarot" : "Numerology"}{" "}
                      — {chapterTitle(chapter)}
                    </span>
                  </label>
                ))}
              </fieldset>
              <button
                className="primary"
                disabled={!a || !b}
                onClick={() => {
                  setComparing(true);
                  window.scrollTo({ top: 0, behavior: "instant" });
                }}
              >
                Compare Perspectives →
              </button>
            </>
          )}
        </section>
      )}
      <details className="codex-privacy">
        <summary>About saving on this device</summary>
        <p>
          Only Save to this device writes a chapter. It keeps the selected Tarot
          cards and orientations, or Numerology’s Expression, Personal Year and
          Life Path numbers, plus the source edition, chapter identifier and
          save time. Names, dates entered into Numerology, original questions,
          calculation traces, replay seeds and Gemini commentary are excluded.
          Exported Codex copies use this same minimal scope with source
          references.
        </p>
        <p>
          Records are unencrypted in this browser profile at this site address.
          Other people using this profile can read them. There is no account,
          cloud sync or automatic backup. Private browsing, clearing site data,
          browser policies or storage limits can erase or block them. The app
          and its artwork must be available to reopen chapters. Export before
          changing browser, device or site address. This edition holds up to 50
          chapters.
        </p>
        <p>
          Comparison selections stay in memory. Chapter records are not uploaded
          to the server or Gemini. Loading the app and its artwork still makes
          normal resource requests to the host.
        </p>
        <button className="text-button" onClick={() => requestDelete(null)}>
          Delete all local Codex data
        </button>
      </details>
      <dialog ref={confirm} className="codex-confirm">
        <h2>{clearAll ? "Let this Codex go?" : "Let this chapter go?"}</h2>
        <p>
          {clearAll
            ? "This removes all saved FATE chapters from this browser profile."
            : "This removes the selected chapter from this browser profile."}{" "}
          Export a copy first if you want to keep it. Previously downloaded
          files are unchanged.
        </p>
        <div>
          <button
            className="secondary"
            onClick={() => confirm.current?.close()}
          >
            Keep {clearAll ? "my Codex" : "this chapter"}
          </button>
          <button
            className="primary"
            onClick={() => {
              const okay = clearAll
                ? codex.clear()
                : deleteId
                  ? codex.remove(deleteId)
                  : false;
              if (okay) {
                setComparison([]);
                setComparing(false);
                confirm.current?.close();
              }
            }}
          >
            {clearAll ? "Delete all saved chapters" : "Delete chapter"}
          </button>
        </div>
      </dialog>
    </div>
  );
}
