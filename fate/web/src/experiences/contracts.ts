/** Consumer availability is independent of Workbench/core engine status. */
export type OracleId = 4 | 16;
export interface ExperienceContract {
  id: OracleId;
  title: string;
  room: string;
  invitation: string;
  endpoint: string;
  privacy: string;
}
export const EXPERIENCES: Record<OracleId, ExperienceContract> = {
  16: {
    id: 16,
    title: "Tarot",
    room: "The chamber of symbols",
    invitation: "A different lens for the question you carry.",
    endpoint: "/api/readings",
    privacy: "Only a question, if you choose to share one.",
  },
  4: {
    id: 4,
    title: "Numerology",
    room: "The observatory of numbers",
    invitation: "Find the quiet patterns in your name and date.",
    endpoint: "/api/numerology",
    privacy:
      "Your name and dates are processed by this server for this visit only.",
  },
};
export interface NumberInput {
  name: string;
  birth: string;
  target: string;
  basis: "birth" | "current";
  y_roles: string;
}
export interface NumberTrace {
  result: number | null;
  steps?: number[];
  input?: number;
  components?: NumberTrace[];
}
export interface NumberTheme {
  scope: string;
  number?: number;
  coverage: "direct" | "compositional";
  text: string;
  source_id: string;
  url: string;
  locator: string;
}
export interface NumberResult {
  technique_id: 4;
  profile: string;
  birth: string;
  target: string;
  name: { original: string; basis: string; y_roles: string };
  life_path: NumberTrace;
  expression: NumberTrace;
  soul_urge: NumberTrace;
  personality: NumberTrace;
  birthday: { original_day: number; companion: NumberTrace };
  cycles: {
    year: NumberTrace;
    month: NumberTrace;
    day: NumberTrace;
    sun: NumberTrace;
    year_interval: string[];
  };
  readings: NumberTheme[];
  sources: { id: string; url: string; locator: string }[];
  conventions: unknown;
  limitations: string[];
  interpretation_limits: string;
}
export interface NumberEnvelope {
  oracle_id: 4;
  result: NumberResult;
  receipt: string;
}
export interface NumberCommentary {
  themes: { scope: string; source_id: string; reflection: string }[];
  provenance: { provider: string; model: string };
  coverage: string;
}
