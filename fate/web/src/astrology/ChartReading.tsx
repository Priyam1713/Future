import type { Component, WesternResult } from "./contracts";
import { BODY_NAMES, degree, signAt } from "./contracts";
import { planetComponent, signComponent } from "./source";
import { ASPECT_NAMES } from "./BirthChart";
import reference from "./reference-v1.json";
export function SourceDepth({ parts }: { parts: Component[] }) {
  return (
    <details className="chart-source-depth">
      <summary>
        Source language & scope <span aria-hidden="true">＋</span>
      </summary>
      {parts.map((r) => (
        <blockquote key={r.id}>
          <p>{r.text}</p>
          <cite>
            <a href={r.url} target="_blank" rel="noreferrer">
              {r.author} · {r.locator}
            </a>
          </cite>
          <small>
            {r.id} · v{r.version}
          </small>
          {r.exceptions?.length > 0 && <p>{r.exceptions.join(" ")}</p>}
        </blockquote>
      ))}
      <p>
        Separate symbolic components, not a documented combined placement
        reading or an established fact about you.
      </p>
    </details>
  );
}
export function CoreLights({ result }: { result: WesternResult }) {
  return (
    <div className="chart-core-lights">
      {["Sun", "Moon", "Ascendant"].map((n, i) => {
        const lon =
            i === 2 ? result.angles.ascendant : result.planets[n].longitude,
          row = result.reading.placements.find((r) => r.planet === n),
          body = row && planetComponent(row),
          sign = reference.records.find(
            (r) => r.kind === "sign" && r.key === signAt(lon),
          );
        return (
          <article key={n}>
            <span className="eyebrow">
              {
                [
                  "YOUR CENTRAL LIGHT",
                  "YOUR INNER RHYTHM",
                  "THE EASTERN HORIZON",
                ][i]
              }
            </span>
            <h3>
              {n} <em>in {signAt(lon)}</em>
            </h3>
            <p className="light-coordinate">
              {degree(lon)}
              {i < 2 ? ` · House ${result.planets[n].house}` : ""}
            </p>
            {body && <p>{body.text}.</p>}
            <p className="light-sign-theme">
              <span>{signAt(lon)}’s source theme</span>
              {sign?.text}.
            </p>
            {i === 2 && (
              <p className="scope-note">
                The calculated rising degree. The sign theme above is separate;
                no direct Ascendant-personality interpretation is supplied.
              </p>
            )}
            <SourceDepth
              parts={[
                ...(body ? [body] : []),
                ...(sign ? [sign as Component] : []),
              ]}
            />
          </article>
        );
      })}
    </div>
  );
}
export function PlacementFocus({
  result,
  selected,
}: {
  result: WesternResult;
  selected: string;
}) {
  const row = result.reading.placements.find((r) => r.planet === selected);
  if (!row)
    return (
      <section className="placement-focus">
        <span className="eyebrow">EASTERN HORIZON</span>
        <h2>
          Ascendant <em>in {signAt(result.angles.ascendant)}</em>
        </h2>
        <p>{degree(result.angles.ascendant)}</p>
        <p>
          The intersection of the eastern horizon and the ecliptic at the
          entered time and place. House 1 begins at the start of its sign in
          whole-sign charts, rather than at this exact degree.
        </p>
      </section>
    );
  const p = result.planets[selected],
    body = planetComponent(row),
    sign = signComponent(row);
  return (
    <section className="placement-focus" aria-live="polite">
      <p className="eyebrow">A CALCULATED PLACEMENT / TOUCH TO EXPLORE</p>
      <h2>
        {selected} <em>in {p.sign}</em>
      </h2>
      <p className="placement-coordinate">
        {degree(p.longitude)} <span>·</span> House {p.house}{" "}
        {p.retrograde ? "· Retrograde" : ""}
      </p>
      {body && <p className="placement-meaning">{body.text}.</p>}
      <p>{sign?.text}.</p>
      <p className="scope-note">
        {body
          ? "Planet and sign themes are separate source components."
          : "A sign theme is available; this edition supplies no planet-specific symbolic meaning for " +
            selected +
            "."}{" "}
        {p.retrograde
          ? "Retrograde is apparent astronomical motion, not an extra personality claim."
          : ""}
      </p>
      <SourceDepth parts={row.components} />
    </section>
  );
}
export function ChartReading({ result }: { result: WesternResult }) {
  const notable = [...result.aspects].sort((a, b) => a.orb - b.orb).slice(0, 3);
  return (
    <div className="chart-reading">
      <header className="chart-reading-heading">
        <p className="eyebrow">THREE LIGHTS / ONE SKY</p>
        <h2>
          The Sun, Moon and <em>Ascendant.</em>
        </h2>
        <p>
          Your three calculated placements, with their separate source themes
          where available.
        </p>
      </header>
      <CoreLights result={result} />
      <section className="notable-aspects">
        <p className="eyebrow">LINES ACROSS YOUR SKY</p>
        <h2>
          Closer to <em>an exact angle.</em>
        </h2>
        <p>
          These are the three major aspects nearest their exact angles, ordered
          by orb. This selects geometry, not personal importance.
        </p>
        {notable.length ? (
          notable.map((a, i) => {
            const r = result.reading.aspects.find(
              (r) => r.bodies.join() === a.bodies.join() && r.angle === a.angle,
            );
            return (
              <article key={i}>
                <span
                  className={`aspect-sigil aspect-${a.angle}`}
                  aria-hidden="true"
                >
                  {
                    (
                      {
                        0: "☌",
                        60: "⚹",
                        90: "□",
                        120: "△",
                        180: "☍",
                      } as Record<number, string>
                    )[a.angle]
                  }
                </span>
                <div>
                  <h3>{a.bodies.join(" & ")}</h3>
                  <p>
                    {ASPECT_NAMES[a.angle]} · {a.angle}° · orb{" "}
                    {a.orb.toFixed(2)}°
                  </p>
                  {r?.components.map((c) => (
                    <p key={c.id}>{c.text}.</p>
                  ))}
                  <p className="scope-note">
                    General aspect symbolism. Direct planet-pair interpretation
                    is unsupported.
                  </p>
                  {r && <SourceDepth parts={r.components} />}
                </div>
              </article>
            );
          })
        ) : (
          <p>No major aspects fall within this profile’s declared orbs.</p>
        )}
      </section>
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
      <div className="chart-takeaway">
        <span aria-hidden="true">✧</span>
        <h2>
          Hold a question,
          <br />
          <em>rather than a verdict.</em>
        </h2>
        <p>
          Which of these documented themes gives you a useful way to reflect?
          Keep what opens your thinking, while leaving room for your own
          experience.
        </p>
        <small>
          Symbolic tradition · no event predictions or established personality
          assessment.
        </small>
      </div>
    </div>
  );
}
