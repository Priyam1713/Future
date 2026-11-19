import { NumberDial } from "../numerology/NumberDial";
import { NumberInputForm } from "../numerology/NumberInputForm";
import { NumberReading } from "../numerology/NumberReading";
import { useNumerology } from "../numerology/useNumerology";
import type { Oracle } from "../hooks/useOracle";
export default function NumerologyScreen({ oracle }: { oracle: Oracle }) {
  const state = useNumerology(oracle);
  const { stage, result, step, heading } = state;
  const seals = result
    ? [
        {
          value: result.expression.result,
          label: "Expression",
          text: result.readings.find((r) => r.scope === "expression")!.text,
        },
        {
          value: result.cycles.year.result,
          label: `Personal year · ${result.target.slice(0, 4)}`,
          text: result.readings.find((r) => r.scope === "personal_year")!.text,
        },
        {
          value: result.life_path.result,
          label: "Birth-date pattern",
          text: "Your date, reduced through the native calculation. A framework for reflection, without a number-specific interpretation.",
        },
      ]
    : [];
  const seal = seals[stage === "reading" ? 0 : step];
  return (
    <div className={`numerology-room page-enter stage-${stage}`}>
      <div className="journey-top">
        <button
          className="text-button"
          onClick={() => oracle.navigate("explore")}
        >
          ← The Gallery
        </button>
        <span className="eyebrow">ROOM 02 / NUMEROLOGY</span>
      </div>
      <div className="number-room-heading">
        <p className="eyebrow">THE OBSERVATORY OF NUMBERS</p>
        <h1 ref={heading} tabIndex={-1}>
          {stage === "input" ? (
            <>
              The quiet geometry
              <br />
              of <em>you.</em>
            </>
          ) : stage === "ritual" ? (
            <>
              Your pattern,
              <br />
              <em>coming into light.</em>
            </>
          ) : (
            <>
              A rhythm to
              <br />
              <em>reflect on.</em>
            </>
          )}
        </h1>
        <p>
          {stage === "input"
            ? "Trace the symbols held in a name and a date."
            : stage === "ritual"
              ? "The calculation is complete. Turn each seal to meet your numbers."
              : "Two source-grounded themes. A new way to pause and consider."}
        </p>
      </div>
      <div className="number-room-layout">
        <div className="number-artifact">
          <NumberDial
            reduced={oracle.reduced}
            paused={oracle.paused}
            value={seal?.value}
            label={seal?.label}
            active={stage === "ritual"}
          />
          <p className="dial-invitation">
            {oracle.reduced || oracle.paused
              ? "A MOMENT OF STILLNESS"
              : "TOUCH TO TURN · MOVE TO CATCH THE LIGHT"}
          </p>
          <button
            className="text-button"
            aria-pressed={oracle.paused}
            onClick={() => oracle.setPaused((p) => !p)}
          >
            {oracle.paused ? "Resume atmosphere" : "Pause atmosphere"}
          </button>
        </div>
        {stage === "input" ? (
          <NumberInputForm state={state} />
        ) : stage === "ritual" && seal ? (
          <section className="number-seal" aria-live="polite">
            <p className="eyebrow">SEAL {step + 1} OF 3</p>
            <h2>{seal.label}</h2>
            <p key={step} className="seal-theme">
              {seal.text}
            </p>
            <p className="scope-note">
              {step < 2
                ? "A direct source summary, not a prediction."
                : "Calculated context · Life Path"}
            </p>
            <div className="seal-progress" aria-hidden="true">
              {seals.map((_, i) => (
                <i key={i} className={i <= step ? "lit" : ""} />
              ))}
            </div>
            <button className="primary" onClick={state.reveal}>
              {step === 2 ? "Read my constellation" : "Reveal the next seal"}{" "}
              <span aria-hidden="true">→</span>
            </button>
            <button className="text-button" onClick={state.finish}>
              Go straight to my reading
            </button>
          </section>
        ) : null}
      </div>
      {stage === "reading" && <NumberReading state={state} oracle={oracle} />}
    </div>
  );
}
