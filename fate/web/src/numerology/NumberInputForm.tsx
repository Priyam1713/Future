import type { Numerology } from "./useNumerology";
import { EXPERIENCES } from "../experiences/contracts";
export function NumberInputForm({ state }: { state: Numerology }) {
  const { input, change, busy, error, calculate } = state;
  const ys = Array.from(input.name.matchAll(/y/gi));
  return (
    <form
      className="number-form"
      onSubmit={(e) => {
        e.preventDefault();
        void calculate();
      }}
      autoComplete="off"
    >
      <p className="eyebrow">YOUR COORDINATES</p>
      <h2>
        Every pattern
        <br />
        begins <em>somewhere.</em>
      </h2>
      <label>
        Your full name
        <input
          required
          maxLength={160}
          pattern="[A-Za-z]+(?:[-'][A-Za-z]+)*(?: +[A-Za-z]+(?:[-'][A-Za-z]+)*)*"
          value={input.name}
          onChange={(e) => change("name", e.target.value)}
          aria-describedby="name-help"
          placeholder="The name you wish to explore"
        />
      </label>
      <p id="name-help" className="field-note">
        Use Latin A–Z letters, with spaces, internal hyphens or apostrophes.
        Other scripts need your own explicit transliteration; we never convert
        silently.
      </p>
      <fieldset className="name-basis">
        <legend>This is my</legend>
        <label>
          <input
            type="radio"
            name="basis"
            checked={input.basis === "birth"}
            onChange={() => change("basis", "birth")}
          />{" "}
          Full birth name
        </label>
        <label>
          <input
            type="radio"
            name="basis"
            checked={input.basis === "current"}
            onChange={() => change("basis", "current")}
          />{" "}
          Current name
        </label>
      </fieldset>
      {input.basis === "current" && (
        <p className="field-note">
          A current-name overlay, kept separate from birth-name results.
        </p>
      )}
      {ys.length > 0 && (
        <fieldset className="y-roles">
          <legend>How does each Y sound?</legend>
          <p className="field-note">
            Choose the role of each Y in your name, from left to right. The
            engine does not guess pronunciation.
          </p>
          {ys.map((match, i) => (
            <label key={i}>
              Y {i + 1} —{" "}
              {input.name.slice(
                Math.max(0, (match.index ?? 0) - 4),
                (match.index ?? 0) + 5,
              )}
              <select
                required
                value={input.y_roles[i] ?? ""}
                onChange={(e) => {
                  const roles = Array.from(
                    { length: ys.length },
                    (_, j) => input.y_roles[j] ?? "_",
                  );
                  roles[i] = e.target.value;
                  change("y_roles", roles.join(""));
                }}
              >
                <option value="">Choose a role</option>
                <option value="v">Vowel sound</option>
                <option value="c">Consonant sound</option>
              </select>
            </label>
          ))}
        </fieldset>
      )}
      <div className="date-pair">
        <label>
          Date of birth
          <input
            type="date"
            required
            min="0001-01-01"
            max="9998-12-31"
            value={input.birth}
            onChange={(e) => change("birth", e.target.value)}
          />
        </label>
        <label>
          Date to explore
          <input
            type="date"
            required
            min="0001-01-01"
            max="9998-12-31"
            value={input.target}
            onChange={(e) => change("target", e.target.value)}
          />
        </label>
      </div>
      <p className="field-note">
        The second date sets your personal year, month and day. Annual themes
        follow the calendar year.
      </p>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      <button className="primary" disabled={busy}>
        {busy ? "Calculating your pattern…" : "Awaken my numbers"}
        <span aria-hidden="true">↗</span>
      </button>
      <p className="scope-note">
        {EXPERIENCES[4].privacy} Nothing is sent to Gemini unless you separately
        consent. Your inputs leave this page when you return to the Gallery.
      </p>
    </form>
  );
}
