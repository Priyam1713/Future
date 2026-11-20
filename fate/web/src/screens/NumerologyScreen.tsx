import { NumberDial } from "../numerology/NumberDial";
import { NumberInputForm } from "../numerology/NumberInputForm";
import { NumberReading } from "../numerology/NumberReading";
import { useNumerology } from "../numerology/useNumerology";
import { SequenceMarks } from "../components/ArtifactSurface";
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
          text: "Your birth-date pattern.",
        },
      ]
    : [];
  const seal = seals[stage === "reading" ? 0 : step];
  return (
    <div
      className={`numerology-room page-enter stage-${stage} finished-material`}
    >
      <div className="journey-top">
        <button
          className="text-button"
          onClick={() => oracle.navigate("gallery")}
        >
          ← The Gallery
        </button>
        <span className="eyebrow">Numerology</span>
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
              Three numbers, <em>three lenses.</em>
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
              ? "Begin with the name, the year and the birth date."
              : "Your name and your year, each read through its own source."}
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
        </div>
        {stage === "input" ? (
          <NumberInputForm state={state} />
        ) : stage === "ritual" && seal ? (
          <section className="number-seal" aria-live="polite">
            <div key={step} className="artifact-arrival">
              <p className="eyebrow">Seal {step + 1} of 3</p>
              <h2>{seal.label}</h2>
              <p className="seal-theme">{seal.text}</p>
              {step === 2 && <p className="scope-note">Calculated context</p>}
            </div>
            <SequenceMarks step={step} total={seals.length} />
            <button className="primary tactile" onClick={state.reveal}>
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
