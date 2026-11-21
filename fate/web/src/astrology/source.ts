import edition from "./reference-v1.json";
import {
  BODY_NAMES,
  signAt,
  type Component,
  type Geometry,
  type PlacementReading,
} from "./contracts";
const records = edition.records;
export function sourcePlacements(g: Geometry): PlacementReading[] {
  return BODY_NAMES.map((planet) => {
    const p = g.planets[planet];
    const parts = records.filter(
      (r) =>
        (["planet", "planet_symbol"].includes(r.kind) && r.key === planet) ||
        (r.kind === "sign" && r.key === signAt(p.longitude)) ||
        (r.kind === "house" && r.key === String(p.house)),
    );
    return {
      planet,
      sign: signAt(p.longitude),
      house: p.house,
      coverage: parts.length ? "compositional" : "unsupported",
      components: parts.map((r) => ({
        id: r.id,
        version: r.version,
        tradition: r.tradition,
        text: r.text,
        url: r.url,
        author: r.author,
        locator: r.locator,
        exceptions: r.exceptions,
      })) as Component[],
      missing_components: [
        ...(!parts.some(r=>['planet','planet_symbol'].includes(r.kind))?['planet meaning']:[]),
        ...(!parts.some(r=>r.kind==='sign')?['sign meaning']:[]),
        ...(!parts.some(r=>r.kind==='house')?['house meaning']:[]),
      ],
    };
  });
}
export function aspectSource(angle: number) {
  return records.filter((r) => r.kind === "aspect" && Number(r.key) === angle);
}
export function houseComponent(house: number): Component | undefined {
  return records.find((record) => record.kind === "house" && record.key === String(house));
}
export function planetComponent(row: PlacementReading) {
  return row.components.find((r) => r.id.includes(".symbol."));
}
export function signComponent(row: PlacementReading) {
  return row.components.find((r) => r.id.startsWith("houlding.sign."));
}
