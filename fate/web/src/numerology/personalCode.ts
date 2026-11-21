import type { Narrative, Passage, ReadingSection } from "../codex/narrative";
import type { NumberResult } from "../experiences/contracts";
import { NUMBER_EDITION, numberRules } from "./readingEdition";

export const numberSections = [
  "life-path", "expression", "soul-urge", "personality", "birthday", "cycles", "connections",
] as const;

const context = (title: string, text: string, ...rules: string[]): Passage =>
  ({ title, text, coverage: "compositional", rules });
const limited = (coverage: "calculated" | "unsupported", title: string, text: string, rule: string): Passage =>
  ({ title, text, coverage, rules: [rule] });

function direct(title: string, id: string): Passage | undefined {
  const rule = Object.hasOwn(numberRules, id) ? numberRules[id] : undefined;
  if (rule?.text) return { title, text: rule.text, coverage: "direct", rules: [id] };
}

export function personalCode(result: NumberResult): Narrative | undefined {
  if (result.profile !== "decoz-component-reduction") return;
  const current = result.name.basis === "current";
  const life = result.life_path.result;
  const birthDay = result.birthday.original_day;
  const year = result.cycles.year.result;
  const month = result.cycles.month.result;
  const day = result.cycles.day.result;
  const lifeRule = `decoz.life-path.${life}`;
  const birthdayRule = `decoz.birthday.${birthDay}`;
  const lifeReading = direct(`Life Path ${life}`, lifeRule);
  const birthdayReading = direct(`Birthday ${birthDay}`, birthdayRule);
  const yearReading = direct(`Personal Year ${year}`, `decoz.year.${year}`);
  if (!lifeReading || !birthdayReading || !yearReading) return;
  const soulRule = `decoz.soul-urge.${result.soul_urge.result}`;
  const personalityRule = `decoz.personality.${result.personality.result}`;

  function nameSection(id: string, title: string, value: number | null, letters: string): ReadingSection {
    const heading = value === null ? title : `${title} ${value}`;
    const missing = value === null
      ? limited("unsupported", heading, `The name has no letters that qualify for the ${letters} total.`, "decoz.name-roles")
      : limited("unsupported", `Minor ${heading}`, "This value comes from your current name. This edition leaves its number-specific Minor interpretation open.", "decoz.current-name");
    const passage = current || value === null ? missing : direct(heading, `decoz.${id}.${value}`);
    return { id, title, passages: [passage ?? limited("unsupported", heading, "This value has no reviewed interpretation in the current edition.", "decoz.name-roles")] };
  }

  return { technique: 4, edition: NUMBER_EDITION, sections: [
    { id: "life-path", title: "Life Path", passages: [lifeReading] },
    nameSection("expression", "Expression", result.expression.result, "all-letter"),
    nameSection("soul-urge", "Soul Urge", result.soul_urge.result, "vowel"),
    nameSection("personality", "Personality", result.personality.result, "consonant"),
    { id: "birthday", title: "Birthday", passages: [
      birthdayReading,
      limited("calculated", "Reduced companion", `The calculation also records ${result.birthday.companion.result} as the reduced companion. The Birthday passage corresponds to day ${birthDay}.`, birthdayRule),
    ] },
    { id: "cycles", title: "Personal cycles", passages: [
      yearReading,
      limited("calculated", `Personal Month ${month}`, "The calendar month sets this value within the Personal Year. A standalone symbolic meaning is outside this edition.", "decoz.month-method"),
      limited("calculated", `Personal Day ${day}`, "The calendar day sets this value within the Personal Month. A standalone symbolic meaning is outside this edition.", "decoz.day-method"),
    ] },
    { id: "connections", title: "Connections", passages: [
      context(`Life Path ${life} and Birthday ${birthDay}`,
        "Read the Birthday as a particular ability alongside the longer Life Path. Where could the Birthday's emphasis help you engage with the direction described in the Life Path?",
        "decoz.birthday-role", lifeRule, birthdayRule),
      ...(!current && Object.hasOwn(numberRules, soulRule) && Object.hasOwn(numberRules, personalityRule) ? [
        context(`Soul Urge ${result.soul_urge.result} and Personality ${result.personality.result}`,
          "Compare what the vowel reading values from within with what the consonant reading describes at first encounter. Their roles stay distinct even when they produce the same number.",
          "decoz.name-roles", soulRule, personalityRule),
      ] : []),
    ] },
  ] };
}
