import type { StudyId } from "./contracts";
export type Control = {
  label: string;
  choices?: string[];
  max?: number;
  map?: (n: number) => string;
  commit?: string;
};
export const CONTROLS: Partial<Record<StudyId, Control>> = {
  26: {
    label: "Open a leaf",
    choices: [
      "Records",
      "Pathway",
      "Describe",
      "Question framing",
      "Scope limits",
    ],
  },
  45: {
    label: "Set the final cue",
    choices: ["A differs", "B differs", "Both the same"],
  },
  49: {
    label: "Forecast method",
    choices: [
      "Last value",
      "Trend drift",
      "Mean",
      "Smoothing",
      "NOAA benchmark",
    ],
  },
  50: {
    label: "Route the gates",
    choices: [
      "Bell pair",
      "Independent H",
      "Flip second wire",
      "Quarter turn Ry",
    ],
  },
  51: {
    label: "Synthetic evidence ratio",
    choices: ["3 : 1", "1 : 1", "0 : 1", "1 : 2", "5 : 1"],
  },
  52: {
    label: "Choose a starting node",
    choices: ["000 · left", "001 · centre", "002 · right"],
  },
  53: {
    label: "Second sensor reading",
    choices: ["Missing", "Available · 4 V"],
  },
  54: { label: "Generations to compute", max: 12, commit: "Advance the cells" },
  55: {
    label: "Held-out feature mean",
    max: 8,
    commit: "Compare with both classes",
  },
  56: {
    label: "Back-door adjustment",
    choices: ["Control for Z", "Leave Z open"],
  },
  57: {
    label: "Forecaster B’s probability",
    max: 10,
    map: (n) => n * 10 + "%",
    commit: "Update the pool",
  },
  58: {
    label: "Yes shares in this example",
    max: 8,
    commit: "Update market quote",
  },
  59: {
    label: "Integration window",
    choices: ["3 units", "9 units", "15 units", "21 units"],
  },
  60: {
    label: "Weight of branch A",
    max: 100,
    map: (n) => n + "%",
    commit: "Reweigh the branches",
  },
};
