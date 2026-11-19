import { useState } from "react";
import { archive, motif, titleCase } from "./reference";
import { GlassSurface } from "./GlassSurface";
import { PendulumModel } from "./PendulumModel";
import type { RitualId } from "./contracts";

type Submit = (input: object) => void;
type Props = { busy: boolean; submit: Submit; still: boolean };
const safeSeed = () => crypto.randomUUID();

export function OracleEntry({ busy, submit }: Props) {
  const [spread, setSpread] = useState("three");
  const [browse, setBrowse] = useState(false);
  return (
    <>
      <div className="oracle-entry">
        <div className="oracle-stack" aria-hidden="true">
          <i />
          <i />
          <i />
        </div>
        <div>
          <h2>Lay your cards.</h2>
          <div className="ritual-choices" role="group" aria-label="Draw size">
            {[
              ["one", "One"],
              ["three", "Three"],
              ["five", "Five"],
            ].map(([value, label]) => (
              <button
                key={value}
                aria-pressed={spread === value}
                onClick={() => setSpread(value)}
              >
                {label}
              </button>
            ))}
          </div>
          <p>Upright cards from the 36-card Lenormand collection.</p>
          <button
            className="primary"
            disabled={busy}
            onClick={() => submit({ spread, seed: safeSeed() })}
          >
            Draw the oracle cards
          </button>
        </div>
      </div>
      <details
        className="ritual-depth deck-collection"
        onToggle={(e) => setBrowse(e.currentTarget.open)}
      >
        <summary>Browse all 36 illustrations</summary>
        {browse && (
          <div className="deck-catalog">
            {archive.cards.map((c) => (
              <figure key={c.id}>
                <img
                  src={"/art/ritual-deck/" + c.id + ".webp"}
                  width="384"
                  height="500"
                  loading="lazy"
                  alt=""
                />
                <figcaption>
                  {c.number} · {c.name}
                </figcaption>
              </figure>
            ))}
          </div>
        )}
      </details>
    </>
  );
}

const directions = ["clockwise", "counterclockwise", "vertical", "horizontal"];
export function PendulumEntry({ busy, submit, still }: Props) {
  const [manual, setManual] = useState(false);
  const [yes, setYes] = useState(""),
    [no, setNo] = useState(""),
    [signal, setSignal] = useState(""),
    [quality, setQuality] = useState("full");
  return (
    <div className="pendulum-entry">
      <PendulumModel still={still} />
      <div>
        <div
          className="ritual-choices"
          role="group"
          aria-label="Pendulum protocol"
        >
          <button aria-pressed={!manual} onClick={() => setManual(false)}>
            Digital symbol
          </button>
          <button aria-pressed={manual} onClick={() => setManual(true)}>
            My observed movement
          </button>
        </div>
        {!manual ? (
          <>
            <h2>Draw a symbol.</h2>
            <p>
              The seeded draw selects yes, no or unresolved from an editorial
              distribution.
            </p>
            <button
              className="primary"
              disabled={busy}
              onClick={() => submit({ seed: safeSeed() })}
            >
              Draw a digital symbol
            </button>
          </>
        ) : (
          <form
            className="ritual-fields"
            onSubmit={(event) => {
              event.preventDefault();
              if (!signal || !yes || !no || yes === no) return;
              submit({
                calibration: [
                  { signal: yes, response: "yes" },
                  { signal: no, response: "no" },
                ],
                observations: [{ signal, quality }],
              });
            }}
          >
            <h2>Record your observation.</h2>
            <p>Use the movements you established with a physical pendulum.</p>
            <div className="two-fields">
              <label>
                My yes movement
                <select
                  value={yes}
                  onChange={(e) => setYes(e.target.value)}
                  required
                >
                  <option value="">Choose</option>
                  {directions.map((d) => (
                    <option key={d} value={d} disabled={d === no}>
                      {titleCase(d)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                My no movement
                <select
                  value={no}
                  onChange={(e) => setNo(e.target.value)}
                  required
                >
                  <option value="">Choose</option>
                  {directions.map((d) => (
                    <option key={d} value={d} disabled={d === yes}>
                      {titleCase(d)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Movement observed
                <select
                  value={signal}
                  onChange={(e) => setSignal(e.target.value)}
                  required
                >
                  <option value="">Choose</option>
                  {Object.keys(archive.pendulum.signals).map((d) => (
                    <option key={d} value={d}>
                      {titleCase(d)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Observation quality
                <select
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                >
                  {archive.pendulum.quality.map((d) => (
                    <option key={d} value={d}>
                      {titleCase(d)}
                    </option>
                  ))}
                </select>
              </label>
            </div>
            <button
              className="primary"
              disabled={busy || !signal || !yes || !no || yes === no}
            >
              Read my reported movement
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

const observationLabels: Record<string, string> = {
  observed_reflection: "A reflection",
  subjective_imagery: "Subjective imagery",
  imagined_imagery: "Deliberately imagined imagery",
  uncertain: "Something uncertain",
  no_imagery: "No imagery",
};
export function JournalEntry({
  id,
  still,
  busy,
  submit,
}: Props & { id: 21 | 22 }) {
  const [step, setStep] = useState<"look" | "journal">("look");
  const [notes, setNotes] = useState(""),
    [experience, setExperience] = useState("");
  const [surface, setSurface] = useState("unspecified");
  return (
    <div className="journal-entry">
      <div className="glass-stage">
        <GlassSurface mirror={id === 22} still={still} />
      </div>
      {step === "look" ? (
        <div className="journal-gate">
          <h2>
            {id === 21 ? "Watch the light drift." : "Let the reflections pass."}
          </h2>
          <p>
            Take a quiet moment if you like. The moving light is part of the
            illustration.
          </p>
          <button className="primary" onClick={() => setStep("journal")}>
            Open my journal
          </button>
          <button
            className="text-button"
            onClick={() =>
              submit({ session: { status: "discontinued" }, journal: [] })
            }
            disabled={busy}
          >
            Finish without an entry
          </button>
          <details className="ritual-depth">
            <summary>Prepare the space and settle your attention</summary>
            <ol>
              {archive.guides[id].steps.slice(0, 3).map((step) => (
                <li key={step.id}>{step.text}</li>
              ))}
            </ol>
          </details>
        </div>
      ) : (
        <form
          className="ritual-fields"
          onSubmit={(event) => {
            event.preventDefault();
            const journal =
              experience || notes.trim()
                ? [
                    {
                      ...(experience ? { experience_type: experience } : {}),
                      ...(notes.trim() ? { description: notes } : {}),
                      ...(experience === "uncertain"
                        ? { uncertainty: true }
                        : {}),
                    },
                  ]
                : [];
            submit({ session: { surface, status: "completed" }, journal });
          }}
        >
          <h2>What did you notice?</h2>
          <label>
            My own observation
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              maxLength={4000}
              rows={4}
              placeholder="Leave blank if you wish."
            />
          </label>
          <div className="two-fields">
            <label>
              How I describe it
              <select
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
              >
                <option value="">Leave unclassified</option>
                {archive.guides[id].types.map((type) => (
                  <option key={type} value={type}>
                    {observationLabels[type]}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Physical surface, if used
              <select
                value={surface}
                onChange={(e) => setSurface(e.target.value)}
              >
                {archive.guides[id].surfaces.map((type) => (
                  <option key={type} value={type}>
                    {titleCase(type)}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <p>
            Process these words in this visit. My Fate can save the guide only.
          </p>
          <button className="primary" disabled={busy}>
            Close the journal
          </button>
        </form>
      )}
    </div>
  );
}

const contextLabels: Record<string, string> = {
  hungry: "Were you hungry?",
  thirsty: "Were you thirsty?",
  current_fear: "Already feared while awake?",
  current_desire: "Already desired while awake?",
  at_sea: "At sea in the relevant account?",
  exact_correspondence_reported:
    "An exact correspondence you personally reported?",
  circumstances: "Historical circumstances to compare",
  staff_cases: "Staff accounts to compare",
  myth_versions: "Versions of the myth",
};
export function DreamEntry({ busy, submit }: Props) {
  const [notes, setNotes] = useState(""),
    [chosen, setChosen] = useState<string[]>([]);
  const [context, setContext] = useState<Record<string, boolean | string[]>>(
    {},
  );
  const keys = [
    ...new Set(
      chosen.flatMap((id) =>
        motif(id).reference.cases.flatMap((row) => Object.keys(row.requires)),
      ),
    ),
  ];
  const set = (key: string, value: boolean | string[] | undefined) =>
    setContext((previous) => {
      const next = { ...previous };
      if (value === undefined) delete next[key];
      else next[key] = value;
      return next;
    });
  function choose(id: string) {
    setChosen((old) =>
      old.includes(id) ? old.filter((item) => item !== id) : [...old, id],
    );
  }
  return (
    <form
      className="dream-entry ritual-fields"
      onSubmit={(e) => {
        e.preventDefault();
        submit({
          ...(notes.trim() ? { narrative: notes } : {}),
          lookups: chosen,
          context: Object.fromEntries(
            keys.flatMap((key) => {
              const value = context[key];
              if (value === undefined) return [];
              if (key === "myth_versions" && Array.isArray(value))
                return [
                  [key, [...new Set(value.filter((item) => item.trim()))]],
                ];
              return [[key, value]];
            }),
          ),
        });
      }}
    >
      <div className="dream-leaf">
        <h2>Keep a fragment.</h2>
        <label>
          My dream notes
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            maxLength={5000}
            rows={4}
            placeholder="A place, a feeling, a single detail…"
          />
        </label>
      </div>
      <fieldset>
        <legend>Which motifs would you like to look up?</legend>
        <div className="motif-options">
          {Object.keys(archive.dream.motifs).map((id) => (
            <button
              type="button"
              key={id}
              aria-pressed={chosen.includes(id)}
              onClick={() => choose(id)}
            >
              {titleCase(id)}
            </button>
          ))}
        </div>
      </fieldset>
      {!!keys.length && (
        <details className="ritual-depth" open>
          <summary>Optional context for these references</summary>
          <div className="two-fields">
            {keys.map((key) => {
              if (key === "myth_versions")
                return (
                  <fieldset key={key}>
                    <legend>{contextLabels[key]}</legend>
                    {[0, 1].map((i) => (
                      <label key={i}>
                        Version {i + 1}
                        <input
                          maxLength={220}
                          value={
                            (context[key] as string[] | undefined)?.[i] ?? ""
                          }
                          onChange={(e) => {
                            const list = [
                              ...((context[key] as string[] | undefined) ?? [
                                "",
                                "",
                              ]),
                            ];
                            list[i] = e.target.value;
                            set(key, list);
                          }}
                        />
                      </label>
                    ))}
                  </fieldset>
                );
              if (key === "staff_cases" || key === "circumstances") {
                const values =
                  key === "staff_cases"
                    ? ["initial_account", "repeat_during_paralysis"]
                    : ["perfume_trade", "civic_standing", "illness"];
                return (
                  <fieldset key={key}>
                    <legend>{contextLabels[key]}</legend>
                    {values.map((value) => (
                      <label className="ritual-check" key={value}>
                        <input
                          type="checkbox"
                          checked={(
                            (context[key] as string[] | undefined) ?? []
                          ).includes(value)}
                          onChange={(e) => {
                            const list =
                              (context[key] as string[] | undefined) ?? [];
                            set(
                              key,
                              e.target.checked
                                ? [...list, value]
                                : list.filter((item) => item !== value),
                            );
                          }}
                        />
                        {titleCase(value)}
                      </label>
                    ))}
                  </fieldset>
                );
              }
              return (
                <label key={key}>
                  {contextLabels[key]}
                  <select
                    value={
                      context[key] === true
                        ? "yes"
                        : context[key] === false
                          ? "no"
                          : ""
                    }
                    onChange={(e) =>
                      set(
                        key,
                        e.target.value ? e.target.value === "yes" : undefined,
                      )
                    }
                  >
                    <option value="">Leave unknown</option>
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                  </select>
                </label>
              );
            })}
          </div>
        </details>
      )}
      <button className="primary" disabled={busy}>
        Open my selected references
      </button>
    </form>
  );
}

export function dots(n: number) {
  return n === 1 ? "●" : n === 2 ? "● ●" : "·";
}
export function GeomancyEntry({ busy, submit }: Props) {
  const [rows, setRows] = useState(() => Array<number>(16).fill(0));
  return (
    <div className="sand-entry">
      <h2>Set the four Mothers.</h2>
      <p>
        Tap each row to cycle through empty, one dot, and two dots. Read the
        rows from top to bottom.
      </p>
      <div className="sand-mothers">
        {[0, 1, 2, 3].map((m) => (
          <fieldset key={m}>
            <legend>Mother {m + 1}</legend>
            {[0, 1, 2, 3].map((r) => {
              const i = m * 4 + r,
                n = rows[i];
              return (
                <button
                  key={i}
                  aria-label={`Mother ${m + 1}, row ${r + 1}: ${n === 0 ? "empty" : n === 1 ? "one dot" : "two dots"}`}
                  data-dots={n}
                  onClick={() =>
                    setRows((previous) =>
                      previous.map((v, k) => (k === i ? (v + 1) % 3 : v)),
                    )
                  }
                >
                  {dots(n)}
                </button>
              );
            })}
          </fieldset>
        ))}
      </div>
      <button
        className="primary"
        disabled={busy || rows.includes(0)}
        onClick={() =>
          submit({
            mothers: [0, 1, 2, 3].map((i) =>
              rows.slice(i * 4, i * 4 + 4).join(""),
            ),
          })
        }
      >
        Form the shield
      </button>
    </div>
  );
}

export function LibraryEntry({ busy, submit }: Props) {
  const [chapter, setChapter] = useState(0),
    [radius, setRadius] = useState(1),
    [pick, setPick] = useState("");
  const page = archive.book.pages[chapter];
  const selected = page.passages.find((p) => p.sentence_id === pick);
  return (
    <div className="library-entry">
      <p className="eyebrow">Ruth · World English Bible Classic</p>
      <div
        className="ritual-choices"
        role="group"
        aria-label="Logical chapter pages"
      >
        {archive.book.pages.map((p, i) => (
          <button
            key={p.id}
            aria-pressed={i === chapter}
            onClick={() => {
              setChapter(i);
              setPick("");
            }}
          >
            Ruth {p.chapter}
          </button>
        ))}
      </div>
      <div className="book-spread" key={chapter}>
        <div
          className="book-selection"
          role="group"
          aria-label={`Sentences in Ruth ${page.chapter}`}
        >
          {page.passages.map((p) => (
            <button
              type="button"
              key={p.sentence_id}
              aria-pressed={pick === p.sentence_id}
              onClick={() => setPick(p.sentence_id)}
            >
              <small>{p.citation}</small> {p.text}
            </button>
          ))}
        </div>
        <div className="book-picker">
          <h2>{selected ? selected.citation : "Choose a sentence."}</h2>
          <p>
            {selected?.text ??
              "Select a passage on the page, then open it with its nearby sentences."}
          </p>
          <label>
            Nearby sentences on each side
            <select
              value={radius}
              onChange={(e) => setRadius(Number(e.target.value))}
            >
              {[0, 1, 2].map((n) => (
                <option key={n}>{n}</option>
              ))}
            </select>
          </label>
          <button
            className="primary"
            disabled={busy || !selected}
            onClick={() =>
              selected &&
              submit({
                selections: [
                  { path: selected.path, sentence_id: selected.sentence_id },
                ],
                context: radius,
              })
            }
          >
            Read this passage
          </button>
        </div>
      </div>
    </div>
  );
}

export function RitualEntry({ id, ...props }: Props & { id: RitualId }) {
  switch (id) {
    case 17:
      return <OracleEntry {...props} />;
    case 20:
      return <PendulumEntry {...props} />;
    case 21:
    case 22:
      return <JournalEntry id={id} {...props} />;
    case 23:
      return <DreamEntry {...props} />;
    case 33:
      return <GeomancyEntry {...props} />;
    case 36:
      return <LibraryEntry {...props} />;
  }
}
