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
  return reading.direct_component.symbolic_focus
    .split(" OR ")
    .map((alternative) =>
      alternative
        .split(";")
        .map((t) => plain[t.trim()] ?? t.trim())
        .join(", "),
    )
    .join(" — or, in an alternative account, ");
}
export function reflectionPrompt(
  reading: Reading,
  index: number,
  total: number,
) {
  const themes = plainThemes(reading);
  if (total === 1)
    return `With “${themes}” in mind, what feels useful to explore in your question?`;
  return [
    `Looking back, which part of “${themes}” feels useful to reflect on?`,
    `Pause with “${themes}”. What, if anything, resonates with the present moment?`,
    `As you consider a next step, what would you like to explore in “${themes}”?`,
  ][index];
}
