import { lazy, Suspense, useState } from "react";
const TurningSky = lazy(() => import("../turning/TurningSky"));
import type { Oracle } from "../hooks/useOracle";
import { useWestern } from "../astrology/useWestern";
import { BirthForm } from "../astrology/BirthForm";
import { BirthChart } from "../astrology/BirthChart";
import { ChartCalculations, ChartReading, PlacementFocus } from "../astrology/ChartReading";
import { degree, signAt } from "../astrology/contracts";
import { SaveChapter } from "../codex/SaveChapter";
import { ArtifactSurface, SequenceMarks } from "../components/ArtifactSurface";
function exportNative(result: unknown) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(result, null, 2)], { type: "application/json" }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = "fate-western-native.json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export default function WesternScreen({ oracle }: { oracle: Oracle }) {
  const [turning, setTurning] = useState(false);
  const s = useWestern(oracle),
    r = s.result;
  const reading = s.envelope?.natal_reading;
  const select = (key: string) => {
    s.setSelected(key);
    oracle.sound.cue("select");
  };
  const names = ["Sun", "Moon", "Ascendant"];
  const name = names[s.step],
    lon = r
      ? s.step === 2
        ? r.angles.ascendant
        : r.planets[name].longitude
      : 0;
  if (turning && r)
    return (
      <Suspense fallback={<p role="status">Opening The Turning Sky...</p>}>
        <TurningSky
          origin={s.envelope?.transit_origin}
          oracle={oracle}
          onBack={() => setTurning(false)}
        />
      </Suspense>
    );
  return (
    <div
      className={`western-room page-enter western-${s.stage} finished-material`}
    >
      <div className="western-environment" aria-hidden="true">
        <picture>
          <source
            media="(max-width:700px)"
            srcSet="/art/western-observatory-portrait-450.webp 450w, /art/western-observatory-portrait-750.webp 750w"
            sizes="100vw"
          />
          <img
            src="/art/western-observatory-960.webp"
            srcSet="/art/western-observatory-640.webp 640w, /art/western-observatory-960.webp 960w, /art/western-observatory-1536.webp 1536w"
            sizes="100vw"
            width="1672"
            height="941"
            alt=""
          />
        </picture>
      </div>
      <div className="journey-top">
        <button
          className="text-button"
          onClick={() => oracle.navigate("gallery")}
        >
          ← The Gallery
        </button>
        <span className="eyebrow">Western Astrology</span>
      </div>
      <header className="western-heading">
        <p className="eyebrow">THE ASTRAL OBSERVATORY</p>
        <h1 ref={s.heading} tabIndex={-1}>
          {s.stage === "input" ? (
            <>
              The sky held
              <br />
              <em>a moment.</em>
            </>
          ) : s.stage === "ritual" ? (
            <>
              Three lights <em>in your sky.</em>
            </>
          ) : (
            <>
              Your <em>natal reading.</em>
            </>
          )}
        </h1>
        {s.stage !== "reading" && <p>
          {s.stage === "input"
            ? "Trace the real celestial geometry of your arrival."
            : "Explore the Sun, Moon and Ascendant before looking closer."}
        </p>}
      </header>
      {s.stage === "input" ? (
        <div className="western-entry">
          <aside className="observatory-invitation">
            <span className="observatory-seal" aria-hidden="true">
              ○
            </span>
            <p>
              A moment, precisely placed.
              <br />A sky of your own.
            </p>
            <small>
              The chart appears only after your actual time and place have been
              calculated.
            </small>
          </aside>
          <BirthForm
            onSubmit={(q) => void s.calculate(q)}
            busy={s.busy}
            error={s.error}
          />
        </div>
      ) : (
        r && (
          <>
            {s.stage === "reading" && reading && <ChartReading result={r} reading={reading} />}
            {s.stage === "reading" && <h2 className="natal-instrument-title" id="western-instrument" tabIndex={-1}>Explore your chart</h2>}
            <div className="western-chart-layout">
              <div className="western-instrument">
                <ArtifactSurface
                  still={oracle.reduced || oracle.paused}
                  className="western-surface"
                >
                  <BirthChart
                    chart={r}
                    reduced={oracle.reduced}
                    paused={oracle.paused}
                    selected={s.selected}
                    onSelect={select}
                    exploreDetails={s.stage === "reading"}
                  />
                </ArtifactSurface>
                <p className="chart-caption">
                  Tropical chart · {r.settings.houses.replaceAll("_", " ")}{" "}
                  houses
                </p>
              </div>
              {s.stage === "ritual" ? (
                <section className="chart-reveal" aria-live="polite">
                  <div key={s.step} className="artifact-arrival">
                    <p className="eyebrow">Light {s.step + 1} of 3</p>
                    <h2>
                      {name} <em>in {signAt(lon)}.</em>
                    </h2>
                    <span className="reveal-coordinate">{degree(lon)}</span>
                    <p>
                      {s.step === 0
                        ? "Begin with the Sun, the source tradition’s symbol of identity, purpose and creative agency."
                        : s.step === 1
                          ? "Meet the Moon, associated in this source with emotional needs, habits and instinctive responses."
                          : "Your Ascendant is the calculated rising degree on the eastern horizon. It depends on the entered time and coordinates."}
                    </p>
                  </div>
                  <SequenceMarks step={s.step} total={names.length} />
                  <button className="primary tactile" onClick={s.reveal}>
                    {s.step === 2
                      ? "Enter my reading"
                      : "Reveal the next light"}{" "}
                    <span aria-hidden="true">→</span>
                  </button>
                  <button className="text-button" onClick={s.finish}>
                    Skip reveal & read my chart
                  </button>
                </section>
              ) : (
                reading && <PlacementFocus result={r} selected={s.selected} reading={reading} onSelect={select} />
              )}
            </div>
            {s.stage === "reading" && (
              <>
                {reading && <ChartCalculations result={r} reading={reading} />}
                <section className="turning-door">
                  <div>
                    <p className="eyebrow">
                      THE SAME NATAL SKY / A NEW DIMENSION
                    </p>
                    <h2>
                      The sky
                      <br />
                      <em>keeps turning.</em>
                    </h2>
                    <p>
                      Explore the next 1–30 days through actual transit
                      contacts. Your current natal calculation is already here.
                    </p>
                    <button
                      className="primary"
                      onClick={() => setTurning(true)}
                    >
                      Enter The Turning Sky ↗
                    </button>
                  </div>
                </section>
                <SaveChapter kind="western" result={r} oracle={oracle} />
                <section className="western-commentary">
                  <p className="eyebrow">AN OPTIONAL SECOND VOICE</p>
                  <h2>Reflect with Gemini.</h2>
                  <p>
                    Separate experimental commentary on the Sun, Moon and
                    Mercury’s supplied source components. Birth date/time,
                    coordinates and timezone are excluded from the provider
                    prompt. Native truth stays unchanged.
                  </p>
                  <label className="birth-check">
                    <input
                      type="checkbox"
                      checked={s.consent}
                      onChange={(e) => s.setConsent(e.target.checked)}
                    />
                    I agree to send these source components to Google Gemini for
                    this explanation.
                  </label>
                  <button
                    className="secondary"
                    disabled={!s.consent || !oracle.gemini || s.aiBusy}
                    onClick={() => void s.explain()}
                  >
                    {s.aiBusy ? "Reflecting…" : "Request optional commentary"}
                  </button>
                  {!oracle.gemini && (
                    <p className="scope-note">
                      Gemini is not configured. Your native chart and sources
                      are complete.
                    </p>
                  )}
                  <p role="status">{s.aiError}</p>
                  {s.ai && (
                    <aside className="chart-ai">
                      <h3>Gemini commentary · separate from the sources</h3>
                      {s.ai.themes.map((t) => (
                        <p key={t.id}>
                          {t.reflection}
                          <small>{t.id}</small>
                        </p>
                      ))}
                      <p>
                        {s.ai.provenance.provider} · {s.ai.provenance.model} ·
                        experimental, not saved to My Fate.
                      </p>
                    </aside>
                  )}
                </section>
                <div className="western-actions">
                  <button className="secondary" onClick={() => exportNative(r)}>
                    Export full native chart
                  </button>
                  <button className="text-button" onClick={s.reset}>
                    Calculate another chart
                  </button>
                  <button
                    className="text-button"
                    onClick={() => oracle.navigate("numerology")}
                  >
                    Visit the room of numbers ↗
                  </button>
                </div>
                <p className="scope-note native-export-disclosure">
                  Full native export includes your entered birth details and
                  complete calculations. Codex export excludes those original
                  inputs.
                </p>
              </>
            )}
          </>
        )
      )}
    </div>
  );
}
