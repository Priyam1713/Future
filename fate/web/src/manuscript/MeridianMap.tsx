import { useMemo, useRef, useState, type PointerEvent } from "react";
import { ResultLeaf } from "../components/ResultLeaf";
import land from "./world-land.json";

type Axis = "MC" | "IC" | "ASC" | "DSC";
export type MapLine = {
  id: string;
  geometry: { coordinates: [number, number][][] };
  properties: {
    planet: string;
    angle: Axis;
    interpretation: {
      text: string;
      limitation: string;
      sources: { id: string; url: string; locator?: string; author?: string }[];
    };
  };
};
const axes: Axis[] = ["MC", "IC", "ASC", "DSC"];
const colors = { MC: "#f1b87e", IC: "#e8a5bd", ASC: "#b9e4b2", DSC: "#ace3ed" };
const meaning = {
  MC: "Upper meridian",
  IC: "Lower meridian",
  ASC: "Rising",
  DSC: "Setting",
};
const latitudes = [-60, -30, 0, 30, 60];
const longitudes = Array.from({ length: 11 }, (_, i) => (i - 5) * 30);

export function MeridianMap({ features = [] }: { features?: MapLine[] }) {
  const [planet, setPlanet] = useState("Sun");
  const [axis, setAxis] = useState<Axis>("MC");
  const [zoom, setZoom] = useState(1);
  const [center, setCenter] = useState([0, 0]);
  const start = useRef<{ x: number; y: number; origin: number[] } | null>(null);
  const planets = useMemo(
    () => [...new Set(features.map((f) => f.properties.planet))],
    [features],
  );
  const lines = useMemo(
    () =>
      features
        .filter((f) => f.properties.planet === planet)
        .map((line) => ({
          ...line,
          path: line.geometry.coordinates
            .map(
              (segment) =>
                "M" + segment.map(([lon, lat]) => `${lon},${-lat}`).join(" "),
            )
            .join(" "),
        })),
    [features, planet],
  );
  const selected = lines.find((line) => line.properties.angle === axis);
  const width = 360 / zoom,
    height = 180 / zoom;
  function move(e: PointerEvent<SVGSVGElement>) {
    if (!start.current) return;
    const bounds = e.currentTarget.getBoundingClientRect();
    const [x, y] = start.current.origin;
    setCenter([
      Math.max(
        -180 + width / 2,
        Math.min(
          180 - width / 2,
          x - ((e.clientX - start.current.x) * width) / bounds.width,
        ),
      ),
      Math.max(
        -90 + height / 2,
        Math.min(
          90 - height / 2,
          y - ((e.clientY - start.current.y) * height) / bounds.height,
        ),
      ),
    ]);
  }
  return (
    <section className="meridian-exhibit" aria-label="Astrocartography map">
      <div className="meridian-map">
        <svg
          viewBox={`${center[0] - width / 2} ${center[1] - height / 2} ${width} ${height}`}
          className={zoom > 1 ? "map-zoomed" : ""}
          role="img"
          aria-label="World coastlines with native planetary angular lines"
          onPointerDown={(e) => {
            if (zoom === 1) return;
            start.current = { x: e.clientX, y: e.clientY, origin: center };
            e.currentTarget.setPointerCapture(e.pointerId);
          }}
          onPointerMove={move}
          onLostPointerCapture={() => {
            start.current = null;
          }}
        >
          <g className="map-grid">
            {latitudes.map((y) => (
              <path key={y} d={`M-180 ${y}H180`} />
            ))}
            {longitudes.map((x) => (
              <path key={x} d={`M${x} -90V90`} />
            ))}
          </g>
          <g className="map-land">
            {land.paths.map((d, i) => (
              <path d={d} key={i} />
            ))}
          </g>
          {lines.map((line) => (
            <path
              key={line.id}
              d={line.path}
              data-line={line.id}
              className="map-line"
              data-selected={line.properties.angle === axis}
              stroke={colors[line.properties.angle]}
              onClick={() => setAxis(line.properties.angle)}
            />
          ))}
        </svg>
        {features.length > 0 && (
          <div className="map-tools">
            <button
              aria-label="Zoom map out"
              disabled={zoom === 1}
              onClick={() => {
                setZoom(zoom - 1);
                setCenter([0, 0]);
              }}
            >
              −
            </button>
            <button
              aria-label="Zoom map in"
              disabled={zoom === 3}
              onClick={() => setZoom(zoom + 1)}
            >
              +
            </button>
            <button
              aria-label="Reset map view"
              onClick={() => {
                setZoom(1);
                setCenter([0, 0]);
              }}
            >
              Reset
            </button>
          </div>
        )}
      </div>
      <p className="map-credit">
        Natural Earth coastlines · equirectangular projection
      </p>
      {selected && (
        <>
          <div className="map-selectors">
            <label>
              Planet
              <select
                value={planet}
                onChange={(e) => setPlanet(e.target.value)}
              >
                {planets.map((name) => (
                  <option key={name}>{name}</option>
                ))}
              </select>
            </label>
            <div className="folio-picks" role="group" aria-label="Angular line">
              {axes.map((key) => (
                <button
                  key={key}
                  aria-pressed={key === axis}
                  style={{ borderColor: colors[key] }}
                  onClick={() => setAxis(key)}
                >
                  {key} · {meaning[key]}
                </button>
              ))}
            </div>
          </div>
          <ResultLeaf
            status="Angular line"
            title={`${planet} · ${meaning[axis]}`}
            evidence={
              <details className="folio-depth">
                <summary>Sources and calculation</summary>
                <p>{selected.properties.interpretation.limitation}</p>
                <ul>
                  {selected.properties.interpretation.sources.map((source) => (
                    <li key={source.id}>
                      <a href={source.url} target="_blank" rel="noreferrer">
                        {source.locator || source.author || source.id}
                      </a>
                    </li>
                  ))}
                </ul>
              </details>
            }
          >
            <p className="folio-lead">
              {selected.properties.interpretation.text}
            </p>
          </ResultLeaf>
        </>
      )}
    </section>
  );
}
