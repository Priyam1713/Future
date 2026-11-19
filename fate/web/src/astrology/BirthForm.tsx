import { useEffect, useRef, useState } from "react";
import { api } from "../types";
import type { Houses, WesternInput } from "./contracts";
interface Place {
  id: number;
  name: string;
  country: string;
  region: string;
  latitude: number;
  longitude: number;
  zone: string;
}
export function BirthForm({
  onSubmit,
  busy,
  error,
  chamber,
  children,
}: {
  onSubmit: (q: WesternInput) => void;
  busy: boolean;
  error: string;
  chamber?: "vedic" | "bazi";
  children?: React.ReactNode;
}) {
  const [date, setDate] = useState(""),
    [time, setTime] = useState(""),
    [known, setKnown] = useState(true),
    [query, setQuery] = useState(""),
    [places, setPlaces] = useState<Place[]>([]),
    [searchError, setSearchError] = useState(""),
    [searching, setSearching] = useState(false),
    [place, setPlace] = useState<Place | null>(null),
    [lat, setLat] = useState(""),
    [lon, setLon] = useState(""),
    [zone, setZone] = useState(""),
    [houses, setHouses] = useState<Houses>("whole-sign"),
    [fold, setFold] = useState(""),
    [confirmed, setConfirmed] = useState(false),
    [manual, setManual] = useState(false);
  const abort = useRef<AbortController | null>(null);
  useEffect(() => () => abort.current?.abort(), []);
  const search = async () => {
    abort.current?.abort();
    const c = new AbortController();
    abort.current = c;
    setSearching(true);
    setSearchError("");
    setPlaces([]);
    try {
      const r = await api<{ places: Place[] }>(
        "/api/western/places",
        { query },
        c.signal,
      );
      if (!c.signal.aborted) {
        setPlaces(r.places);
        if (!r.places.length)
          setSearchError(
            "No matching city in this catalog. Try another spelling or enter exact coordinates.",
          );
      }
    } catch (e) {
      if (!c.signal.aborted)
        setSearchError(
          e instanceof Error
            ? e.message
            : "Search unavailable. You can enter coordinates instead.",
        );
    } finally {
      if (!c.signal.aborted) setSearching(false);
    }
  };
  function pick(p: Place) {
    setPlace(p);
    setLat(String(p.latitude));
    setLon(String(p.longitude));
    setZone(p.zone);
    setPlaces([]);
    setConfirmed(false);
  }
  return (
    <form
      className="birth-form"
      onSubmit={(e) => {
        e.preventDefault();
        if (known && confirmed)
          onSubmit({
            local: `${date}T${time}`,
            latitude: Number(lat),
            longitude: Number(lon),
            zone: zone.trim(),
            houses,
            fold: fold === "" ? null : (Number(fold) as 0 | 1),
          });
      }}
    >
      <div className="birth-form-heading">
        <span className="eyebrow">THE MOMENT / THE PLACE</span>
        <h2>Set your coordinates.</h2>
        <p>
          Begin with the time recorded for your birth. Your details stay in this
          visit unless you explicitly export them.
        </p>
      </div>
      <div className="birth-date-time">
        <label>
          Date of birth
          <input
            type="date"
            min="1850-01-01"
            max="2149-12-31"
            required
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
        <label>
          Recorded birth time
          <input
            type="time"
            step="1"
            required={known}
            disabled={!known}
            value={time}
            onChange={(e) => setTime(e.target.value)}
          />
        </label>
      </div>
      <label className="birth-check">
        <input
          type="checkbox"
          checked={!known}
          onChange={(e) => {
            setKnown(!e.target.checked);
            if (e.target.checked) setTime("");
          }}
        />
        I don’t know my birth time
      </label>
      {!known && (
        <p className="birth-warning" role="status">
          {chamber
            ? "A recorded birth time is required for this calculation."
            : "This complete chart needs a known birth time. We won’t substitute noon or invent an Ascendant or houses. You can return when you have a recorded time."}
        </p>
      )}
      <div className="place-search">
        <label>
          Birth city
          <input
            type="search"
            autoComplete="off"
            value={query}
            maxLength={80}
            placeholder="City and country code, e.g. London GB"
            onChange={(e) => {
              setQuery(e.target.value);
              setConfirmed(false);
              abort.current?.abort();
              setSearching(false);
              setPlaces([]);
              setSearchError("");
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                if (query.trim().length >= 2) void search();
              }
            }}
          />
        </label>
        <button
          className="secondary"
          type="button"
          disabled={searching || query.trim().length < 2}
          onClick={() => void search()}
        >
          {searching ? "Searching…" : "Find city"}
        </button>
      </div>
      {searchError && (
        <p role="status" className="scope-note">
          {searchError}
        </p>
      )}
      {!!places.length && (
        <ul className="place-results" aria-label="Matching birth cities">
          {places.map((p) => (
            <li key={p.id}>
              <button type="button" onClick={() => pick(p)}>
                <strong>
                  {p.name} · {p.country}
                </strong>
                <span>
                  Region {p.region} · {p.latitude.toFixed(4)},{" "}
                  {p.longitude.toFixed(4)} · {p.zone}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
      {place && (
        <div className="selected-place">
          <span aria-hidden="true">⌖</span>
          <div>
            <strong>
              {place.name}, {place.country}
            </strong>
            <small>GeoNames city reference point · {place.id}</small>
          </div>
        </div>
      )}
      <button
        type="button"
        className="text-button coordinate-toggle"
        aria-expanded={manual}
        onClick={() => setManual(!manual)}
      >
        {manual
          ? "Hide coordinate editor"
          : "Enter or refine exact coordinates / timezone"}{" "}
        <span aria-hidden="true">＋</span>
      </button>
      {(manual || place) && (
        <div className="coordinate-editor">
          <p>
            A city point is approximate. For a precise birthplace, edit
            latitude/longitude. The timezone must match the actual birthplace;
            historical records can be uncertain.
          </p>
          <div className="birth-date-time">
            <label>
              Latitude · north positive
              <input
                type="number"
                step="any"
                min="-89.999999"
                max="89.999999"
                required
                value={lat}
                onChange={(e) => {
                  setLat(e.target.value);
                  setConfirmed(false);
                }}
              />
            </label>
            <label>
              Longitude · east positive
              <input
                type="number"
                step="any"
                min="-180"
                max="180"
                required
                value={lon}
                onChange={(e) => {
                  setLon(e.target.value);
                  setConfirmed(false);
                }}
              />
            </label>
          </div>
          <label>
            IANA timezone
            <input
              required
              placeholder="Europe/London"
              autoComplete="off"
              maxLength={80}
              value={zone}
              onChange={(e) => {
                setZone(e.target.value);
                setConfirmed(false);
              }}
            />
          </label>
        </div>
      )}
      {children}
      <details className="birth-conventions">
        <summary>Chart conventions & repeated clock times</summary>
        {chamber ? (
          <p>
            {chamber === "vedic"
              ? "Lahiri 1956 sidereal convention, mean nodes and whole-sign houses. Latitude must be strictly within 66° north or south."
              : "Li Chun sets the year, and solar terms set the months. Supported local years are 1901–2100."}
          </p>
        ) : (
          <>
            <p>
              Tropical zodiac · modern psychological source components ·
              traditional rulership · ten apparent geocentric bodies. No direct
              placement or aspect-pair predictions.
            </p>
            <label>
              House system
              <select
                value={houses}
                onChange={(e) => setHouses(e.target.value as Houses)}
              >
                {[
                  "whole-sign",
                  "equal",
                  "porphyry",
                  "placidus",
                  "regiomontanus",
                  "campanus",
                ].map((h) => (
                  <option key={h}>{h}</option>
                ))}
              </select>
            </label>
            <p>
              Whole-sign is the default. Quadrant systems reject the polar
              domain without silently switching systems.
            </p>
          </>
        )}
        <label>
          Repeated local time at a clock change
          <select value={fold} onChange={(e) => setFold(e.target.value)}>
            <option value="">Ask if this time repeats</option>
            <option value="0">
              First occurrence · before the clock goes back
            </option>
            <option value="1">
              Second occurrence · after the clock goes back
            </option>
          </select>
        </label>
        <p>
          Nonexistent times are rejected.{" "}
          {chamber !== "bazi" && "Supported ephemeris epochs: 1850–2149."}
          Pinned IANA tzdata 2025.2.
        </p>
      </details>
      <label className="birth-check coordinate-confirm">
        <input
          type="checkbox"
          checked={confirmed}
          required
          onChange={(e) => setConfirmed(e.target.checked)}
          disabled={!lat || !lon || !zone}
        />
        I’ve checked the coordinates and timezone for my birthplace.
      </label>
      <p className="birth-error" role="alert">
        {error}
      </p>
      <button
        className="primary"
        type="submit"
        disabled={busy || !known || !confirmed}
      >
        {busy
          ? "Calculating…"
          : chamber === "vedic"
            ? "Open my sidereal charts"
            : chamber === "bazi"
              ? "Open my Four Pillars"
              : "Open my celestial chart"}{" "}
        <span aria-hidden="true">✧</span>
      </button>
      <p className="birth-attribution">
        City search:{" "}
        <a href="https://www.geonames.org/" target="_blank" rel="noreferrer">
          GeoNames · CC BY 4.0
        </a>
        . Bundled city catalog; your search reaches this server, not a
        third-party geocoder. No browser geolocation.
      </p>
    </form>
  );
}
