import catalog from "./index-v1.json";

export const ROOMS = {
  24: ["automatic-writing", "Automatic Writing", "The Unwritten Page", "draft"],
  26: ["akashic", "Akashic Records", "The Archive of Claims", "index"],
  43: ["remote-viewing", "Remote Viewing", "The Sealed Gallery", "sealed"],
  44: ["prophetic-dreams", "Prophetic Dreams", "The Dream Ledger", "ledger"],
  45: [
    "intuitive-prediction",
    "Intuitive Prediction",
    "The First Useful Clue",
    "cue",
  ],
  46: ["deja-reve", "Déjà Rêvé", "The Echo of a Dream", "memory"],
  49: [
    "forecast-models",
    "Predictive Modeling",
    "The Forecast Spectrograph",
    "series",
  ],
  50: [
    "quantum-circuit",
    "Quantum Simulation",
    "The Quantum Switchyard",
    "circuit",
  ],
  51: [
    "forecast-updates",
    "Superforecasting",
    "The Probability Balance",
    "posterior",
  ],
  52: [
    "population-dynamics",
    "Psychohistory",
    "The Threshold Constellation",
    "network",
  ],
  53: ["digital-twin", "Digital Twins", "The Second Instrument", "sensor"],
  54: ["cellular-automata", "Agent-Based Models", "The Cell Loom", "cells"],
  55: [
    "intention-classifier",
    "Brain Intention",
    "The Feature Comparator",
    "scatter",
  ],
  56: ["causal-graphs", "Causal AI", "The Causal Orrery", "graph"],
  57: [
    "collective-forecasts",
    "Collective Intelligence",
    "The Signal Confluence",
    "pool",
  ],
  58: [
    "prediction-market",
    "Prediction Markets",
    "The Exchange of Odds",
    "market",
  ],
  59: ["lorenz-chaos", "Chaos Theory", "The Lorenz Chamber", "orbit"],
  60: [
    "scenario-trees",
    "Multiverse Scenarios",
    "The Forking Observatory",
    "tree",
  ],
} as const;
export type Id = keyof typeof ROOMS;
export type StudyId = Exclude<Id, 43>;
export type Slug = (typeof ROOMS)[Id][0];
export const roomIds = Object.keys(ROOMS).map(Number) as Id[];
export const isFuture = (n: number): n is Id => Object.hasOwn(ROOMS, n);
export const futureId = (slug: string) =>
  roomIds.find((id) => ROOMS[id][0] === slug);
export const edition = "fate-future-studies-v1";
export const index = catalog as Record<
  StudyId,
  { maximum: number; default: number }
>;
export type FutureBookmark = {
  oracle: StudyId;
  profile: typeof edition;
  option: number;
};
export function isFutureBookmark(value: {
  oracle: number;
}): value is FutureBookmark {
  return isFuture(value.oracle) && value.oracle !== 43;
}
export function validateFutureBookmark(
  value: Record<string, unknown>,
): value is FutureBookmark {
  if (
    Object.keys(value).length !== 3 ||
    value.profile !== edition ||
    typeof value.oracle !== "number" ||
    !isFutureBookmark({ oracle: value.oracle }) ||
    typeof value.option !== "number"
  )
    return false;
  return (
    Number.isSafeInteger(value.option) &&
    value.option >= 0 &&
    value.option <= index[value.oracle as StudyId].maximum
  );
}
export type Source = {
  id: string;
  title: string;
  url: string;
  locator: string;
};
export type Readout = { status: string; title: string; lead: string };
export type Mark = { label: string; value: number };
export type Track = { label: string; points: [number, number][] };
export type Node = {
  id: string;
  parent: string | null;
  mass: string;
  depth: number;
  utility: string | null;
};
export type InstrumentData = {
  labels?: string[];
  notes?: string[];
  text?: string;
  bars?: Mark[];
  series?: Track[];
  points?: { label: string; xy: [number, number] }[];
  gates?: { op: string; target: number; control?: number }[];
  frames?: number[][];
  counts?: number[];
  links?: [string, string][];
  nodes?: Node[];
};
export type Study = {
  oracle: StudyId;
  result: Record<string, unknown>;
  private: boolean;
  view: Readout & { instrument: InstrumentData };
  sources: Source[];
};
