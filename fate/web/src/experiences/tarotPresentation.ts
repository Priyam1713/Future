import type { Reading } from "../types";
/** Editorial glosses only; never replace native output, source wording or rules.
 * Alternatives remain alternatives. No question-specific inference is added. */
const plain: Record<string, string> = {
  folly: "unwise choices",
  extravagance: "excess",
  disquiet: "unease",
  vacillation: "indecision",
  concord: "agreement",
  contrariety: "opposition",
  prudence: "careful judgment",
  circumspection: "caution",
  dissimulation: "concealment",
  equity: "fairness",
  probity: "integrity",
  privation: "hardship",
  haughtiness: "pride",
  recompense: "reward",
  superfluity: "excess",
  vehemence: "intensity",
  inertia: "inaction",
  lethargy: "low energy",
  disunion: "division",
  fruitfulness: "growth",
  presumption: "overconfidence",
};
export function plainThemes(reading: Reading) {
  return plainGloss(reading.direct_component.symbolic_focus);
}
export function plainGloss(focus: string) {
  return focus
    .replace(/^(?:unchanged|varying accounts):\s*/, "")
    .split(" OR ")
    .map((alternative) =>
      alternative
        .split(";")
        .map((t) => plain[t.trim()] ?? t.trim())
        .join(", "),
    )
    .join(" — or, in an alternative account, ");
}
