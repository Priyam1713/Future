import { oracleLabel } from "../chambers/contracts";
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
              Save two chapters to compare their source perspectives.
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
                      {oracleLabel(chapter.snapshot.oracle)} —{" "}
                      {chapterTitle(chapter)}
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
          Saving keeps a small chapter in this browser profile. Chapters contain
          selected results, chart geometry, dated transit snapshots, or source
          bookmarks. They include the edition and save time. Codex exports use
          the same scope and include source references.
        </p>
        <p>
          Local records are unencrypted. Anyone using the profile can read them,
          and clearing site data can erase them. Export to keep a copy across
          devices or site addresses.
        </p>
        <details>
          <summary>Exact retention and limits</summary>
          <p>
            Names, birth details, questions, journal and dream notes,
            calibration, replay seeds and Gemini commentary stay outside the
            Codex. Chart geometry can reveal information about a birth moment.
            Saved transit chapters keep the dates you choose. Manuscript and
            compass bookmarks keep source IDs only. Dream Archive and Tomorrow
            Machine bookmarks keep the public study setting. Personal writing
            and live archive sessions stay outside My Fate.
          </p>
          <p>
            Comparison choices stay in memory. The app and artwork must be
            available to reopen chapters. This edition holds 50 chapters up to
            65,536 characters in total. Private mode and browser policies can
            restrict local saving.
          </p>
        </details>
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
