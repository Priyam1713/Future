import { evidenceFor, type Evidence } from "./reference";
import type { Chapter } from "./records";
/** Small, explicit editorial vocabulary. Matching refers to source language,
 * not independent agreement, predictive validity or a combined interpretation. */
export const THEME_VOCABULARY_VERSION = "fate-source-language-v1";
const vocabulary = [
  {
    label: "Beginnings & initiative",
    pattern: /\b(beginning|beginnings|initiation|initiative|enterprise)\b/i,
  },
  {
    label: "Creativity & expression",
    pattern: /\b(creative|creativity|creation|artistry|communication)\b/i,
  },
  {
    label: "Cooperation & connection",
    pattern: /\b(cooperation|alliance|concord|agreement|friendship)\b/i,
  },
  {
    label: "Care & responsibility",
    pattern:
      /\b(care|service|compassion|compassionate|humanitarian|responsibility|charity)\b/i,
  },
  {
    label: "Change & flexibility",
    pattern: /\b(change|adaptability|flexibility|mutation|renewal)\b/i,
  },
  {
    label: "Study & reflection",
    pattern: /\b(inquiry|reflection|study|contemplation|wisdom|discernment)\b/i,
  },
  {
    label: "Order & sustained effort",
    pattern:
      /\b(order|organization|construction|stability|sustained|perseverance)\b/i,
  },
  {
    label: "Completion & release",
    pattern: /\b(completion|release|end|ending)\b/i,
  },
  {
    label: "Work & resources",
    pattern: /\b(work|management|ambition|material|stewardship|business)\b/i,
  },
  {
    label: "Tension & uncertainty",
    pattern:
      /\b(doubt|instability|quarrel|discord|dispute|conflict|fear|anxiety)\b/i,
  },
];
export function compareChapters(left: Chapter, right: Chapter) {
  const a = evidenceFor(left.snapshot),
    b = evidenceFor(right.snapshot);
  const groups = vocabulary.map((t) => ({
    label: t.label,
    left: a.filter((e) => !e.alternative && t.pattern.test(e.quote)),
    right: b.filter((e) => !e.alternative && t.pattern.test(e.quote)),
  }));
  return {
    vocabulary: THEME_VOCABULARY_VERSION,
    echoes: groups.filter((g) => g.left.length && g.right.length),
    leftOnly: groups.filter((g) => g.left.length && !g.right.length),
    rightOnly: groups.filter((g) => g.right.length && !g.left.length),
    leftEvidence: a,
    rightEvidence: b,
    alternatives: [...a, ...b].filter((e) => e.alternative),
    samePattern:
      JSON.stringify(left.snapshot) === JSON.stringify(right.snapshot),
  };
}
export type Comparison = ReturnType<typeof compareChapters>;
