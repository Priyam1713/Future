import { isFutureBookmark } from "../futures/contracts";
import { FutureChapter } from "../futures/StudyPage";
import { isBookmark } from "../manuscript/contracts";
import { BookmarkPage } from "../manuscript/Result";
import CardArt from "../CardArt";
import type { Chapter } from "./records";
import { cardReference, chapterTitle, evidenceFor } from "./reference";
import { ReadingConclusion } from "../components/ReadingConclusion";
import { plainGloss } from "../experiences/tarotPresentation";
import { BirthChart } from "../astrology/BirthChart";
import { snapshotGeometry, degree } from "../astrology/contracts";
import { restoreTransit } from "../turning/snapshot";
import { TimeInstrument } from "../turning/TimeInstrument";
import { TransitChapter } from "../turning/TransitChapter";
import { isChamberSnapshot, ROOMS } from "../chambers/contracts";
import { ChamberChapter, Instrument } from "../chambers/ChamberScreen";
import { isSign } from "../signs/contracts";
import { SavedSign } from "../signs/SignsScreen";
import { isRitualSnapshot, RITUAL_ROOMS } from "../ritual/contracts";
import { RitualChapter, RitualReading } from "../ritual/Readings";
import { NarrativeReading } from "./NarrativeReading";
export function ChapterIllustration({ chapter }: { chapter: Chapter }) {
  const s = chapter.snapshot;
  if (isFutureBookmark(s)) return <FutureChapter s={s} compact />;
  if (isBookmark(s)) return <BookmarkPage snapshot={s} compact />;
  if (isSign(s)) return <SavedSign s={s} compact />;
  if (isRitualSnapshot(s))
    return (
      <div className={"ritual-miniature ritual-" + RITUAL_ROOMS[s.oracle].slug}>
        <RitualReading s={s} compact />
      </div>
    );
  if (isChamberSnapshot(s))
    return (
      <div
        className={"chamber-miniature chamber-" + ROOMS[s.oracle].slug}
        data-motion="still"
        data-reading={chapter.narrative?.technique}
      >
        <Instrument snapshot={s} compact frames={chapter.narrative?.technique === 2} />
      </div>
    );
  if (s.profile === "turning-sky-v1")
    return (
      <div className="codex-chart-study">
        <TimeInstrument
          result={restoreTransit(s)}
          index={0}
          onDay={() => {}}
          selectedEvent={null}
          reduced
          paused
          compact
        />
      </div>
    );
  if (s.oracle === 1)
    return (
      <div className="codex-chart-study">
        <BirthChart chart={snapshotGeometry(s)} compact reduced paused />
      </div>
    );
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
      <i>○</i>
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
  if (chapter.narrative) {
    const s = chapter.snapshot;
    const context = s.oracle === 1 && s.profile === "modern-tropical-v1"
      ? `Tropical · ${s.houses} houses · Ascendant ${degree(s.angles[0])}`
      : s.oracle === 3 ? `Clock convention · ${s.profile}`
      : s.oracle === 4 ? "Decoz · Personal Code" : "Sidereal · Rashi and Navamsa";
    return <NarrativeReading key={chapter.id} narrative={chapter.narrative}
      title={chapterTitle(chapter)} context={context}
      illustration={<ChapterIllustration chapter={chapter} />} />;
  }
  if (isFutureBookmark(chapter.snapshot))
    return <FutureChapter key={chapter.id} s={chapter.snapshot} />;
  if (isBookmark(chapter.snapshot))
    return <BookmarkPage key={chapter.id} snapshot={chapter.snapshot} />;
  if (isSign(chapter.snapshot))
    return <SavedSign key={chapter.id} s={chapter.snapshot} index={index} />;
  if (isRitualSnapshot(chapter.snapshot))
    return (
      <RitualChapter key={chapter.id} s={chapter.snapshot} index={index} />
    );
  if (isChamberSnapshot(chapter.snapshot))
    return (
      <ChamberChapter key={chapter.id} s={chapter.snapshot} index={index} />
    );
  const rows = evidenceFor(chapter.snapshot);
  if (chapter.snapshot.profile === "turning-sky-v1")
    return (
      <TransitChapter
        chapter={{ ...chapter, snapshot: chapter.snapshot }}
        index={index}
      />
    );
  return (
    <>
      <header className="folio-heading">
        <p className="eyebrow">
          CHAPTER {String(index + 1).padStart(2, "0")} ·{" "}
          {chapter.snapshot.oracle === 1
            ? "WESTERN ASTROLOGY"
            : chapter.snapshot.oracle === 16
              ? "TAROT"
              : "NUMEROLOGY"}
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
        {chapter.snapshot.oracle === 1 &&
          chapter.snapshot.profile === "modern-tropical-v1" && (
            <div className="folio-chart-context">
              <p>Ascendant {degree(chapter.snapshot.angles[0])}</p>
              <p>
                Tropical · {chapter.snapshot.houses} houses. These are separate
                source components, not a combined placement interpretation.
                Planet symbols are supplied for Sun, Moon and Mercury only; no
                other planet-specific or direct aspect-pair meanings are added.
              </p>
              <details>
                <summary>The saved chart geometry</summary>
                <pre>
                  {JSON.stringify(snapshotGeometry(chapter.snapshot), null, 2)}
                </pre>
              </details>
            </div>
          )}
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
      {chapter.snapshot.oracle !== 1 && (
        <ReadingConclusion
          themes={rows.map((r) =>
            chapter.snapshot.oracle === 16 ? plainGloss(r.quote) : r.quote,
          )}
          kind={chapter.snapshot.oracle === 16 ? "tarot" : "numerology"}
        />
      )}
      {chapter.snapshot.oracle === 1 && (
        <p className="folio-scope">
          Your sky offers documented themes to reflect on, rather than a
          verdict. Birth details and Gemini commentary are excluded; the
          celestial geometry itself remains personal and can reveal information
          about the birth moment.
        </p>
      )}
      <p className="folio-scope">
        Saved chapter · {chapter.reference}. Original inputs, entered dates,
        questions, replay seeds and Gemini commentary are excluded. This is a
        source-based snapshot of the completed reading. Full native calculation
        traces remain in any native export you explicitly downloaded.
      </p>
    </>
  );
}
