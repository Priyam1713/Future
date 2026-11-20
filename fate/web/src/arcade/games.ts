import type { Study } from "../futures/contracts";

export const games = [
  {
    id: "play-loom",
    name: "The Living Loom",
    tag: "Cellular automaton",
    instruction:
      "Change up to three cells, then send the pattern forward four generations. Aim for the target population.",
    oracle: 54,
  },
  {
    id: "play-switch",
    name: "The Signal Switch",
    tag: "Ideal quantum simulation",
    instruction:
      "Patch the two-wire instrument to send as much measured probability as possible to the two marked outputs. Keep both outputs fed.",
    oracle: 50,
  },
  {
    id: "play-signal",
    name: "The Forecast Station",
    tag: "Synthetic forecasting exercise",
    instruction:
      "Read the incoming evidence, set your chance of a signal and seal your forecast. The station draws a simulated outcome using the native probability update.",
    oracle: 51,
  },
] as const;
export type Game = (typeof games)[number];
export type GameId = Game["id"];
export const isGame = (id: string): id is GameId =>
  games.some((game) => game.id === id);

export const programs = [
  ["Bell pair", "H on top · controlled NOT"],
  ["Independent wires", "H on both wires"],
  ["Flip lower wire", "X on lower wire"],
  ["Turn upper wire", "Quarter-turn on upper wire"],
] as const;
export const channels = ["00", "01", "10", "11"] as const;
const targets = [
  ["00", "11"],
  ["00", "10"],
  ["00", "01"],
] as const;
const clues = [
  {
    option: 0,
    ratio: "3 : 1",
    copy: "Receivers hear a repeating pulse. This clue is three times as likely when the signal is present.",
  },
  {
    option: 4,
    ratio: "5 : 1",
    copy: "A second antenna confirms the same pulse. This clue is five times as likely when the signal is present.",
  },
  {
    option: 3,
    ratio: "1 : 2",
    copy: "A ground receiver reports interference. This clue is half as likely when the signal is present.",
  },
] as const;
const seed = [9, 17, 22, 23, 24];

export function mission(round: number) {
  const n = round % 3;
  return {
    goal: [6, 8, 7][n],
    cells: Array.from({ length: 49 }, (_, i) =>
      Number(seed.some((a) => (a + n * 7) % 49 === i)),
    ),
    targets: targets[n],
    bestShare: [0.5, 0.25, 0.5][n],
    clue: clues[n],
  };
}

export function settle(
  game: GameId,
  round: number,
  forecast: number,
  study: Study,
  sample: number,
) {
  const { counts, bars } = study.view.instrument;
  const task = mission(round);
  if (game === "play-loom") {
    const population = counts!.at(-1)!;
    const gap = Math.abs(population - task.goal);
    return {
      points: Math.max(0, 100 - 15 * gap),
      title: `${population} living cells`,
      detail: `Target ${task.goal}. The native grid has ${population} at generation four. Each cell of difference costs 15 points.`,
    };
  }
  if (game === "play-switch") {
    const shares = task.targets.map(
      (bit) => bars!.find((bar) => bar.label === bit)!.value,
    );
    return {
      points: Math.min(
        100,
        Math.round((100 * Math.min(...shares)) / task.bestShare),
      ),
      title: `${(100 * (shares[0] + shares[1])).toFixed(0)}% reached the target pair`,
      detail: `${task.targets[0]} receives ${(shares[0] * 100).toFixed(0)}%. ${task.targets[1]} receives ${(shares[1] * 100).toFixed(0)}%. The smaller share earns full points at ${task.bestShare * 100}%, the best this cartridge set can deliver to both ports.`,
    };
  }
  const probability = bars!.find((bar) => bar.label === "Updated")!.value;
  const detected = sample < probability;
  const loss = (forecast / 100 - Number(detected)) ** 2;
  return {
    points: Math.round(100 * (1 - loss)),
    title: detected ? "Signal received" : "No signal this round",
    detail: `Your forecast was ${forecast}%. The native update put the chance at ${(probability * 100).toFixed(1)}% before the virtual draw. Points equal 100 times one minus squared forecast error. Over repeated rounds, honest probabilities give the best expected score.`,
  };
}
