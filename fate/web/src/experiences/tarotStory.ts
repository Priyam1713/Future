import type { Narrative, Passage, ReadingSection } from "../codex/narrative";
import type { Result } from "../types";
import { plainGloss } from "./tarotPresentation";
import {
  cardReference, recurrence, recurrenceId, sequenceRule, spreadPositions, tarotRule,
  TAROT_EDITION, TAROT_PROFILE, type TarotSnapshot,
} from "./tarotEdition";

function composition(title: string, text: string, rules: string[]): Passage {
  return { title, text, coverage: "compositional", rules };
}
const families = {
  accord: ["concord", "harmony", "union", "alliance", "co-operation", "qualified concord"],
  discord: ["discord", "disunion", "division", "quarrel", "quarrels", "dispute", "disputes", "conflict"],
  movement: ["movement", "activity", "departure", "journey", "voyage"],
  stillness: ["inertia", "stagnation", "delay", "repose", "retreat"],
  fruition: ["prosperity", "increase", "abundance", "gain", "accomplishment"],
  loss: ["loss", "privation", "decline", "loss with something remaining", "decline of a matter"],
  inquiry: ["study", "reflection", "discernment", "wisdom", "examination"],
  uncertainty: ["doubt", "vacillation", "indecision", "perplexity", "confusion", "uncertain design"],
} as const;
type Family = keyof typeof families;
const opposites: [Family, Family][] = [["accord", "discord"], ["movement", "stillness"], ["fruition", "loss"]];

export function tarotStory(snapshot: TarotSnapshot): Narrative {
  const entries = snapshot.cards.map(({ id, orientation }, index) => {
    const card = cardReference(id);
    const meaning = card.meanings[orientation];
    const uncertain = meaning.symbolic_focus.includes(" OR ") ||
      meaning.flags.some((flag) => flag !== "primary_section_has_no_reversed_entry_explicit_section4_gap_fill");
    const motifs = meaning.symbolic_focus.replace(/^unchanged:/, "").split(";");
    return { card, orientation, meaning, uncertain, motifs,
      position: snapshot.spread === "one" ? "Focus" : spreadPositions[index],
      lead: uncertain ? "unresolved alternatives" : plainGloss(motifs[0]),
      families: uncertain ? [] : (Object.keys(families) as Family[]).filter((family) =>
        (families[family] as readonly string[]).some((word) => motifs.includes(word))),
    };
  });
  const sections: ReadingSection[] = entries.map((entry, index) => {
    const { card, meaning, position, uncertain, orientation } = entry;
    const focus = plainGloss(meaning.symbolic_focus);
    const contexts = [
      `The opening uses ${focus} as the condition brought into the spread.`,
      `In the middle, ${focus} changes what stands out in the opening card.`,
      `At the closing position, set ${focus} beside the opening and the middle as a possibility for consideration.`,
    ];
    const text = uncertain
      ? `The source gives this position ${focus}. Keep its accounts and conditions open before comparing it with another card.`
      : snapshot.spread === "one" ? `The focus is ${focus}.` : contexts[index];
    const qualification = meaning.symbolic_focus.startsWith("unchanged:")
      ? " Waite marks the reversed meaning as unchanged." : "";
    return { id: `position-${index + 1}`, title: position, passages: [
      composition(card.name, text + qualification, [meaning.rule_id]),
      { title: `Waite · ${orientation}`, text: meaning.text, coverage: "direct", rules: [meaning.rule_id] },
    ] };
  });
  const [opening, middle, closing] = entries;
  const rules = entries.map(({ meaning }) => meaning.rule_id);
  if (!middle || !closing) return { technique: 16, edition: TAROT_EDITION, sections: [
    { id: "overview", title: "A single focus", passages: [
      composition(opening.card.name,
        opening.uncertain ? `Waite leaves ${opening.card.name} open to more than one reading. Hold ${plainGloss(opening.meaning.symbolic_focus)} in view together.`
          : `${opening.card.name} puts ${opening.lead} at the center of this reading.`, rules),
    ] },
    ...sections,
  ] };

  const relationships: Passage[] = [];
  const shared = (Object.keys(families) as Family[]).map((family) =>
    ({ family, rows: entries.filter((entry) => entry.families.includes(family)) }))
    .find(({ rows }) => rows.length >= 2);
  const contrasts = opposites.flatMap(([a, b]) => entries.flatMap((left) =>
    entries.filter((right) => left !== right && left.families.includes(a) && right.families.includes(b))
      .map((right) => ({ a, b, left, right })))).at(0);
  if (shared) {
    const { family, rows } = shared;
    const words = rows.map(({ card, motifs }) =>
      `${card.name} brings ${plainGloss(motifs.find((word) => (families[family] as readonly string[]).includes(word))!)}`);
    relationships.push(composition(`A recurring theme of ${family}`,
      `${words.join(". ")}. These motifs share a theme across different positions.`,
      [sequenceRule, ...rows.map(({ meaning }) => meaning.rule_id)]));
  }
  if (contrasts) {
    const { a, b, left, right } = contrasts;
    relationships.push(composition(`${a[0].toUpperCase() + a.slice(1)} beside ${b}`,
      `${left.card.name} places ${a} at “${left.position}”. ${right.card.name} brings ${b} into “${right.position}”. Both remain visible in the spread.`,
      [sequenceRule, left.meaning.rule_id, right.meaning.rule_id]));
  }
  if (entries.every(({ orientation }) => orientation === "upright")) {
    for (const rank of ["two", "three"] as const) {
      const count = entries.filter(({ card }) => card.rank === rank && card.arcana === "minor").length;
      if (count === 2 || count === 3) {
        const id = recurrenceId(`${rank}-${count}`);
        relationships.push({ title: "Waite’s rank recurrence", text: tarotRule(id)!.text, coverage: "direct", rules: [id] });
      }
    }
  }
  const ambiguous = entries.filter(({ uncertain }) => uncertain);
  if (ambiguous.length) relationships.push({
    title: "Where the reading stays open",
    text: `The entries for ${ambiguous.map(({ card }) => card.name).join(", ")} carry alternatives or conditions. The spread leaves those readings open.`,
    coverage: "unsupported", rules: ambiguous.map(({ meaning }) => meaning.rule_id),
  });
  if (!relationships.length) relationships.push(composition("A comparison across positions",
    `${middle.card.name} puts ${middle.lead} between the opening and closing cards. The connection here is the change of emphasis across those roles.`,
    [sequenceRule, ...rules]));

  const title = contrasts ? `${contrasts.a[0].toUpperCase() + contrasts.a.slice(1)} beside ${contrasts.b}`
    : shared ? `${shared.family[0].toUpperCase() + shared.family.slice(1)} across the spread`
    : `${middle.card.name} at the center`;
  const overview = contrasts
    ? `${contrasts.left.card.name} and ${contrasts.right.card.name} pull the reading toward different emphases. The middle’s ${middle.lead} sets the context for reading the closing card beside the opening.`
    : shared
      ? `The language of ${shared.family} returns across positions. Follow the shift from the opening’s ${opening.lead} through ${middle.lead} in the middle to the closing’s ${closing.lead}.`
      : `${middle.card.name} shifts the emphasis from ${opening.lead} toward ${middle.lead}. That middle position gives a way to compare the opening with the closing card’s ${closing.lead}.`;
  const ending = ambiguous.length
    ? `Read ${closing.card.name} beside ${opening.card.name} and ${middle.card.name}. Keep the closing emphasis on ${closing.lead} alongside the spread’s unresolved source accounts.`
    : contrasts
      ? `Read the closing emphasis on ${closing.lead} in light of the spread’s tension between ${contrasts.a} and ${contrasts.b}. What remains of the opening’s ${opening.lead} after the middle brings in ${middle.lead}?`
      : `Consider ${closing.lead} in relation to ${opening.lead} at the opening and ${middle.lead} in the middle. What from the opening still has a place at the end of the spread?`;
  return { technique: 16, edition: TAROT_EDITION, sections: [
    { id: "overview", title, passages: [composition(title,
      overview,
      [sequenceRule, ...rules])] },
    ...sections,
    { id: "relationships", title: "Connections in the spread", passages: relationships },
    { id: "closing", title: "Read the three together", passages: [composition("The closing position",
      ending,
      [sequenceRule, ...rules])] },
  ] };
}

export function matchesLiveStory(result: Result, snapshot: TarotSnapshot): boolean {
  return result.profile === TAROT_PROFILE && result.spread === snapshot.spread &&
    result.readings.length === (snapshot.spread === "three" ? 3 : 1) &&
    result.readings.every(({ card, orientation, position, direct_component: meaning }, index) => {
      const pinned = cardReference(card.id)?.meanings[orientation];
      return position.label === (snapshot.spread === "one" ? "Focus" : spreadPositions[index]) &&
        pinned?.rule_id === meaning.rule_id && pinned.text === meaning.text &&
        pinned.symbolic_focus === meaning.symbolic_focus;
    });
}
