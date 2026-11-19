import type { TransitSnapshot } from "./contracts";
export function validTransit(v: unknown): v is TransitSnapshot {
  if (!v || typeof v !== "object" || Array.isArray(v)) return false;
  const s = v as TransitSnapshot;
  const keys = (o: object, n: string[]) =>
    Object.keys(o).length === n.length && n.every((k) => Object.hasOwn(o, k));
  const lon = (n: unknown) =>
    typeof n === "number" && Number.isFinite(n) && n >= 0 && n < 360;
  const integer = (n: unknown, max: number) =>
    typeof n === "number" && Number.isInteger(n) && n >= 0 && n < max;
  const stamp = (t: unknown) =>
    typeof t === "string" &&
    /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:\+00:00|Z)$/.test(t) &&
    Number.isFinite(Date.parse(t)) &&
    new Date(t).getUTCFullYear() >= 1850 &&
    new Date(t).getUTCFullYear() <= 2149;
  const refs = (r: unknown) =>
    Array.isArray(r) &&
    r.length <= 32 &&
    new Set(r).size === r.length &&
    r.every((i) => integer(i, 62));
  if (
    !keys(s, [
      "oracle",
      "profile",
      "window",
      "targets",
      "configs",
      "events",
      "frames",
    ]) ||
    s.oracle !== 1 ||
    s.profile !== "turning-sky-v1" ||
    !Array.isArray(s.window) ||
    s.window.length !== 2 ||
    !s.window.every(stamp)
  )
    return false;
  const span = Date.parse(s.window[1]) - Date.parse(s.window[0]);
  if (span < 86400000 || span > 30 * 86400000 || span % 86400000) return false;
  const inside = (t: string, end = false) =>
    stamp(t) &&
    Date.parse(t) >= Date.parse(s.window[0]) &&
    Date.parse(t) <= Date.parse(s.window[1]) - (end ? 0 : 1);
  if (
    !Array.isArray(s.targets) ||
    s.targets.length !== 12 ||
    !s.targets.every(lon) ||
    !Array.isArray(s.configs) ||
    s.configs.length > 1080 ||
    !Array.isArray(s.events) ||
    s.events.length > 1000 ||
    !Array.isArray(s.frames) ||
    s.frames.length !== span / 86400000
  )
    return false;
  if (
    !s.configs.every(
      (c) =>
        Array.isArray(c) &&
        c.length === 9 &&
        integer(c[0], 10) &&
        integer(c[1], 12) &&
        [0, 60, 90, 120, 180].includes(c[2]) &&
        [c[2], -c[2]].includes(c[3]) &&
        typeof c[4] === "number" &&
        Number.isFinite(c[4]) &&
        c[4] >= 0 &&
        c[4] <= 8 &&
        Array.isArray(c[5]) &&
        c[5].length <= 20 &&
        c[5].every(
          (w) =>
            Array.isArray(w) &&
            w.length === 5 &&
            inside(w[0], true) &&
            inside(w[1], true) &&
            Date.parse(w[0]) < Date.parse(w[1]) &&
            typeof w[2] === "boolean" &&
            typeof w[3] === "boolean" &&
            typeof w[4] === "number" &&
            Number.isFinite(w[4]) &&
            w[4] > 0 &&
            w[4] <= 720,
        ) &&
        refs(c[6]) &&
        refs(c[7]) &&
        typeof c[8] === "number" &&
        Number.isFinite(c[8]) &&
        c[8] >= 0 &&
        c[8] <= 720,
    )
  )
    return false;
  if (
    !s.events.every(
      (e, i) =>
        Array.isArray(e) &&
        e.length === 11 &&
        integer(e[0], s.configs.length) &&
        inside(e[1]) &&
        (!i || Date.parse(s.events[i - 1][1]) <= Date.parse(e[1])) &&
        lon(e[2]) &&
        typeof e[3] === "boolean" &&
        typeof e[4] === "boolean" &&
        typeof e[5] === "number" &&
        typeof e[6] === "number" &&
        typeof e[7] === "number" &&
        integer(e[5] - 1, 12) &&
        integer(e[6] - 1, 1000) &&
        integer(e[7] - 1, 1000) &&
        e[6] <= e[7] &&
        typeof e[8] === "number" &&
        Number.isFinite(e[8]) &&
        e[8] >= 0 &&
        e[8] <= 0.01 &&
        refs(e[9]) &&
        refs(e[10]),
    )
  )
    return false;
  return s.frames.every(
    (f, i) =>
      Array.isArray(f) &&
      f.length === 4 &&
      inside(f[0]) &&
      Date.parse(f[0]) === Date.parse(s.window[0]) + i * 86400000 &&
      Array.isArray(f[1]) &&
      f[1].length === 10 &&
      f[1].every(lon) &&
      Array.isArray(f[2]) &&
      f[2].length === 10 &&
      f[2].every((x) => typeof x === "boolean") &&
      Array.isArray(f[3]) &&
      f[3].length <= 1080 &&
      f[3].every(
        (c) =>
          Array.isArray(c) &&
          c.length === 2 &&
          integer(c[0], s.configs.length) &&
          integer(c[1], 4),
      ),
  );
}
