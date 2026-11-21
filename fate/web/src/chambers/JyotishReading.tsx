import { useState } from "react";
import type { VedicSnapshot } from "./contracts";
import { vedic } from "./reference";

type Passage = { title: string; text: string; rule_ids: string[]; inputs: string[] };
type Position = { dignities: string[]; ruler: string };
type Graha = {
  topic: string; house_topic: string; nodal: boolean;
  d1: Position & { rules_houses: number[]; moolatrikona: boolean | string };
  d9: Position; comparison: Passage;
  contacts: { index: number; from: string; place_from_planet: number; target_sign: string; targets: string[] }[];
};
type Period = { lord: string; start_inclusive_utc: string; end_exclusive_utc: string };
export type JyotishReading = {
  profile: string; lagna_lord: string; chapters: Passage[];
  grahas: Record<string, Graha>;
  timing: { target: string; year_days: number; main: Period[]; sub: Period[]; upcoming: (Period & {mahadasa_lord: string})[] };
  sources: Record<string, { url: string; locator: string; edition: string }>;
};

function Depth({ reading, ids }: { reading: JyotishReading; ids: string[] }) {
  return <details className="chamber-depth">
    <summary>Sources and scope</summary>
    <ul>{[...new Set(ids)].map((id) => {
      const source = reading.sources[id];
      return <li key={id}><a href={source.url} target="_blank" rel="noreferrer">{source.locator}</a>
        <small>{source.edition} · {id}</small></li>;
    })}</ul>
  </details>;
}

export function JyotishOpening({ reading }: { reading: JyotishReading }) {
  const [rising] = reading.chapters;
  return <section className="jyotish-opening" aria-label="Jyotish reading">
    <p className="eyebrow">Lagna and its lord</p>
    <h2>The rising pattern</h2>
    <p>{rising.text}</p>
    <Depth reading={reading} ids={rising.rule_ids} />
  </section>;
}

export function LunarReading({ reading }: {reading: JyotishReading}) {
  const lunar = reading.chapters[1];
  return <>
    <p>{lunar.text}</p>
    <Depth reading={reading} ids={lunar.rule_ids} />
  </>;
}

const dignities: Record<string, string> = {
  own_sign: "Own sign", exaltation_sign: "Exaltation sign", debilitation_sign: "Debilitation sign",
};
export function GrahaReading({ reading, graha, s }: {reading: JyotishReading; graha: string; s: VedicSnapshot}) {
  const evidence = reading.grahas[graha];
  const row = s.planets[vedic.grahas.indexOf(graha)];
  return <section className="jyotish-graha" aria-live="polite">
    <h3>{graha} across the two charts</h3>
    <dl className="jyotish-pair">
      <div><dt>Rashi · D1</dt><dd>{vedic.signs[row[1]]} · House {row[2]}</dd>
        <dd>{evidence.d1.dignities.map((flag) => dignities[flag]).join(" · ") || "No supported sign dignity"}{evidence.d1.moolatrikona === true && " · Moolatrikona"}</dd></div>
      <div><dt>Navamsa · D9</dt><dd>{vedic.signs[row[4]]} · House {row[5]}</dd>
        <dd>{evidence.d9.dignities.map((flag) => dignities[flag]).join(" · ") || "No supported sign dignity"}</dd></div>
    </dl>
    <p>{evidence.comparison.text}</p>
    <p>Rao associates {graha} with {evidence.topic}. Its Rashi placement brings up the house topics of {evidence.house_topic}.</p>
    <p>{evidence.nodal ? "This profile leaves nodal ownership, dignity and outgoing aspects open." :
      `In Rashi, ${graha} rules ${evidence.d1.rules_houses.length === 1 ? "house" : "houses"} ${evidence.d1.rules_houses.join(" and ")}.`}</p>
    <details className="chamber-depth">
      <summary>Graha drishti and placement details</summary>
      <p>Sign rulers · {evidence.d1.ruler} in D1, {evidence.d9.ruler} in D9. D9 describes a symbolic house frame. Degree-specific dignity stays with D1.</p>
      {typeof evidence.d1.moolatrikona === "string" && !evidence.nodal &&
        <p>The source’s Mars interval is disputed and remains open.</p>}
      {!!evidence.contacts.length && <ul>{evidence.contacts.map((edge) =>
        <li key={edge.index}>{edge.from} looks to {edge.target_sign} from {edge.place_from_planet} signs away by inclusive count
          {edge.targets.length ? ` · ${edge.targets.join(", ")}` : ""}.</li>)}</ul>}
    </details>
    <Depth reading={reading} ids={[...evidence.comparison.rule_ids, "fate.jyotish.v1.grahas", "fate.jyotish.v1.houses", "vedic.drishti"]} />
  </section>;
}

const exact = (stamp: string) => stamp.replace("T", " ").replace("+00:00", " UTC");
function PeriodBounds({ period }: { period: Period }) {
  return <dl className="jyotish-bounds">
    <div><dt>Begins · inclusive</dt><dd><time dateTime={period.start_inclusive_utc}>{exact(period.start_inclusive_utc)}</time></dd></div>
    <div><dt>Ends · exclusive</dt><dd><time dateTime={period.end_exclusive_utc}>{exact(period.end_exclusive_utc)}</time></dd></div>
  </dl>;
}

export function JyotishTimeline({ reading, active }: { reading: JyotishReading; active: number }) {
  const { main, sub, upcoming, target, year_days } = reading.timing;
  const [selected, setSelected] = useState(active);
  const [following, setFollowing] = useState("");
  const period = sub[selected];
  const span = Date.parse(main[0].end_exclusive_utc) - Date.parse(main[0].start_inclusive_utc);
  const position = 100 * (Date.parse(target) - Date.parse(main[0].start_inclusive_utc)) / span;
  const mainGraha = reading.grahas[main[0].lord];
  const subGraha = reading.grahas[period.lord];
  const periodReading = reading.chapters[2];
  const future = following.startsWith("main:") ? main[Number(following.slice(5))]
    : following.startsWith("sub:") ? upcoming[Number(following.slice(4))] : undefined;
  return <section className="dasha-rail jyotish-timeline" aria-label="Vimshottari timeline">
    <p className="eyebrow">Vimshottari · {year_days === 360 ? "Savana year" : "Solar year"}</p>
    <h3>{main[0].lord} main period</h3>
    <p>{sub[active].lord} subperiod at <time dateTime={target}>{exact(target)}</time></p>
    <details className="chamber-depth"><summary>Main period boundaries</summary><PeriodBounds period={main[0]} /></details>
    <div className="jyotish-scale" aria-hidden="true">
      {sub.map((item, i) => <span key={item.lord} data-selected={i === selected} style={{
        flexGrow: Date.parse(item.end_exclusive_utc) - Date.parse(item.start_inclusive_utc),
      }} />)}
      <i style={{left: `${position}%`}} />
    </div>
    <div className="chamber-switch jyotish-periods" role="group" aria-label="Explore subperiods">
      {sub.map((item, i) => <button key={item.lord} aria-pressed={i === selected} onClick={() => setSelected(i)}>{item.lord}</button>)}
    </div>
    <div className="chamber-measure" aria-live="polite">
      <h4>{period.lord} subperiod</h4>
      <PeriodBounds period={period} />
      <p>{selected === active ? periodReading.text :
        `The main lord’s Rashi house concerns ${mainGraha.house_topic}. This subperiod’s lord brings the house topic of ${subGraha.house_topic} into view.`}</p>
    </div>
    <details className="chamber-depth">
      <summary>Upcoming main periods and subdivisions</summary>
      <label className="jyotish-upcoming">Choose an upcoming period
        <select value={following} onChange={(event) => setFollowing(event.target.value)}>
          <option value="">Upcoming periods</option>
          <optgroup label="Main periods">
            {main.slice(1).map((item, index) => <option key={item.start_inclusive_utc} value={`main:${index + 1}`}>
              {item.lord} · {item.start_inclusive_utc.slice(0, 10)}
            </option>)}
          </optgroup>
          <optgroup label="Subperiods">
            {upcoming.map((item, index) => <option key={item.start_inclusive_utc} value={`sub:${index}`}>
              {item.mahadasa_lord} / {item.lord} · {item.start_inclusive_utc.slice(0, 10)}
            </option>)}
          </optgroup>
        </select>
      </label>
      {future && <div aria-live="polite">
        <PeriodBounds period={future} />
        <p>{future.lord} returns the reading to its Rashi house, with the topic of {reading.grahas[future.lord].house_topic}.</p>
      </div>}
    </details>
    <p className="scope-note">All boundaries are shown in UTC. The symbolic topics are separate from the calculated times.</p>
    <Depth reading={reading} ids={periodReading.rule_ids} />
  </section>;
}
