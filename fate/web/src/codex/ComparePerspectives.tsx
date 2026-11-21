import { oracleLabel } from "../chambers/contracts";
import { compareChapters } from "./compare";
import { chapterTitle, type Evidence } from "./reference";
import type { Chapter } from "./records";
import { ChapterIllustration } from "./ChapterContent";
import { useState } from "react";
function Quotation({ evidence }: { evidence: Evidence }) {
  return (
    <blockquote className="comparison-quote">
      <p>“{evidence.quote}”</p>
      <details className="comparison-citation">
        <summary>Source & context</summary>
        {evidence.rules ? <ul>{evidence.rules.map((rule) => (
          <li key={rule.id}>
            {rule.url ? <a href={rule.url} target="_blank" rel="noreferrer">{rule.locator}</a> : rule.locator}
            <p>{rule.edition} · {rule.id}</p>
            {rule.exceptions.map((exception) => <p key={exception}>{exception}</p>)}
          </li>
        ))}</ul> : <><cite>
          {evidence.label} ·{" "}
          <a href={evidence.url} target="_blank" rel="noreferrer">
            Source
          </a>
        </cite>
        <p>{evidence.locator}</p>
        <small>{evidence.sourceId}</small>
        <p>{evidence.wording}</p></>}
      </details>
    </blockquote>
  );
}
export function ComparePerspectives({
  left,
  right,
  onClose,
}: {
  left: Chapter;
  right: Chapter;
  onClose: () => void;
}) {
  const comparison = compareChapters(left, right);
  const [allEchoes, setAllEchoes] = useState(false);
  return (
    <section
      className="perspectives page-enter"
      aria-labelledby="compare-title"
    >
      <button className="text-button" onClick={onClose}>
        ← Back to your Codex
      </button>
      <p className="eyebrow">TWO CHAPTERS, SIDE BY SIDE</p>
      <h2 id="compare-title" tabIndex={-1}>
        Compare <em>Perspectives.</em>
      </h2>
      <p className="comparison-intro">
        Notice the language each tradition offers. Similar words can be useful
        prompts; they do not establish independent agreement or a shared
        prediction.
      </p>
      <div className="comparison-titles">
        <span>
          {oracleLabel(left.snapshot.oracle).toUpperCase()} ·{" "}
          {chapterTitle(left)}
        </span>
        <span>
          {oracleLabel(right.snapshot.oracle).toUpperCase()} ·{" "}
          {chapterTitle(right)}
        </span>
      </div>
      <div
        className="perspective-constellation"
        aria-label="The two selected source chapters"
      >
        <figure>
          <ChapterIllustration chapter={left} />
          <figcaption>{chapterTitle(left)}</figcaption>
        </figure>
        <div className="perspective-bridge" aria-hidden="true">
          <span />○<span />
        </div>
        <figure>
          <ChapterIllustration chapter={right} />
          <figcaption>{chapterTitle(right)}</figcaption>
        </figure>
      </div>
      {comparison.samePattern && (
        <p className="comparison-note">
          These chapters contain the same saved pattern. Repetition is not
          independent corroboration.
        </p>
      )}
      <h3>Echoes in the wording</h3>
      {comparison.echoes.length ? (
        comparison.echoes.slice(0, allEchoes ? undefined : 3).map((group) => (
          <article className="comparison-echo" key={group.label}>
            <h4>{group.label}</h4>
            <div>
              {[group.left, group.right].map((side, i) => (
                <div key={i}>
                  {side.slice(0, 1).map((e, j) => (
                    <Quotation evidence={e} key={j} />
                  ))}
                  {side.length > 1 && (
                    <details className="comparison-more">
                      <summary>{side.length - 1} more cited passages</summary>
                      {side.slice(1).map((e, j) => (
                        <Quotation key={j} evidence={e} />
                      ))}
                    </details>
                  )}
                </div>
              ))}
            </div>
          </article>
        ))
      ) : (
        <p className="comparison-note">
          These chapters share no match in this small editorial vocabulary.
          Absence of a match does not establish disagreement; each chapter can
          stand on its own.
        </p>
      )}
      {comparison.echoes.length > 3 && (
        <button
          className="text-button"
          onClick={() => setAllEchoes(!allEchoes)}
        >
          {allEchoes
            ? "Show fewer source families"
            : `Explore ${comparison.echoes.length - 3} other shared source families`}
        </button>
      )}
      <h3>Different emphases</h3>
      <div className="comparison-differences">
        {[
          {
            groups: comparison.leftOnly,
            lead: comparison.leftOnly[0]?.left[0],
            rows: comparison.leftEvidence,
            chapter: left,
          },
          {
            groups: comparison.rightOnly,
            lead: comparison.rightOnly[0]?.right[0],
            rows: comparison.rightEvidence,
            chapter: right,
          },
        ].map((side, i) => (
          <div key={i}>
            <p className="eyebrow">
              {oracleLabel(side.chapter.snapshot.oracle).toUpperCase()}
            </p>
            <p>
              {side.groups.length
                ? side.groups.map((g) => g.label).join(" · ")
                : "Read this chapter’s source language in its own context."}
            </p>
            {side.lead && <Quotation evidence={side.lead} />}
            {side.rows.length > 0 && (
              <details className="comparison-more">
                <summary>
                  Explore all {side.rows.length} source passages
                </summary>
                {side.rows.map((e, j) => (
                  <Quotation key={j} evidence={e} />
                ))}
              </details>
            )}
          </div>
        ))}
      </div>
      {comparison.alternatives.length > 0 && (
        <aside className="comparison-note">
          Alternative readings and procedural references remain available in the
          source passages. Automatic theme matching skips them.
        </aside>
      )}
      <details className="comparison-method">
        <summary>How this comparison works</summary>
        <p>
          A small versioned editorial vocabulary groups explicitly present words
          in saved narratives and earlier source chapters. Each passage stays
          with its source tradition and coverage. Matching uses a fixed vocabulary
          and adds no new interpretations or scores. Alternative accounts remain
          separate. Tarot positions are
          editorial prompts; Numerology’s two direct themes concern Expression
          and Personal Year only.
        </p>
        <p>
          {comparison.vocabulary} · Saved source editions {left.narrative?.edition ?? left.reference} /{" "}
          {right.narrative?.edition ?? right.reference}
        </p>
      </details>
      <p className="comparison-closing">
        What changes when you hold both perspectives gently, without needing
        them to become one answer?
      </p>
    </section>
  );
}
