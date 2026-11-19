import archive from "./reference-v1.json";
import { BODY_NAMES } from "../astrology/contracts";
import {
  TARGETS,
  PHASES,
  type TurningResult,
  type TransitSnapshot,
  type Interpretation,
  type TransitRule,
  type TransitConfig,
  type TransitEvent,
  type SkyFrame,
} from "./contracts";
const records = archive.records;
export function transitRule(index: number): TransitRule {
  const r = records[index];
  return {
    rule_id: r.id,
    version: r.version,
    text: r.text,
    source: r.url,
    author: r.author,
    locator: r.locator,
    exceptions: r.exceptions,
    ...(r.kind === "transit"
      ? {
          tradition: r.tradition,
          conditions: "conditions" in r ? r.conditions : {},
          documentation_scope:
            "documentation_scope" in r
              ? String(r.documentation_scope)
              : undefined,
        }
      : { scope: r.kind }),
  };
}
const sourceIndex = (r: TransitRule) => {
  const i = records.findIndex(
    (s) =>
      s.id === r.rule_id &&
      s.version === r.version &&
      s.text === r.text &&
      s.url === r.source &&
      s.locator === r.locator,
  );
  if (i < 0)
    throw new Error(
      "This transit source is not in the saved edition. Export the full native report instead.",
    );
  return i;
};
function indices(i: Interpretation) {
  return [i.direct.map(sourceIndex), i.components.map(sourceIndex)] as const;
}
export function transitSnapshot(result: TurningResult): TransitSnapshot {
  const r = result.report,
    configs = r.configurations;
  const target: Record<string, number> = {
    ...Object.fromEntries(
      Object.entries(r.natal_summary.planets).map(([n, p]) => [n, p.longitude]),
    ),
    ...r.natal_summary.angles,
  };
  return {
    oracle: 1,
    profile: "turning-sky-v1",
    window: [r.window.start_utc, r.window.end_utc],
    targets: TARGETS.map((n) => target[n]),
    configs: configs.map((c) => {
      const [direct, parts] = indices(c.interpretations);
      return [
        TARGETS.indexOf(c.transiting),
        TARGETS.indexOf(c.natal_target),
        c.aspect_degrees,
        c.branch_degrees,
        c.orb_limit,
        c.intervals.map((i) => [
          i.start_utc,
          i.end_utc,
          i.start_clipped,
          i.end_clipped,
          i.hours_in_window,
        ]),
        direct,
        parts,
        c.hours_in_window,
      ];
    }),
    events: r.exact_events.map((e) => {
      const [direct, parts] = indices(e.interpretations);
      return [
        configs.findIndex((c) => c.configuration_id === e.configuration_id),
        e.exact_utc,
        e.longitude,
        e.retrograde,
        e.near_station,
        e.transit_natal_house,
        e.pass_in_window,
        e.passes_in_window,
        e.angular_residual_degrees,
        direct,
        parts,
      ];
    }),
    frames: result.sky_samples.map((f) => [
      f.utc,
      BODY_NAMES.map((n) => f.planets[n].longitude),
      BODY_NAMES.map((n) => f.planets[n].retrograde),
      f.contacts.map((c) => [
        configs.findIndex((x) => x.configuration_id === c.configuration_id),
        PHASES.indexOf(c.phase as (typeof PHASES)[number]),
      ]),
    ]),
  };
}
export function restoreTransit(s: TransitSnapshot): TurningResult {
  const interp = (d: number[], c: number[]): Interpretation => ({
    coverage: d.length
      ? "documented"
      : c.length
        ? "compositional"
        : "unsupported",
    direct: d.map(transitRule),
    components: c.map(transitRule),
    missing_coverage: d.length
      ? []
      : ["No documented direct planet-pair reading for this contact."],
  });
  const configs: TransitConfig[] = s.configs.map((c, i) => ({
    configuration_id: `saved-config-${i}`,
    transiting: TARGETS[c[0]],
    natal_target: TARGETS[c[1]],
    aspect_degrees: c[2],
    branch_degrees: c[3],
    orb_limit: c[4],
    intervals: c[5].map((w) => ({
      start_utc: w[0],
      end_utc: w[1],
      start_clipped: w[2],
      end_clipped: w[3],
      hours_in_window: w[4],
    })),
    hours_in_window: c[8],
    interpretations: interp(c[6], c[7]),
  }));
  const events: TransitEvent[] = s.events.map((e, i) => ({
    ...configs[e[0]],
    id: `event-${String(i + 1).padStart(4, "0")}`,
    exact_utc: e[1],
    longitude: e[2],
    phase: "exact",
    retrograde: e[3],
    near_station: e[4],
    transit_natal_house: e[5],
    pass_in_window: e[6],
    passes_in_window: e[7],
    angular_residual_degrees: e[8],
    interpretations: interp(e[9], e[10]),
  }));
  const frames: SkyFrame[] = s.frames.map((f) => ({
    utc: f[0],
    planets: Object.fromEntries(
      BODY_NAMES.map((n, i) => [
        n,
        { longitude: f[1][i], retrograde: f[2][i] },
      ]),
    ),
    contacts: f[3].map((c) => ({
      configuration_id: configs[c[0]].configuration_id,
      phase: PHASES[c[1]],
    })),
  }));
  const repeats = configs.flatMap((c) => {
    const es = events.filter((e) => e.configuration_id === c.configuration_id);
    return es.length > 1
      ? [
          {
            configuration_id: c.configuration_id,
            event_ids: es.map((e) => e.id),
            kind: es.some((e) => e.retrograde)
              ? "retrograde repetition"
              : "recurring contact",
            explanation:
              "The same directed contact repeats inside this saved window; contacts outside it are not counted.",
            source:
              "https://theastrologypodcast.com/transcripts/tap-ep-365-transcript-transits-in-astrology-an-introduction-to-timing/",
            locator: "Retrogrades, stations and extended transit sequences",
          },
        ]
      : [];
  });
  return {
    report: {
      technique_id: 1,
      application: "transits",
      window: {
        start_utc: s.window[0],
        end_utc: s.window[1],
        end_exclusive: true,
      },
      natal_summary: {
        planets: Object.fromEntries(
          BODY_NAMES.map((n, i) => [n, { longitude: s.targets[i] }]),
        ),
        angles: { ascendant: s.targets[10], midheaven: s.targets[11] },
      },
      exact_events: events,
      configurations: configs,
      active_at_start: frames[0]?.contacts ?? [],
      precision: { root_bracket_seconds: 0.25, scan_hours: 3 },
      orbs: { 0: 8, 60: 4, 90: 6, 120: 6, 180: 8 },
      reproducibility: { source_edition: "fate-transit-reference-v1" },
      limitations: [
        "Minimal saved contact edition. Original birth details, session proof and native speed traces are excluded.",
        "Timing brackets are numerical convergence, not personal-event accuracy.",
      ],
      presentation: {
        overview: {
          exact_contacts: events.length,
          active_at_start: frames[0]?.contacts.length ?? 0,
          configurations: configs.length,
          repeated_patterns: repeats.length,
        },
        repeated_patterns: repeats,
        phase_context: {
          meaning:
            "Applying approaches exactness; separating recedes. A station can interrupt application.",
          source: "https://www.skyscript.co.uk/aspects2.html",
          locator: "Applying & Separating Aspects",
        },
        grouping_source: {
          url: "https://theastrologypodcast.com/transcripts/tap-ep-365-transcript-transits-in-astrology-an-introduction-to-timing/",
          locator: "Duration and repeated contacts",
          principle: "Durations are measured only inside this saved window.",
        },
      },
    },
    sky_samples: frames,
    sampling:
      "Saved native daily sky samples; no interpolation or new calculation.",
    computation: {
      seconds: null,
      deadline_seconds: 60,
      native_days: frames.length,
    },
  };
}
