import { ASPECT_NAMES } from "../astrology/BirthChart";
import { degree } from "../astrology/contracts";
import {
  fullTime,
  exactTime,
  type TransitEvent,
  type TransitConfig,
  type Interpretation,
} from "./contracts";
export function TransitSources({
  interpretation,
}: {
  interpretation: Interpretation;
}) {
  return (
    <details className="transit-sources">
      <summary>
        Source interpretations & limits <span aria-hidden="true">＋</span>
      </summary>
      {interpretation.direct.length > 0 && (
        <>
          <p className="eyebrow">
            DOCUMENTED SYMBOLIC PAIR / SELECTED CONDITIONS
          </p>
          {interpretation.direct.map((r) => (
            <blockquote key={r.rule_id}>
              <p>{r.text}</p>
              <cite>
                <a href={r.source} target="_blank" rel="noreferrer">
                  {r.author} · {r.locator}
                </a>
              </cite>
              {r.documentation_scope && (
                <p className="scope-note">{r.documentation_scope}</p>
              )}
              {!!r.conditions &&
                Object.keys(r.conditions as object).length > 0 && (
                  <p className="scope-note">
                    Matched source conditions: {JSON.stringify(r.conditions)}
                  </p>
                )}
              {r.exceptions.map((e, i) => (
                <p key={i} className="scope-note">
                  {e}
                </p>
              ))}
              <small>
                {r.rule_id} · v{r.version}
              </small>
            </blockquote>
          ))}
        </>
      )}
      {interpretation.components.length > 0 && (
        <>
          <p className="eyebrow">SEPARATE SOURCE COMPONENTS</p>
          <p>These themes are not a documented combined planet-pair reading.</p>
          {interpretation.components.map((r) => (
            <blockquote key={r.rule_id}>
              <p>{r.text}</p>
              <cite>
                <a href={r.source} target="_blank" rel="noreferrer">
                  {r.author} · {r.locator}
                </a>
              </cite>
              <small>
                {r.rule_id} · v{r.version}
              </small>
            </blockquote>
          ))}
        </>
      )}
      {!interpretation.direct.length && (
        <p>
          No direct symbolic pair interpretation is supplied for these
          conditions. The astronomical contact remains calculated.
        </p>
      )}
      <p>
        Symbolic tradition, not a life-event prediction or demonstrated personal
        accuracy.
      </p>
    </details>
  );
}
export function ContactReading({
  event,
  config,
}: {
  event: TransitEvent;
  config: TransitConfig;
}) {
  const direct = event.interpretations.direct[0],
    parts = event.interpretations.components;
  return (
    <article className="contact-reading" aria-live="polite">
      <p className="eyebrow">A MOMENT OF ALIGNMENT / CALCULATED CONTACT</p>
      <h2>
        {event.transiting}
        <br />
        <em>
          {ASPECT_NAMES[event.aspect_degrees].toLowerCase()} natal{" "}
          {event.natal_target}.
        </em>
      </h2>
      <p className="contact-time">{exactTime(event.exact_utc)}</p>
      <div className="contact-facts">
        <span>{event.aspect_degrees}° aspect</span>
        <span>{event.retrograde ? "Retrograde" : "Direct motion"}</span>
        <span>
          Pass {event.pass_in_window} of {event.passes_in_window} in this window
        </span>
      </div>
      <p className="contact-theme">
        {direct
          ? direct.text
          : (parts.find((r) => r.scope === "aspect")?.text ??
            "A calculated angular contact; no supported symbolic interpretation is supplied.")}
      </p>
      <p className="scope-note">
        {direct
          ? "A documented symbolic account under the matched conditions."
          : "General aspect symbolism, without a direct pair interpretation."}{" "}
        An exact astronomical time does not promise a life event.
      </p>
      <TransitSources interpretation={event.interpretations} />
      <details className="contact-duration">
        <summary>Duration, geometry & timing precision</summary>
        <p>
          Exact native timestamp {event.exact_utc}. Transiting longitude{" "}
          {degree(event.longitude)} · natal-house sector{" "}
          {event.transit_natal_house}. Residual{" "}
          {event.angular_residual_degrees.toExponential(2)}°.
        </p>
        <p>
          Native root brackets converge to 0.25 seconds. That is numerical
          precision, not certainty about personal timing; near stations timing
          is less certain.
        </p>
        {event.near_station && (
          <p>Native near-station flag: apparent motion is slow.</p>
        )}
        <p>
          Within {config.orb_limit}° orb for {config.hours_in_window.toFixed(1)}{" "}
          calculated hours in this window. Orb limits are conventions, not a
          strength or importance score.
        </p>
        {config.intervals.map((w, i) => (
          <p key={i}>
            {fullTime(w.start_utc)} → {fullTime(w.end_utc)}
            {w.start_clipped || w.end_clipped
              ? " · clipped to this window; full duration unknown"
              : ""}
          </p>
        ))}
        <p>
          Repeated pass counts refer only to this selected window. Extra passes
          outside it are not inferred.
        </p>
      </details>
    </article>
  );
}
