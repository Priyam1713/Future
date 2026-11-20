import type { Screen } from "../hooks/useOracle";
import { ROOMS as FUTURES } from "../futures/contracts";
import { ROOMS as FOLIOS } from "../manuscript/contracts";
import { ROOMS as CHAMBERS } from "../chambers/contracts";
import { RITUAL_ROOMS } from "../ritual/contracts";
import { SIGNS } from "../signs/contracts";
import inventory from "./inventory.json";

type World = {
  id: string;
  title: string;
  description: string;
  art: string;
  focus: string;
  featured: number;
  rooms: readonly number[];
};

export const worlds = [
  {
    id: "sky",
    title: "The Celestial Court",
    description: "Birth charts, celestial cycles and the patterns in a name.",
    art: "folio-court",
    focus: "64% 52%",
    featured: 1,
    rooms: [1, 2, 3, 4, 5, 6, 7],
  },
  {
    id: "ritual",
    title: "The Ritual Wing",
    description: "Turn cards, cast coins and read symbols drawn by hand.",
    art: "ritual-oracle",
    focus: "54% 62%",
    featured: 16,
    rooms: [16, 17, 18, 19, 20, 21, 22, 33, 36],
  },
  {
    id: "dream",
    title: "The Dream Archive",
    description: "Keep a dream, open a manuscript or conduct a blind trial.",
    art: "future-dream",
    focus: "64% 47%",
    featured: 43,
    rooms: [23, 24, 26, 43, 44, 45, 46],
  },
  {
    id: "tomorrow",
    title: "The Tomorrow Machine",
    description: "Wire a circuit, test a model and watch trajectories diverge.",
    art: "future-tomorrow",
    focus: "63% 48%",
    featured: 50,
    rooms: [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
  },
  {
    id: "earth",
    title: "The World of Signs",
    description: "Explore declared signs in water, flame, stone and direction.",
    art: "signs-table",
    focus: "58% 60%",
    featured: 40,
    rooms: [28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40],
  },
  {
    id: "human",
    title: "The Human Manuscript",
    description:
      "Read a hand by observation and examine historical beliefs in context.",
    art: "folio-manuscript",
    focus: "57% 56%",
    featured: 8,
    rooms: [8, 9, 10, 11, 12, 13, 14, 15],
  },
] as const satisfies readonly World[];

const labels: Record<number, [string, string]> = {
  1: [
    "Western Astrology",
    "Turn a calculated birth chart and explore its planets.",
  ],
  2: [
    "Vedic Astrology",
    "Explore sidereal charts, lunar mansions and dasha periods.",
  ],
  3: [
    "Chinese BaZi",
    "Examine the stems and branches of four calculated pillars.",
  ],
  4: ["Numerology", "Uncover three symbolic numbers from a name and date."],
  5: ["Horary Astrology", "Inspect chart diagnostics for a question."],
  6: [
    "Mundane Astrology",
    "Explore historical ingresses and planetary cycles.",
  ],
  7: [
    "Astrocartography",
    "Follow calculated angular lines across a world map.",
  ],
  8: ["Palmistry", "Select the lines you observe on an illustrated hand."],
  9: ["Face Reading", "Read a historical archive of physiognomy."],
  10: [
    "Phrenology",
    "Examine a discredited practice in its historical context.",
  ],
  11: ["Moleosophy", "Look up historical associations with body marks."],
  12: ["Podomancy", "Explore historical foot-reading references."],
  13: ["Graphology", "Review historical writing classifications."],
  14: ["Aura Reading", "Explore historical colour symbolism."],
  15: ["Iridology", "Examine historical iris charts and their limitations."],
  16: ["Tarot", "Turn an illustrated card and read its source motifs."],
  17: ["Oracle Cards", "Lay out an illustrated Lenormand line."],
  18: ["I Ching", "Cast six lines and explore how they change."],
  19: ["Runes", "Uncover engraved stones and their distinct sources."],
  20: ["Pendulum", "Observe a pendulum or try a seeded symbolic exercise."],
  21: ["Crystal Ball", "Use living glass as a prompt for your own notes."],
  22: ["Mirror Scrying", "Reflect on what you observe in a dark mirror."],
  23: [
    "Dream Interpretation",
    "Choose a dream motif and find historical readings.",
  ],
  24: ["Automatic Writing", "Write a first draft or open a teaching excerpt."],
  26: ["Akashic Records", "Open a historical practitioner’s reference."],
  28: ["Tea Leaves", "Declare the shape and position you see in a cup."],
  29: ["Coffee Grounds", "Read documented references for a declared mark."],
  30: ["Flame Signs", "Look up a declared observation of a flame."],
  31: ["Water Signs", "Explore a declared water observation."],
  32: ["Air Signs", "Explore a declared sky or weather observation."],
  33: ["Geomancy", "Mark four Mothers and watch fifteen figures form."],
  34: ["Lithomancy", "Place declared stones on the table of signs."],
  35: ["Osteomancy", "Examine a documentary archive of oracle bones."],
  36: ["Bibliomancy", "Choose a passage in the pinned source book."],
  37: ["Cleromancy", "Declare a lot and read its documented context."],
  38: ["Augury", "Consult sources for a declared bird observation."],
  39: ["Haruspicy", "Open documented Roman cases in their historical context."],
  40: ["Feng Shui", "Set a bearing and read the compass’s 24 mountains."],
  43: [
    "Remote Viewing",
    "Commit a target, lock two submissions and open the seal.",
  ],
  44: [
    "Prophetic Dreams",
    "Lock a dream before the observation window closes.",
  ],
  45: [
    "Intuitive Prediction",
    "Test which declared cue distinguishes two options.",
  ],
  46: ["Déjà Rêvé", "Annotate the features of a remembered experience."],
  49: [
    "Time-series Forecasting",
    "Compare model traces or open a historical NOAA study.",
  ],
  50: [
    "Quantum Simulation",
    "Route two wires and compare their outcome probabilities.",
  ],
  51: ["Superforecasting", "See how new evidence changes a prior probability."],
  52: [
    "Population Dynamics",
    "Light a starting node and follow its neighbours.",
  ],
  53: [
    "Digital Twin",
    "See how a missing measurement changes a synthetic twin.",
  ],
  54: [
    "Cellular Automata",
    "Draw a pattern in cells and advance its generations.",
  ],
  55: [
    "Intention Classification",
    "Test a class boundary with synthetic offline features.",
  ],
  56: [
    "Causal Graphs",
    "Explore what changes when you control for a confounder.",
  ],
  57: [
    "Collective Forecasts",
    "Pool probabilities from synthetic forecasters.",
  ],
  58: ["Prediction Markets", "Move a model quote by buying simulated shares."],
  59: ["Lorenz Chaos", "Scrub two near-identical starts as they diverge."],
  60: ["Scenario Trees", "Change a branch weight and inspect the outcomes."],
};

const routes = new Map<number, Screen>([
  [1, "western"],
  [4, "numerology"],
  [16, "ritual"],
  ...Object.entries(CHAMBERS).map(
    ([id, value]) => [Number(id), value.slug] as const,
  ),
  ...Object.entries(RITUAL_ROOMS).map(
    ([id, value]) => [Number(id), value.slug] as const,
  ),
  ...Object.entries(SIGNS).map(
    ([id, value]) => [Number(id), value.slug] as const,
  ),
  ...Object.entries(FOLIOS).map(
    ([id, value]) => [Number(id), value[0]] as const,
  ),
  ...Object.entries(FUTURES).map(
    ([id, value]) => [Number(id), value[0]] as const,
  ),
]);

export const rooms = inventory.methods.map((method) => ({
  method,
  screen: routes.get(method.id)!,
  name: labels[method.id][0],
  description: labels[method.id][1],
  historical:
    (method.id >= 9 && method.id <= 15) ||
    method.id === 26 ||
    method.id === 35 ||
    method.id === 39,
}));

export type GalleryRoom = (typeof rooms)[number];
export type GalleryWorld = (typeof worlds)[number];
