import { NumberDial } from "../numerology/NumberDial";
import { NumberInputForm } from "../numerology/NumberInputForm";
import { NumberReading } from "../numerology/NumberReading";
import { useNumerology } from "../numerology/useNumerology";
import { SequenceMarks } from "../components/ArtifactSurface";
import { personalCode } from "../numerology/personalCode";
import type { Oracle } from "../hooks/useOracle";
export default function NumerologyScreen({ oracle }: { oracle: Oracle }) {
  const state = useNumerology(oracle);
  const { stage, result, step, heading } = state;
  const narrative = result && personalCode(result);
  const seals = result
    ? [
        {
          value: result.expression.result,
          label: "Expression",
          text: narrative?.sections[1].passages[0].text,
        },
        {
          value: result.cycles.year.result,
          label: `Personal year · ${result.target.slice(0, 4)}`,
          text: result.readings.find((r) => r.scope === "personal_year")!.text,
        },
        {
          value: result.life_path.result,
          label: "Life Path",
          text: narrative?.sections[0].passages[0].text,
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
              Your <em>personal code.</em>
            </>
          )}
        </h1>
        <p>
          {stage === "input"
            ? "Trace the symbols held in a name and a date."
            : stage === "ritual"
              ? "Begin with the name, the year and the birth date."
              : "Read the five core numbers, then explore how they sit alongside the calendar cycles."}
        </p>
      </div>
      {stage !== "reading" && <div className="number-room-layout">
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
              : "Turn the instrument to inspect it. The number stays fixed."}
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
      </div>}
      {stage === "reading" && <NumberReading state={state} oracle={oracle} narrative={narrative} />}
    </div>
  );
}
