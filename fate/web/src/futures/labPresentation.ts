import type { Mark, Study } from "./contracts";

export function probability(value: number) {
  return (
    (value * 100).toFixed(
      (value > 0 && value < 0.0005) || (value > 0.995 && value < 1) ? 2 : 1,
    ) + "%"
  );
}

export function likelyOutcomes(rows: Mark[]) {
  return rows.filter(({ value }) => value > 0.000000001);
}

export function simulationTime(label: string) {
  const [value, denominator = "1"] = label.split("/");
  return (Number(value) / Number(denominator)).toFixed(2);
}

export function labReadout(study: Study) {
  const { view } = study;
  const rows = view.instrument.bars ?? [];
  if (study.oracle === 50) {
    const possible = likelyOutcomes(rows);
    const chance = possible[0]?.value;
    if (chance === undefined) return view;
    const equal = possible.every(
      ({ value }) => Math.abs(value - chance) < 1e-10,
    );
    return {
      status: "Ideal two-wire circuit",
      title:
        possible.length === 1
          ? `${possible[0].label} every time`
          : equal
            ? `${possible.length} equally likely outcomes`
            : "Unequal outcomes",
      lead:
        possible.length === 1
          ? "This circuit places all measured probability on one bitstring."
          : equal
            ? `${possible.map(({ label }) => label).join(", ")} each have ${probability(chance)} probability in this simulation.`
            : "The output bars show how the circuit divides probability among the measured bitstrings.",
    };
  }
  if (study.oracle === 58) {
    const yes = rows.find(({ label }) => label === "YES");
    if (yes)
      return {
        status: "Simulated market · play credits",
        title: `Yes trades at ${probability(yes.value)}`,
        lead: "The quote comes from the market’s cost function. Buying simulated shares moves the quote.",
      };
  }
  if (study.oracle === 59) {
    const separation = view.instrument.counts?.at(-1);
    if (separation !== undefined)
      return {
        status: "Lorenz equations · simulated trajectories",
        title: `${separation.toFixed(3)} apart at the final sample`,
        lead: "Two nearly identical starts follow the same equations. Scrub backward to see when the gap opens.",
      };
  }
  return view;
}
