import { useState } from "react";
import type { Component, NatalPassage, NatalReading, WesternResult } from "./contracts";
import { aspectKey, BODY_NAMES, degree, signAt } from "./contracts";
import { ASPECT_NAMES } from "./BirthChart";
import { houseComponent } from "./source";

export function SourceDepth({ parts }: { parts: Component[] }) {
  if (!parts.length) return null;
  return (
    <details className="chart-source-depth">
      <summary>Sources and scope</summary>
      {parts.map((r) => (
        <blockquote key={r.id}>
          <p>{r.text}</p>
          <cite><a href={r.url} target="_blank" rel="noreferrer">{r.author} · {r.locator}</a></cite>
          <small>{r.id} · v{r.version} · {r.tradition}</small>
          {r.exceptions.map((exception) => <p key={exception}>{exception}</p>)}
        </blockquote>
      ))}
    </details>
  );
}

function Passages({ passages, reading, additional = [] }: {
  passages: NatalPassage[]; reading: NatalReading; additional?: Component[];
}) {
  const ids = [...new Set(passages.flatMap((passage) => passage.rule_ids))];
  return <>
    {passages.map((passage) => (
      <section className="natal-passage" key={passage.title}>
        <h3>{passage.title}</h3>
        <p>{passage.body}</p>
      </section>
    ))}
    {passages.some((passage) => passage.coverage === "editorial") && (
      <p className="scope-note">This chapter includes an editorial reading of the contacts together.</p>
    )}
    <SourceDepth parts={[...ids.map((id) => reading.sources[id]), ...additional]} />
  </>;
}

const shortTitles: Record<string, string> = {
  identity: "Identity", emotion: "Feelings", communication: "Thought",
  work: "Work", themes: "Themes", aspects: "Other aspects",
};

export function ChartReading({ result, reading }: { result: WesternResult; reading: NatalReading }) {
  const [active, setActive] = useState("identity");
  const chapter = reading.chapters.find((item) => item.id === active) ?? reading.chapters[0];
  return (
    <section className="chart-reading natal-story" aria-label="Natal reading">
      <header className="natal-intro">
        <div className="chart-core-lights natal-coordinates">
          {["Sun", "Moon", "Ascendant"].map((name) => (
            <article key={name}>
              <span className="eyebrow">{name}</span>
              <strong>{signAt(name === "Ascendant" ? result.angles.ascendant : result.planets[name].longitude)}</strong>
            </article>
          ))}
        </div>
        <p className="scope-note">A symbolic reading of your calculated birth chart.</p>
      </header>
      {chapter && <>
        <nav className="natal-chapters" aria-label="Reading chapters">
          {reading.chapters.map((item) => (
            <button key={item.id} className="text-button" aria-pressed={chapter.id === item.id}
              onClick={() => setActive(item.id)}>{shortTitles[item.id]}</button>
          ))}
        </nav>
        <div className="natal-chapter" aria-live="polite">
          <h2>{chapter.title}</h2>
          <Passages passages={chapter.passages} reading={reading} />
        </div>
      </>}
      <a className="text-button natal-chart-link" href="#western-instrument"
        onClick={(event) => {
          event.preventDefault();
          const heading = document.getElementById("western-instrument");
          heading?.scrollIntoView({block: "start"});
          heading?.focus({preventScroll: true});
        }}>Explore the chart ↓</a>
    </section>
  );
}

const aspectLabel = (aspect: WesternResult["aspects"][number]) =>
  `${aspect.bodies[0]} ${ASPECT_NAMES[aspect.angle].toLowerCase()} ${aspect.bodies[1]}`;

export function PlacementFocus({ result, selected, reading, onSelect }: {
  result: WesternResult;
  selected: string;
  reading: NatalReading;
  onSelect: (key: string) => void;
}) {
  const planet = result.planets[selected];
  const house = selected.startsWith("house:") ? Number(selected.slice(6)) : undefined;
  const occupants = house ? BODY_NAMES.filter((name) => result.planets[name].house === house) : [];
  const aspect = result.aspects.find((item) => aspectKey(item) === selected);
  const focus = reading.focuses[selected];
  const base = result.reading.placements.find((item) => item.planet === selected);
  const houseSource = house ? houseComponent(house) : undefined;
  const references = [
    ...(base?.components ?? []),
    ...(houseSource ? [houseSource] : []),
    ...(selected === "Ascendant" ? reading.chart_ruler?.rule_ids.map((id) => reading.sources[id]) ?? [] : []),
  ];
  const heading = planet ? `${selected} in ${planet.sign}`
    : aspect ? aspectLabel(aspect) : house ? `House ${house}` : `Ascendant in ${signAt(result.angles.ascendant)}`;
  return (
    <section className="placement-focus" aria-label="Selected chart detail">
      <div className="natal-inspector-controls">
        <label>Choose a house
          <select value={house ?? ""} onChange={(event) => onSelect(event.target.value ? `house:${event.target.value}` : "Ascendant")}>
            <option value="">Houses</option>
            {result.house_cusps.map((_, i) => <option key={i} value={i + 1}>House {i + 1}</option>)}
          </select>
        </label>
        <label>Choose an aspect
          <select value={aspect ? selected : ""} disabled={!result.aspects.length}
            onChange={(event) => onSelect(event.target.value || "Ascendant")}>
            <option value="">Aspects</option>
            {result.aspects.map((item) => <option key={aspectKey(item)} value={aspectKey(item)}>
              {aspectLabel(item)}{reading.focuses[aspectKey(item)]?.passages.length ? " · reading" : ""}
            </option>)}
          </select>
        </label>
        <button type="button" className="text-button" aria-pressed={selected === "Ascendant"}
          onClick={() => onSelect("Ascendant")}>Ascendant</button>
      </div>
      <div aria-live="polite">
        <h2>{heading}</h2>
        {planet && <p className="placement-coordinate">
          {degree(planet.longitude)} · House {planet.house}{planet.retrograde ? " · Retrograde" : ""}
        </p>}
        {aspect && <p className="placement-coordinate">{aspect.orb.toFixed(2)}° from exact</p>}
        {house && <p className="placement-coordinate">{degree(result.house_cusps[house - 1])} · {occupants?.length ? occupants.join(", ") : "No planets"}</p>}
        {houseSource && <p>House theme · {houseSource.text}.</p>}
        {!planet && !house && !aspect && <>
          <p className="placement-coordinate">{degree(result.angles.ascendant)}</p>
          {reading.chart_ruler && <p>
            Traditional ruler: <button className="text-button" onClick={() => onSelect(reading.chart_ruler!.body)}>
              {reading.chart_ruler.body} in {reading.chart_ruler.sign} · House {reading.chart_ruler.house}
            </button>
          </p>}
        </>}
        {focus?.passages.length ? <Passages passages={focus.passages} reading={reading} additional={references} /> : (<>
          <p>{planet && base?.missing_components.includes("planet meaning")
            ? `This edition supplies no planet-specific symbolic meaning for ${selected} in this placement.`
            : aspect ? "This contact is calculated. A direct reading for this pair and angle is outside this edition."
            : "There is no direct placement reading for this selection in this edition."}</p>
          <SourceDepth parts={references} />
        </>)}
      </div>
      {!!focus?.connections.length && (
        <ul className="natal-related" aria-label="Related interpretations">
          {focus.connections.map((key) => {
            const item = result.aspects.find((a) => aspectKey(a) === key);
            return item && <li key={key}><button className="text-button" onClick={() => onSelect(key)}>{aspectLabel(item)} ↗</button></li>;
          })}
        </ul>
      )}
    </section>
  );
}

export function ChartCalculations({ result, reading }: { result: WesternResult; reading: NatalReading }) {
  return (
    <div className="natal-chart-detail">
      {!!reading.patterns.length && (
        <details className="chart-calculations">
          <summary>Calculated chart patterns</summary>
          <p>These configurations describe the angles between planets. This edition adds no pattern-level interpretation.</p>
          {reading.patterns.map((pattern) => <p key={pattern.contacts.join("/")}>
            {pattern.kind} · {pattern.apex} at the apex · {pattern.contacts.map((key) => {
              const contact = result.aspects.find((a) => aspectKey(a) === key);
              return contact && aspectLabel(contact);
            }).join(", ")}
          </p>)}
        </details>
      )}
      <details className="chart-calculations">
        <summary>The full chart, conventions & limitations</summary>
        <p>
          Tropical · modern psychological · {result.settings.houses} houses ·
          traditional rulership. Ephemeris years 1850–2149.
        </p>
        <table>
          <caption>Native planetary positions</caption>
          <thead>
            <tr>
              <th>Body</th>
              <th>Longitude</th>
              <th>House</th>
              <th>Motion</th>
            </tr>
          </thead>
          <tbody>
            {BODY_NAMES.map((n) => (
              <tr key={n}>
                <th>{n}</th>
                <td>{result.planets[n].longitude.toFixed(6)}°</td>
                <td>{result.planets[n].house}</td>
                <td>
                  {result.planets[n].retrograde ? "Retrograde" : "Direct"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p>
          Ascendant {degree(result.angles.ascendant)} · Midheaven{" "}
          {degree(result.angles.midheaven)}
        </p>
        <p>
          Resolved UTC: {result.birth.utc}. Zone: {result.birth.zone}.
          Coordinates: {result.birth.latitude}, {result.birth.longitude}.
        </p>
        <p>{result.reading.scope}</p>
        {result.limitations.map((l, i) => (
          <p key={i}>{l}</p>
        ))}
        <p>
          The dial is a geocentric ecliptic instrument, not a literal sky
          photograph or fixed-star map. Fine markers are engraving; only
          planet/aspect paths encode calculated positions.
        </p>
        <pre>
          {JSON.stringify(
            {
              house_cusps: result.house_cusps,
              aspects: result.aspects,
              conventions: result.conventions,
              reproducibility: result.reproducibility,
            },
            null,
            2,
          )}
        </pre>
      </details>
    </div>
  );
}
