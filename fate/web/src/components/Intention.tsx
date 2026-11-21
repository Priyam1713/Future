import { ArrowRight, Check, LoaderCircle } from "lucide-react";
import CardArt from "../CardArt";
import type { Oracle } from "../hooks/useOracle";
export function Intention({ oracle }: { oracle: Oracle }) {
  const {
    busy,
    cast,
    spread,
    setSpread,
    question,
    setQuestion,
    reversals,
    setReversals,
    error,
  } = oracle;
  return (
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
              <small>Opening, middle and consideration</small>
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
            placeholder="An optional question for this visit"
          />
          <div className="question-helper">
            <span>
              For context and reflection; it doesn’t select your cards.
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
              <small>Use Waite’s entry for each orientation.</small>
            </span>
          </label>
          <p className="privacy-note">
            Your reading stays in this visit. Nothing is saved automatically or
            sent to AI.
          </p>
          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}
          <button className="primary" type="submit" disabled={busy}>
            {busy ? (
              <>
                <LoaderCircle className="spin" size={18} /> Drawing your cards…
              </>
            ) : (
              <>
                Draw {spread === "one" ? "my card" : "my three cards"}{" "}
                <ArrowRight size={17} aria-hidden="true" />
              </>
            )}
          </button>
        </fieldset>
      </form>
      <p className="scope-note">
        A symbolic practice for reflection. The cards don’t establish facts or
        predict certain events.
      </p>
    </>
  );
}
