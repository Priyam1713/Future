import { useEffect, useRef, useState } from "react";
import { api } from "../types";

export type Site = { latitude: number; longitude: number; zone: string };
type Place = Site & {
  id: number;
  name: string;
  country: string;
  region: string;
};
export type Moment = Site & { local: string; fold: null | 0 | 1 };

export function SkySite({
  value,
  onSite,
  disabled,
}: {
  value?: Site;
  onSite: (site?: Site) => void;
  disabled: boolean;
}) {
  const [query, setQuery] = useState("");
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [zone, setZone] = useState("");
  const [places, setPlaces] = useState<Place[]>([]);
  const [label, setLabel] = useState("");
  const [hint, setHint] = useState("");
  const [manual, setManual] = useState(false);
  const pending = useRef<AbortController | null>(null);
  useEffect(() => () => pending.current?.abort(), []);
  async function search() {
    pending.current?.abort();
    const c = new AbortController();
    pending.current = c;
    setPlaces([]);
    setHint("Searching the city catalogue…");
    try {
      const { places: items } = await api<{ places: Place[] }>(
        "/api/western/places",
        { query },
        c.signal,
      );
      if (!c.signal.aborted) {
        setPlaces(items);
        setHint(
          items.length ? "" : "Try another spelling or enter coordinates.",
        );
      }
    } catch (e) {
      if (!c.signal.aborted) setHint((e as Error).message);
    }
  }
  return (
    <div className="sky-site">
      {value ? (
        <div className="sky-confirmed">
          <span>
            {label || `${value.latitude}°, ${value.longitude}°`} · {value.zone}
          </span>
          <button
            type="button"
            className="text-button"
            disabled={disabled}
            onClick={() => onSite(undefined)}
          >
            Change place
          </button>
        </div>
      ) : (
        <>
          {!manual ? (
            <>
              <div className="sky-site-search">
                <label>
                  City or place
                  <input
                    type="search"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={disabled}
                  />
                </label>
                <button
                  type="button"
                  disabled={query.trim().length < 2 || disabled}
                  onClick={() => void search()}
                >
                  Find place
                </button>
              </div>
              <div className="folio-picks">
                {places.map(
                  ({
                    id,
                    name,
                    country,
                    region,
                    latitude,
                    longitude,
                    zone: tz,
                  }) => (
                    <button
                      key={id}
                      type="button"
                      disabled={disabled}
                      onClick={() => {
                        setLabel(`${name}, ${country}`);
                        onSite({ latitude, longitude, zone: tz });
                        setPlaces([]);
                      }}
                    >
                      {[name, region, country].filter(Boolean).join(", ")}
                    </button>
                  ),
                )}
              </div>
              {hint && <p role="status">{hint}</p>}
            </>
          ) : (
            <>
              <div className="folio-pair">
                <label>
                  Latitude
                  <input
                    inputMode="decimal"
                    value={lat}
                    onChange={(e) => setLat(e.target.value)}
                    disabled={disabled}
                  />
                </label>
                <label>
                  Longitude
                  <input
                    inputMode="decimal"
                    value={lon}
                    onChange={(e) => setLon(e.target.value)}
                    disabled={disabled}
                  />
                </label>
              </div>
              <label>
                IANA timezone
                <input
                  placeholder="Europe/London"
                  value={zone}
                  onChange={(e) => setZone(e.target.value)}
                  disabled={disabled}
                />
              </label>
              <button
                type="button"
                className="secondary"
                disabled={
                  disabled ||
                  !lat.trim() ||
                  !lon.trim() ||
                  !zone.trim() ||
                  !(Math.abs(Number(lat)) < 90) ||
                  !(Math.abs(Number(lon)) <= 180)
                }
                onClick={() => {
                  setLabel("");
                  onSite({
                    latitude: Number(lat),
                    longitude: Number(lon),
                    zone: zone.trim(),
                  });
                }}
              >
                Confirm coordinates
              </button>
            </>
          )}
          <button
            type="button"
            className="text-button"
            disabled={disabled}
            onClick={() => setManual(!manual)}
          >
            {manual ? "Search the city catalogue" : "Enter exact coordinates"}
          </button>
        </>
      )}
    </div>
  );
}
