import CardArt from "../CardArt";
import type { Chapter } from "./records";
import { cardReference, chapterTitle, evidenceFor } from "./reference";
import { ReadingConclusion } from "../components/ReadingConclusion";
import { plainGloss } from "../experiences/tarotPresentation";
export function ChapterIllustration({ chapter }: { chapter: Chapter }) {
  const s = chapter.snapshot;
  return s.oracle === 16 ? (
    <div className={`codex-card-study count-${s.cards.length}`}>
      {s.cards.map((p) => (
        <div
          key={p.id}
          className={p.orientation === "reversed" ? "reversed-art" : ""}
        >
          <CardArt card={cardReference(p.id)} />
        </div>
      ))}
    </div>
  ) : (
    <div
      className="codex-number-study"
      aria-label={`Expression ${s.expression}, Personal Year ${s.personalYear}`}
    >
      <span className="number-study-ring" />
      <strong>{s.expression}</strong>
      <i>✧</i>
      <strong>{s.personalYear}</strong>
      <small>EXPRESSION / PERSONAL YEAR</small>
    </div>
  );
}
export function ChapterContent({
  chapter,
  index,
}: {
  chapter: Chapter;
  index: number;
}) {
  const rows = evidenceFor(chapter.snapshot);
  return (
    <>
      <header className="folio-heading">
        <p className="eyebrow">
          CHAPTER {String(index + 1).padStart(2, "0")} ·{" "}
          {chapter.snapshot.oracle === 16 ? "TAROT" : "NUMEROLOGY"}
        </p>
        <h2 tabIndex={-1}>{chapterTitle(chapter)}</h2>
        <p>
          Kept on{" "}
          {new Date(chapter.savedAt).toLocaleDateString(undefined, {
            day: "numeric",
            month: "long",
            year: "numeric",
          })}
        </p>
      </header>
      <div className="folio-mobile-art">
        <ChapterIllustration chapter={chapter} />
      </div>
      <div className="folio-themes">
        {rows.map((row, i) => (
          <section key={i}>
            <p className="eyebrow">{row.label}</p>
            <p className="folio-theme">
              {chapter.snapshot.oracle === 16
                ? plainGloss(row.quote)
                : row.quote}
            </p>
            <details>
              <summary>
                The source passage <span aria-hidden="true">＋</span>
              </summary>
              <blockquote>{row.wording}</blockquote>
              {chapter.snapshot.oracle === 16 && (
                <p>Original source motifs: {row.quote}</p>
              )}
              <a href={row.url} target="_blank" rel="noreferrer">
                {row.locator}
              </a>
              <p className="folio-rule">{row.sourceId}</p>
              {row.alternative && (
                <p>
                  Alternative accounts are retained separately in this passage.
                </p>
              )}
              <p>
                Historical symbolic language is recorded as doctrine. It does
                not establish personal traits, health, motives or future events.
              </p>
            </details>
          </section>
        ))}
      </div>
      {chapter.snapshot.oracle === 4 && (
        <details className="folio-context">
          <summary>Your calculated context</summary>
          <p>
            Life Path {chapter.snapshot.lifePath}. A calculated birth-date
            framework; this source edition supplies no direct number-specific
            meaning for it.
          </p>
        </details>
      )}
      <ReadingConclusion
        themes={rows.map((r) =>
          chapter.snapshot.oracle === 16 ? plainGloss(r.quote) : r.quote,
        )}
        kind={chapter.snapshot.oracle === 16 ? "tarot" : "numerology"}
      />
      <p className="folio-scope">
        Saved chapter · {chapter.reference}. Original inputs, entered dates,
        questions, replay seeds and Gemini commentary are excluded. This is a
        source-based snapshot of the completed reading. Full native calculation
        traces remain in any native export you explicitly downloaded.
      </p>
    </>
  );
}
