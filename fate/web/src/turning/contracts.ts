export const TRANSIT_REFERENCE = "fate-transit-reference-v1";
export const TARGETS = [
  "Sun",
  "Moon",
  "Mercury",
  "Venus",
  "Mars",
  "Jupiter",
  "Saturn",
  "Uranus",
  "Neptune",
  "Pluto",
  "ascendant",
  "midheaven",
];
export const PHASES = [
  "applying",
  "exact",
  "separating",
  "stationary",
] as const;
export interface TransitRule {
  rule_id: string;
  version: number;
  text: string;
  source: string;
  author: string;
  locator: string;
  exceptions: string[];
  scope?: string;
  documentation_scope?: string;
  conditions?: unknown;
  tradition?: string;
}
export interface Interpretation {
  coverage: string;
  direct: TransitRule[];
  components: TransitRule[];
  missing_coverage: string[];
}
export interface TransitConfig {
  configuration_id: string;
  transiting: string;
  natal_target: string;
  aspect_degrees: number;
  branch_degrees: number;
  orb_limit: number;
  intervals: {
    start_utc: string;
    end_utc: string;
    hours_in_window: number;
    start_clipped: boolean;
    end_clipped: boolean;
  }[];
  hours_in_window: number;
  interpretations: Interpretation;
}
export interface TransitEvent {
  id: string;
  configuration_id: string;
  transiting: string;
  natal_target: string;
  aspect_degrees: number;
  branch_degrees: number;
  exact_utc: string;
  longitude: number;
  phase: "exact";
  retrograde: boolean;
  near_station: boolean;
  speed_degrees_per_day?: number;
  transit_natal_house: number;
  angular_residual_degrees: number;
  pass_in_window: number;
  passes_in_window: number;
  interpretations: Interpretation;
}
export interface SkyFrame {
  utc: string;
  planets: Record<string, { longitude: number; retrograde: boolean }>;
  contacts: {
    configuration_id: string;
    phase: string;
    orb?: number;
    retrograde?: boolean;
  }[];
}
export interface TransitOrigin {
  natal: Record<string, unknown>;
  proof: string;
}
export interface TurningResult {
  report: {
    technique_id: 1;
    application: "transits";
    window: { start_utc: string; end_utc: string; end_exclusive: boolean };
    natal_summary: {
      planets: Record<string, { longitude: number }>;
      angles: { ascendant: number; midheaven: number };
    };
    exact_events: TransitEvent[];
    configurations: TransitConfig[];
    active_at_start: unknown[];
    precision: unknown;
    orbs: unknown;
    reproducibility: unknown;
    limitations: string[];
    presentation: {
      overview: {
        exact_contacts: number;
        active_at_start: number;
        configurations: number;
        repeated_patterns: number;
      };
      repeated_patterns: {
        configuration_id: string;
        event_ids: string[];
        kind: string;
        explanation: string;
        source: string;
        locator: string;
      }[];
      phase_context: { meaning: string; source: string; locator: string };
      grouping_source: { url: string; locator: string; principle: string };
    };
  };
  sky_samples: SkyFrame[];
  sampling: string;
  computation: {
    seconds: number | null;
    deadline_seconds: number;
    native_days: number;
  };
}
// Indexed source identities remove repeated prose, not native result content.
export type SavedConfig = [
  number,
  number,
  number,
  number,
  number,
  [string, string, boolean, boolean, number][],
  number[],
  number[],
  number,
];
export type SavedEvent = [
  number,
  string,
  number,
  boolean,
  boolean,
  number,
  number,
  number,
  number,
  number[],
  number[],
];
export interface TransitSnapshot {
  oracle: 1;
  profile: "turning-sky-v1";
  window: [string, string];
  targets: number[];
  configs: SavedConfig[];
  events: SavedEvent[];
  frames: [string, number[], boolean[], [number, number][]][];
}
export const dateLabel = (utc: string) =>
  new Intl.DateTimeFormat("en", {
    timeZone: "UTC",
    month: "short",
    day: "numeric",
  }).format(new Date(utc));
export const timeLabel = (utc: string) =>
  new Intl.DateTimeFormat("en", {
    timeZone: "UTC",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).format(new Date(utc));
export const fullTime = (utc: string) =>
  `${dateLabel(utc)}, ${new Date(utc).getUTCFullYear()} · ${timeLabel(utc)} UTC`;

export const exactTime = (utc: string) =>
  `${dateLabel(utc)}, ${new Date(utc).getUTCFullYear()} · ${new Intl.DateTimeFormat("en", { timeZone: "UTC", hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" }).format(new Date(utc))} UTC`;
