export interface Draw {
  spread: "one" | "three";
  seed: string;
  question: string;
  reversals: boolean;
}
export interface Card {
  id: string;
  name: string;
  number: number | null;
  suit: string | null;
  rank: string;
  rank_number: number | null;
  arcana: string;
}
export interface Meaning {
  text: string;
  symbolic_focus: string;
  rule_id: string;
  version: number;
  locator: string;
  page_url: string;
  source_id: string;
  flags: string[];
}
export interface Reading {
  card: Card;
  orientation: "upright" | "reversed";
  position: { label: string; role: string };
  direct_component: Meaning;
  upright_reference: Meaning | null;
  composition: { text: string; reflection: string };
  ambiguity: string[];
  qualifications: string[];
  additional_source_account: { text: string; locator: string } | null;
}
export interface Result {
  profile: string;
  spread: string;
  question: string | null;
  readings: Reading[];
  overall: { summary: string; coverage: string };
  replay: { seed: string; protocol: string; request: unknown };
  source: { id: string; edition: string; rights_note: string };
  limitations: string[];
  predictive_validity: string;
  factual_prediction: false;
}
export interface Envelope {
  result: Result;
  receipt: string;
}
export interface Commentary {
  cards: { card_id: string; rule_id: string; reflection: string }[];
  provenance: { provider: string; model: string };
  coverage: string;
}
export async function api<T>(
  path: string,
  body?: unknown,
  signal?: AbortSignal,
): Promise<T> {
  const response = await fetch(path, {
    method: body ? "POST" : "GET",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
    signal,
  });
  let value;
  try {
    value = await response.json();
  } catch {
    throw new Error(
      "The connection faded. Please try again; your question is still here.",
    );
  }
  if (!response.ok)
    throw new Error(
      typeof value.detail === "string"
        ? value.detail
        : response.status === 422
          ? "Please check your question and try again."
          : "The connection faded. Please try again.",
    );
  return value;
}
