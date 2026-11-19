import { compareChapters } from "./compare";
import { chapterTitle, type Evidence } from "./reference";
import type { Chapter } from "./records";
import { ChapterIllustration } from "./ChapterContent";
function Quotation({ evidence }: { evidence: Evidence }) {
  return (
    <blockquote className="comparison-quote">
      <p>“{evidence.quote}”</p>
      <cite>
        {evidence.label} ·{" "}
        <a href={evidence.url} target="_blank" rel="noreferrer">
          Source
        </a>
      </cite>
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
          {left.snapshot.oracle === 1
            ? "ASTROLOGY"
            : left.snapshot.oracle === 16
              ? "TAROT"
              : "NUMEROLOGY"}{" "}
          · {chapterTitle(left)}
        </span>
        <span>
          {right.snapshot.oracle === 1
            ? "ASTROLOGY"
            : right.snapshot.oracle === 16
              ? "TAROT"
              : "NUMEROLOGY"}{" "}
          · {chapterTitle(right)}
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
          <span />✧<span />
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
        comparison.echoes.map((group) => (
          <article className="comparison-echo" key={group.label}>
            <h4>{group.label}</h4>
            <div>
              {[group.left, group.right].map((side, i) => (
                <div key={i}>
                  {side.map((e, j) => (
                    <Quotation evidence={e} key={j} />
                  ))}
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
      <h3>Different emphases</h3>
      <div className="comparison-differences">
        {[
          {
            groups: comparison.leftOnly,
            rows: comparison.leftEvidence,
            chapter: left,
          },
          {
            groups: comparison.rightOnly,
            rows: comparison.rightEvidence,
            chapter: right,
          },
        ].map((side, i) => (
          <div key={i}>
            <p className="eyebrow">
              {side.chapter.snapshot.oracle === 1
                ? "ASTROLOGY"
                : side.chapter.snapshot.oracle === 16
                  ? "TAROT"
                  : "NUMEROLOGY"}
            </p>
            <p>
              {side.groups.length
                ? side.groups.map((g) => g.label).join(" · ")
                : "Read this chapter’s source language in its own context."}
            </p>
            {side.rows.map((e, j) => (
              <Quotation key={j} evidence={e} />
            ))}
          </div>
        ))}
      </div>
      {comparison.alternatives.length > 0 && (
        <aside className="comparison-note">
          A source offers alternatives within a Tarot gloss. Those passages are
          displayed in full above and excluded from automatic theme matching.
        </aside>
      )}
      <details className="comparison-method">
        <summary>How this comparison works</summary>
        <p>
          A small versioned editorial vocabulary groups explicitly present words
          in saved Tarot glosses, direct Numerology summaries and separate
          Western Astrology source components. It uses no LLM, scores,
          probabilities or new meanings. Vocabulary coverage is limited; a
          shared heading describes language, rather than evidence about your
          life. Alternative accounts remain separate. Tarot positions are
          editorial prompts; Numerology’s two direct themes concern Expression
          and Personal Year only.
        </p>
        <p>
          {comparison.vocabulary} · Saved source editions {left.reference} /{" "}
          {right.reference}
        </p>
      </details>
      <p className="comparison-closing">
        What changes when you hold both perspectives gently, without needing
        them to become one answer?
      </p>
    </section>
  );
}
