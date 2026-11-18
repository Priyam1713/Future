import { createRoot } from "react-dom/client";
import { useEffect, useRef, useState, lazy, Suspense } from "react";
import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  Check,
  ChevronDown,
  Compass,
  Download,
  Info,
  LoaderCircle,
  Pause,
  Play,
  Sparkles,
  Volume2,
  VolumeX,
  X,
} from "lucide-react";
import CardArt from "./CardArt";
import { useSound } from "./useSound";
import {
  api,
  type Draw,
  type Envelope,
  type Commentary,
  type Card,
} from "./types";
import "./style.css";
const Orb = lazy(() => import("./Orb"));
const previewCard: Card = {
  id: "major-17",
  name: "The Star",
  number: 17,
  suit: null,
  rank: "trump",
  rank_number: null,
  arcana: "major",
};
const moonCard: Card = {
  ...previewCard,
  id: "major-18",
  name: "The Moon",
  number: 18,
};
type Screen = "explore" | "ritual" | "reading";
function App() {
  const [screen, setScreen] = useState<Screen>("explore");
  const [spread, setSpread] = useState<"one" | "three">("three");
  const [question, setQuestion] = useState(""),
    [reversals, setReversals] = useState(true);
  const [envelope, setEnvelope] = useState<Envelope | null>(null),
    [draw, setDraw] = useState<Draw | null>(null);
  const [revealed, setRevealed] = useState<number[]>([]),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const [reduced, setReduced] = useState(
      () => matchMedia("(prefers-reduced-motion: reduce)").matches,
    ),
    [paused, setPaused] = useState(false);
  const [consent, setConsent] = useState(false),
    [ai, setAi] = useState<Commentary | null>(null),
    [aiBusy, setAiBusy] = useState(false),
    [aiError, setAiError] = useState("");
  const [gemini, setGemini] = useState(false);
  const dialog = useRef<HTMLDialogElement>(null),
    heading = useRef<HTMLHeadingElement>(null),
    seed = useRef(""),
    inflight = useRef(false),
    controller = useRef<AbortController | null>(null),
    aiController = useRef<AbortController | null>(null);
  const sound = useSound();
  const result = envelope?.result;
  function navigate(next: Screen) {
    history.pushState(null, "", next === "explore" ? "#explore" : `#${next}`);
    setScreen(next);
    setError("");
  }
  useEffect(() => {
    const fn = () => {
      const name = location.hash.slice(1);
      setScreen(
        name === "ritual"
          ? "ritual"
          : name === "reading" && envelope
            ? "reading"
            : "explore",
      );
    };
    window.addEventListener("popstate", fn);
    return () => window.removeEventListener("popstate", fn);
  }, [envelope]);
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
    heading.current?.focus({ preventScroll: true });
  }, [screen]);
  useEffect(() => {
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => setReduced(media.matches);
    media.addEventListener("change", change);
    void api<{ gemini_available: boolean }>("/api/health")
      .then((r) => setGemini(r.gemini_available))
      .catch(() => {});
    return () => {
      media.removeEventListener("change", change);
      controller.current?.abort();
      aiController.current?.abort();
    };
  }, []);
  function begin() {
    sound.cue("select");
    if (!envelope) {
      seed.current = "";
      setDraw(null);
    }
    navigate("ritual");
  }
  function fresh() {
    aiController.current?.abort();
    setAiBusy(false);
    setEnvelope(null);
    setDraw(null);
    setAi(null);
    setAiError("");
    setConsent(false);
    setRevealed([]);
    seed.current = "";
    navigate("ritual");
  }
  async function cast() {
    if (inflight.current) return;
    inflight.current = true;
    setBusy(true);
    setError("");
    if (!seed.current) {
      const bytes = crypto.getRandomValues(new Uint8Array(32));
      seed.current = Array.from(bytes, (b) =>
        b.toString(16).padStart(2, "0"),
      ).join("");
    }
    const request: Draw = { spread, question, reversals, seed: seed.current };
    const abort = new AbortController();
    controller.current = abort;
    const timeout = setTimeout(() => abort.abort(), 20000);
    try {
      const response = await api<Envelope>(
        "/api/readings",
        request,
        abort.signal,
      );
      setEnvelope(response);
      setDraw(request);
      setRevealed([]);
      sound.cue("select");
    } catch (e) {
      setError(
        e instanceof Error && e.name !== "AbortError"
          ? e.message
          : "The connection faded. Try again with the same draw; your question is still here.",
      );
    } finally {
      clearTimeout(timeout);
      inflight.current = false;
      setBusy(false);
    }
  }
  function reveal(index: number) {
    if (revealed.includes(index)) return;
    setRevealed((prev) => (prev.includes(index) ? prev : [...prev, index]));
    sound.cue("reveal");
  }
  function readAll() {
    if (result) setRevealed(result.readings.map((_, i) => i));
    navigate("reading");
  }
  function download() {
    if (!result) return;
    const blob = new Blob(
      [
        JSON.stringify(
          {
            application: "FATE · Block 01",
            artwork: "Original FATE celestial edition; Waite text profile",
            ...result,
          },
          null,
          2,
        ),
      ],
      { type: "application/json" },
    );
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `fate-tarot-${result.replay.seed.slice(0, 8)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function explain() {
    if (!consent || !draw || !envelope || aiBusy) return;
    setAiBusy(true);
    setAiError("");
    const abort = new AbortController();
    aiController.current = abort;
    const timeout = setTimeout(() => abort.abort(), 130000);
    try {
      setAi(
        await api<Commentary>(
          "/api/explain",
          { draw, receipt: envelope.receipt, cloud_consent: consent },
          abort.signal,
        ),
      );
    } catch (e) {
      if (!abort.signal.aborted)
        setAiError(
          e instanceof Error
            ? e.message
            : "Commentary unavailable. Your native reading is still here.",
        );
      else
        setAiError("Commentary timed out. Your native reading is still here.");
    } finally {
      clearTimeout(timeout);
      setAiBusy(false);
    }
  }
  const allRevealed = !!result && revealed.length === result.readings.length;
  return (
    <div className={`app ${reduced || paused ? "still" : ""}`}>
      <a
        className="skip"
        href="#main"
        onClick={(event) => {
          event.preventDefault();
          document.getElementById("main")?.focus();
        }}
      >
        Skip to content
      </a>
      <header className="masthead">
        <a
          href="#explore"
          className="wordmark"
          onClick={(e) => {
            e.preventDefault();
            navigate("explore");
          }}
          aria-label="FATE home"
        >
          <img src="/art/fate_sigil.svg" alt="" width="34" height="34" />
          <span>FATE</span>
        </a>
        <span className="masthead-caption">THE FUTURE IS YOURS TO EXPLORE</span>
        <div className="header-actions">
          <button
            className="icon-button"
            aria-label={sound.on ? "Mute sound" : "Enable sound"}
            aria-pressed={sound.on}
            onClick={() => void sound.toggle()}
          >
            {sound.on ? <Volume2 size={18} /> : <VolumeX size={18} />}
          </button>
          <button
            className="icon-button"
            aria-label="About FATE and settings"
            onClick={() => dialog.current?.showModal()}
          >
            <Info size={18} />
          </button>
        </div>
      </header>
      <main id="main" tabIndex={-1}>
        {screen === "explore" ? (
          <div className="explore page-enter">
            <div className="hero">
              <div className="hero-copy">
                <p className="eyebrow">
                  <span className="tiny-star">✧</span> THE LIVING ORACLE
                </p>
                <h1 ref={heading} tabIndex={-1}>
                  Some answers
                  <br />
                  begin with <em>wonder.</em>
                </h1>
                <p className="hero-description">
                  A quiet moment. An ancient tradition.
                  <br />A different way to see what lies ahead.
                </p>
                <a
                  className="primary desktop-cta"
                  href="#ritual"
                  onClick={(e) => {
                    e.preventDefault();
                    begin();
                  }}
                >
                  Enter the oracle <ArrowRight size={17} />
                </a>
                <p className="hero-footnote desktop-cta">
                  No account. Just your curiosity.
                </p>
              </div>
              <div className="hero-art">
                <span className="orb-coordinate coordinate-left">
                  EST. IN WONDER
                </span>
                <div className="orb-wrap">
                  <Suspense
                    fallback={
                      <div className="orb">
                        <div className="orb-fallback">
                          <img src="/art/fate_orb_core.png" alt="" />
                          <img src="/art/fate_orrery.svg" alt="" />
                        </div>
                      </div>
                    }
                  >
                    <Orb reduced={reduced} paused={paused} />
                  </Suspense>
                </div>
                <div className="orb-caption">
                  <span /> TOUCH THE MYSTERY <span />
                </div>
                <button
                  className="motion-control"
                  aria-pressed={paused}
                  onClick={() => setPaused((p) => !p)}
                >
                  {paused ? <Play size={12} /> : <Pause size={12} />}{" "}
                  {paused ? "Resume atmosphere" : "Pause atmosphere"}
                </button>
              </div>
            </div>
            <section className="oracle-section" aria-labelledby="oracle-title">
              <div className="section-label">
                <span>01 / YOUR FIRST CHAPTER</span>
                <span>AN ANCIENT ART, REIMAGINED</span>
              </div>
              <a
                href="#ritual"
                onClick={(e) => {
                  e.preventDefault();
                  begin();
                }}
                className="oracle-tile"
              >
                <div className="tile-art" aria-hidden="true">
                  <div className="mini-card back-preview">
                    <CardArt card={moonCard} />
                  </div>
                  <div className="mini-card front-preview">
                    <CardArt card={previewCard} />
                  </div>
                  <span className="tile-glow" />
                </div>
                <div className="tile-copy">
                  <p className="eyebrow">THE ART OF REFLECTION</p>
                  <h2 id="oracle-title">The Tarot</h2>
                  <p>
                    Let the cards open
                    <br className="mobile-break" /> a new perspective.
                  </p>
                  <span className="tile-meta">
                    78 CARDS <span>·</span> ONE MOMENT OF POSSIBILITY
                  </span>
                </div>
                <span className="tile-arrow">
                  <ArrowUpRight size={22} />
                </span>
              </a>
            </section>
            <div className="explore-invitation">
              <span className="gold-star">✦</span>
              <p>
                You don’t need to know the question.
                <br />
                Sometimes, curiosity is enough.
              </p>
            </div>
            <div className="mobile-cta">
              <button className="primary" onClick={begin}>
                Begin a reading <ArrowRight size={17} />
              </button>
              <span>No account. Just your curiosity.</span>
            </div>
          </div>
        ) : screen === "ritual" ? (
          <div className="ritual page-enter narrow">
            <div className="journey-top">
              <button
                className="text-button"
                onClick={() => navigate("explore")}
              >
                <ArrowLeft size={15} /> Explore
              </button>
              <span className="eyebrow">
                01 <span className="journey-line" />{" "}
                {result ? "REVEAL" : "THE RITUAL"}
              </span>
            </div>
            <div className="page-heading">
              <p className="eyebrow">THE TAROT · WAITE TRADITION</p>
              <h1 ref={heading} tabIndex={-1}>
                {result ? (
                  "A moment of revelation."
                ) : (
                  <>
                    Make room for
                    <br />
                    <em>a little clarity.</em>
                  </>
                )}
              </h1>
              <p>
                {result
                  ? "Turn each card. Notice what speaks to you."
                  : "Bring a question, or simply bring yourself."}
              </p>
            </div>
            {!result ? (
              <>
                <div className="ritual-deck" aria-hidden="true">
                  <div>
                    <CardArt back />
                  </div>
                  <div>
                    <CardArt back />
                  </div>
                  <div>
                    <CardArt back />
                  </div>
                </div>
                <form
                  className="intention"
                  onSubmit={(e) => {
                    e.preventDefault();
                    void cast();
                  }}
                >
                  <fieldset disabled={busy}>
                    <legend>Choose your reading</legend>
                    <div className="spread-options">
                      <label className={spread === "one" ? "selected" : ""}>
                        <input
                          type="radio"
                          name="spread"
                          value="one"
                          checked={spread === "one"}
                          onChange={() => setSpread("one")}
                        />
                        <span className="spread-icon">Ⅰ</span>
                        <strong>One card</strong>
                        <small>A single point of focus</small>
                        {spread === "one" && <Check size={14} />}
                      </label>
                      <label className={spread === "three" ? "selected" : ""}>
                        <input
                          type="radio"
                          name="spread"
                          value="three"
                          checked={spread === "three"}
                          onChange={() => setSpread("three")}
                        />
                        <span className="spread-icon">Ⅲ</span>
                        <strong>Three cards</strong>
                        <small>A story to reflect on</small>
                        {spread === "three" && <Check size={14} />}
                      </label>
                    </div>
                    <label className="question-label" htmlFor="question">
                      What’s on your mind? <span>OPTIONAL</span>
                    </label>
                    <textarea
                      id="question"
                      value={question}
                      maxLength={1000}
                      rows={3}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder="What might help me see my next chapter differently?"
                    />
                    <div className="question-helper">
                      <span>
                        For context and reflection; it doesn’t select your
                        cards.
                      </span>
                      <span>{question.length}/1000</span>
                    </div>
                    <label className="check-label reversal-control">
                      <input
                        type="checkbox"
                        checked={reversals}
                        onChange={(e) => setReversals(e.target.checked)}
                      />
                      <span>
                        Include reversed cards{" "}
                        <small>
                          A different meaning, not simply an opposite.
                        </small>
                      </span>
                    </label>
                    <p className="privacy-note">
                      Your reading stays in this visit. Nothing is saved
                      automatically or sent to AI.
                    </p>
                    {error && (
                      <p className="error" role="alert">
                        {error}
                      </p>
                    )}
                    <button className="primary" type="submit" disabled={busy}>
                      {busy ? (
                        <>
                          <LoaderCircle className="spin" size={18} /> Drawing
                          your cards…
                        </>
                      ) : (
                        <>
                          Draw {spread === "one" ? "my card" : "my three cards"}{" "}
                          <Sparkles size={17} />
                        </>
                      )}
                    </button>
                  </fieldset>
                </form>
                <p className="scope-note">
                  A symbolic practice for reflection. The cards don’t establish
                  facts or predict certain events.
                </p>
              </>
            ) : (
              <>
                {result.question && (
                  <p className="question-echo">“{result.question}”</p>
                )}
                <div
                  className={`reveal-spread count-${result.readings.length}`}
                >
                  {result.readings.map((r, i) => (
                    <div className="reveal-slot" key={r.card.id}>
                      <p className="position-label">
                        {String(i + 1).padStart(2, "0")} <span />
                        {r.position.label}
                      </p>
                      <button
                        className={`flip-card ${revealed.includes(i) ? "flipped" : ""}`}
                        aria-label={
                          revealed.includes(i)
                            ? `${r.card.name}, ${r.orientation}`
                            : `Reveal card ${i + 1}`
                        }
                        aria-pressed={revealed.includes(i)}
                        onClick={() => reveal(i)}
                      >
                        <span className="flip-inner">
                          <span
                            className="card-face card-back"
                            aria-hidden={revealed.includes(i)}
                          >
                            <CardArt back />
                          </span>
                          <span
                            className="card-face card-front"
                            aria-hidden={!revealed.includes(i)}
                          >
                            <span
                              className={
                                r.orientation === "reversed"
                                  ? "reversed-art"
                                  : ""
                              }
                            >
                              <CardArt card={r.card} />
                            </span>
                          </span>
                        </span>
                      </button>
                      <div
                        className={`card-caption ${revealed.includes(i) ? "visible" : ""}`}
                        aria-hidden={!revealed.includes(i)}
                      >
                        <h2>
                          {revealed.includes(i) ? r.card.name : "Unrevealed"}
                        </h2>
                        <p>
                          {revealed.includes(i) ? r.orientation : "Tap to turn"}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="ritual-status" role="status" aria-live="polite">
                  {allRevealed
                    ? "Your cards are here. Take a breath."
                    : `${revealed.length} of ${result.readings.length} revealed · tap a card to turn it`}
                </div>
                {revealed.length > 0 && (
                  <div className="reveal-insight" key={revealed.at(-1)}>
                    <span className="eyebrow">
                      {result.readings[revealed.at(-1)!].position.label}
                    </span>
                    <p>
                      {result.readings[
                        revealed.at(-1)!
                      ].direct_component.symbolic_focus
                        .split(";")
                        .join(" · ")}
                    </p>
                    <small>Source-derived motifs · a symbolic lens</small>
                  </div>
                )}
                <div className="ritual-actions">
                  <button
                    className={allRevealed ? "primary" : "secondary"}
                    onClick={readAll}
                  >
                    {allRevealed ? "Open my reading" : "Skip reveal & read now"}{" "}
                    <ArrowRight size={17} />
                  </button>
                </div>
                <p className="scope-note">
                  One digital draw, already complete. Turning the cards never
                  changes the result.
                </p>
              </>
            )}
          </div>
        ) : result ? (
          <div className="reading page-enter narrow">
            <div className="journey-top">
              <button
                className="text-button"
                onClick={() => navigate("ritual")}
              >
                <ArrowLeft size={15} /> Your cards
              </button>
              <span className="eyebrow">
                02 <span className="journey-line" /> THE READING
              </span>
            </div>
            <div className="page-heading">
              <p className="eyebrow">A NEW PERSPECTIVE</p>
              <h1 ref={heading} tabIndex={-1}>
                The story in <em>your cards.</em>
              </h1>
              <p>Symbols to sit with. Possibilities to consider.</p>
            </div>
            {result.question && (
              <p className="question-echo">“{result.question}”</p>
            )}
            <div
              className={`reading-art count-${result.readings.length}`}
              aria-hidden="true"
            >
              {result.readings.map((r) => (
                <div
                  key={r.card.id}
                  className={r.orientation === "reversed" ? "reversed-art" : ""}
                >
                  <CardArt card={r.card} />
                </div>
              ))}
            </div>
            <section className="reading-summary" aria-labelledby="themes-title">
              <p className="eyebrow">YOUR READING AT A GLANCE</p>
              <h2 id="themes-title">Threads to follow</h2>
              {result.readings.map((r) => (
                <div className="theme-row" key={r.card.id}>
                  <span>{r.position.label}</span>
                  <strong>
                    {r.direct_component.symbolic_focus.split(";").join(" · ")}
                  </strong>
                </div>
              ))}
              <p className="summary-footnote">
                Source-derived motifs, arranged as a reflection. These positions
                are an editorial frame, not evidence of events.
              </p>
            </section>
            <div className="section-label depth-label">
              <span>LOOK A LITTLE DEEPER</span>
              <ChevronDown size={15} />
            </div>
            {result.readings.map((r, i) => (
              <section className="interpretation" key={r.card.id}>
                <div className="interpretation-heading">
                  <span className="chapter-number">0{i + 1}</span>
                  <div>
                    <span className="eyebrow">{r.position.label}</span>
                    <h2>{r.card.name}</h2>
                  </div>
                  <span className="orientation-pill">{r.orientation}</span>
                </div>
                <p className="reflection">
                  {r.composition.reflection.replaceAll(";", ", ")}
                </p>
                <details>
                  <summary>
                    The traditional meaning <ChevronDown size={16} />
                  </summary>
                  <div className="detail-body">
                    <p className="source-label">
                      HISTORICAL WORDING · WAITE, 1922
                    </p>
                    <blockquote>{r.direct_component.text}</blockquote>
                    <a
                      href={r.direct_component.page_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {r.direct_component.locator} <ArrowUpRight size={12} />
                    </a>
                    {r.upright_reference && (
                      <>
                        <p className="source-label">
                          UPRIGHT REFERENCE FOR THIS REVERSAL
                        </p>
                        <p>{r.upright_reference.text}</p>
                      </>
                    )}
                    <p className="source-caution">
                      Historical language may contain claims about health,
                      appearance or fate. It is recorded as doctrine, never a
                      finding about you.
                    </p>
                    {r.additional_source_account && (
                      <details className="nested-detail">
                        <summary>
                          Separate source account <ChevronDown size={14} />
                        </summary>
                        <p>{r.additional_source_account.text}</p>
                        <small>
                          {r.additional_source_account.locator} · retained
                          separately, not applied to this reading.
                        </small>
                      </details>
                    )}
                    {r.ambiguity.length > 0 && (
                      <ul className="source-flags">
                        {r.ambiguity.map((v) => (
                          <li key={v}>{v.replaceAll("_", " ")}</li>
                        ))}
                      </ul>
                    )}
                    <p className="rule-reference">
                      {r.direct_component.rule_id} · v
                      {r.direct_component.version}
                    </p>
                  </div>
                </details>
              </section>
            ))}
            <section className="ai-section">
              <div className="ai-heading">
                <Sparkles size={20} />
                <span className="eyebrow">AN OPTIONAL SECOND VOICE</span>
                <span className="experimental">EXPERIMENTAL</span>
              </div>
              <h2>A gentler way into the symbols.</h2>
              <p>
                Ask Gemini to put these source-linked themes into everyday
                language. Your cards and their meanings stay the source of
                truth.
              </p>
              {ai ? (
                <div className="commentary" aria-live="polite">
                  {ai.cards.map((c, i) => (
                    <div key={c.card_id}>
                      <h3>{result.readings[i].card.name}</h3>
                      <p>{c.reflection}</p>
                      <small>Grounding: {c.rule_id}</small>
                    </div>
                  ))}
                  <p className="source-caution">
                    AI commentary may be mistaken. Refer to the traditional
                    meanings above. {ai.provenance.provider} ·{" "}
                    {ai.provenance.model}
                  </p>
                  <button
                    className="text-button"
                    onClick={() => {
                      setAi(null);
                      setConsent(false);
                    }}
                  >
                    Dismiss commentary <X size={14} />
                  </button>
                </div>
              ) : gemini ? (
                <>
                  <label className="check-label">
                    <input
                      type="checkbox"
                      checked={consent}
                      onChange={(e) => setConsent(e.target.checked)}
                      disabled={aiBusy}
                    />
                    <span>
                      I agree to send my question, cards and source meanings to
                      Google Gemini for this explanation.
                    </span>
                  </label>
                  <button
                    className="secondary"
                    disabled={!consent || aiBusy}
                    onClick={() => void explain()}
                  >
                    {aiBusy ? (
                      <>
                        <LoaderCircle size={16} className="spin" /> Listening to
                        the symbols…
                      </>
                    ) : (
                      <>
                        Explain my reading <ArrowUpRight size={16} />
                      </>
                    )}
                  </button>
                  {aiError && (
                    <p className="error" role="alert">
                      {aiError}
                    </p>
                  )}
                </>
              ) : (
                <p className="availability">
                  Gemini isn’t configured on this instance. Your complete
                  reading is available above.
                </p>
              )}
            </section>
            <details className="provenance">
              <summary>
                Sources, conventions & limits <ChevronDown size={16} />
              </summary>
              <div className="detail-body">
                <p>{result.source.edition}</p>
                <p>
                  <strong>Text profile:</strong> {result.profile}
                </p>
                <p>
                  <strong>Art:</strong> Original FATE celestial edition. These
                  illustrations are contemporary symbolic designs, not
                  reproductions of historical Waite–Smith cards.
                </p>
                <p>{result.overall.summary}</p>
                <p>
                  <strong>Draw protocol:</strong> {result.replay.protocol}.
                  Cryptographically generated local seed; the native engine uses
                  its frozen deterministic draw protocol.
                </p>
                <p className="seed">Replay seed: {result.replay.seed}</p>
                <ul>
                  {result.limitations.map((l) => (
                    <li key={l}>{l}</li>
                  ))}
                </ul>
                <p>{result.predictive_validity}</p>
                <p>{result.source.rights_note}</p>
              </div>
            </details>
            <div className="reading-actions">
              <button className="secondary" onClick={download}>
                <Download size={16} /> Export native reading
              </button>
              <button className="primary" onClick={fresh}>
                Begin another chapter <ArrowRight size={16} />
              </button>
            </div>
            <p className="scope-note">
              This visit only. Export to keep your reading; nothing is saved
              automatically.
            </p>
          </div>
        ) : null}
      </main>
      <footer>
        <img src="/art/fate_sigil.svg" alt="" width="22" height="22" />
        <p>A little mystery. A new perspective.</p>
        <span>SYMBOLIC REFLECTION · NOT A CERTAIN FORECAST</span>
        <button
          className="text-button"
          onClick={() => dialog.current?.showModal()}
        >
          About this experience <ArrowUpRight size={12} />
        </button>
      </footer>
      <dialog
        ref={dialog}
        className="settings-dialog"
        onClick={(e) => {
          if (e.target === dialog.current) dialog.current?.close();
        }}
      >
        <button
          className="icon-button close-dialog"
          aria-label="Close settings"
          onClick={() => dialog.current?.close()}
        >
          <X size={20} />
        </button>
        <img src="/art/fate_sigil.svg" alt="" width="44" height="44" />
        <p className="eyebrow">FATE · THE LIVING ORACLE</p>
        <h2>A space for wonder.</h2>
        <p>
          Tarot is a symbolic tradition, not an empirically validated forecast.
          FATE uses the existing Future engine’s Waite 1922 text profile, with
          original celestial artwork.
        </p>
        <p>
          No account or automatic storage. Your question is processed by this
          server to draw a reading. It reaches Google only if you explicitly
          request Gemini commentary.
        </p>
        <div className="settings-row">
          <span>Atmosphere</span>
          <button className="secondary" onClick={() => setPaused((p) => !p)}>
            {paused ? "Resume motion" : "Pause motion"}
          </button>
        </div>
        <p className="settings-note">
          {reduced
            ? "Your device’s reduced-motion preference is active."
            : "Your device’s reduced-motion preference is respected."}
        </p>
        <div className="settings-row">
          <span>Sound</span>
          <button className="secondary" onClick={() => void sound.toggle()}>
            {sound.on ? "Turn off" : "Turn on"}
          </button>
        </div>
        <label className="volume-label">
          Ambient volume{" "}
          <input
            type="range"
            min="0"
            max="0.4"
            step="0.01"
            value={sound.music}
            onChange={(e) => sound.setMusic(Number(e.target.value))}
          />
        </label>
        <label className="volume-label">
          Card & selection volume{" "}
          <input
            type="range"
            min="0"
            max="0.6"
            step="0.01"
            value={sound.effects}
            onChange={(e) => sound.setEffects(Number(e.target.value))}
          />
        </label>
        <div className="about-colophon">
          <Compass size={16} /> CHAPTER 01 · BUILT FOR CURIOSITY
        </div>
      </dialog>
    </div>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
