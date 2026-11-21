import { phaseRelationships, type BaziReading } from "../chambers/BaziReading";
import type { BaziSnapshot, VedicSnapshot } from "../chambers/contracts";
import {
  dignities, grahaOwnership, grahaTopics, subperiodTopic, type JyotishReading,
} from "../chambers/JyotishReading";
import { bazi, pillarNames, vedic } from "../chambers/reference";
import { NARRATIVE_EDITIONS, type Narrative, type Passage, type ReadingSection } from "./narrative";

const composition = (title: string, text: string, ...rules: string[]): Passage =>
  ({ title, text, coverage: "compositional", rules });
const direct = (title: string, text: string, ...rules: string[]): Passage =>
  ({ title, text, coverage: "direct", rules });

export function jyotishNarrative(s: VedicSnapshot, reading: JyotishReading): Narrative | undefined {
  if (reading.profile !== NARRATIVE_EDITIONS[2]) return;
  const passage = (p: JyotishReading["chapters"][number]) => composition(p.title, p.text, ...p.rule_ids);
  const [lagna, lunar, period] = reading.chapters;
  const periods = reading.timing;
  const main = periods.main[0].lord;
  const signDignities = (flags: string[]) =>
    flags.map((flag) => dignities[flag]).filter(Boolean).join(" · ") || "No supported sign dignity";
  const grahas = vedic.grahas.map((name, i): ReadingSection => {
    const p = reading.grahas[name];
    const [, d1Sign, d1House, , d9Sign, d9House] = s.planets[i];
    const dignity = p.d1.moolatrikona === true ? " · Moolatrikona" : "";
    const scope = typeof p.d1.moolatrikona === "string" && !p.nodal
      ? " The source’s Mars interval is disputed and remains open." : "";
    return { id: name, title: `${name} across the two charts`, passages: [
      passage(p.comparison),
      composition("Rashi and Navamsa conditions",
        `Rashi · ${vedic.signs[d1Sign]} · House ${d1House} · ${signDignities(p.d1.dignities)}${dignity}. ` +
        `Navamsa · ${vedic.signs[d9Sign]} · House ${d9House} · ${signDignities(p.d9.dignities)}. ` +
        `Sign rulers · ${p.d1.ruler} in D1, ${p.d9.ruler} in D9.${scope}`, "vedic.d9", "vedic.dignity"),
      composition("House topics and ownership", `${grahaTopics(name, p)} ${grahaOwnership(name, p)}`,
        "fate.jyotish.v1.grahas", "fate.jyotish.v1.houses", "vedic.houses"),
      ...p.contacts.map((edge) => composition("Graha drishti",
        `${edge.from} looks to ${edge.target_sign} from ${edge.place_from_planet} signs away by inclusive count` +
        `${edge.targets.length ? " · " + edge.targets.join(", ") : ""}.`, "vedic.drishti")),
    ] };
  });
  return { technique: 2, edition: NARRATIVE_EDITIONS[2], sections: [
    { id: "lagna", title: "The rising pattern", passages: [passage(lagna)] },
    { id: "lunar", title: "Your lunar mansion", passages: [
      passage(lunar),
      ...(s.mansion[2] ? [composition("Mansion boundary",
        "This placement is close to a mansion or quarter boundary.", "vedic.nakshatra")] : []),
    ] },
    ...grahas,
    { id: "periods", title: "Vimshottari periods", passages: [
      passage(period),
      ...periods.sub.filter((_, i) => i !== s.active).map(({ lord }) =>
        composition(`${lord} subperiod`,
          subperiodTopic(reading.grahas[main].house_topic, reading.grahas[lord].house_topic),
          ...period.rule_ids)),
    ] },
  ] };
}

export function baziNarrative(s: BaziSnapshot, result: Partial<BaziReading>): Narrative | undefined {
  const { reading, pillars } = result;
  if (!reading || !pillars) return;
  const pairs = s.pairs.map((i) => bazi.pairs[i]);
  const day = pairs[2].stem;
  const sections: ReadingSection[] = [{
    id: "day-master", title: "The Day Master",
    passages: [composition(`${day.name}, the Day Master`, reading.summary, bazi.masters[day.index].id)],
  }];
  for (const [index, name] of pillarNames.entries()) {
    const pair = pairs[index];
    const pillar = pillars[name];
    const component = reading.pillars.find((row) => row.pillar === name);
    if (!component) return;
    sections.push({
      id: name, title: `${name[0].toUpperCase()}${name.slice(1)} · ${pair.name}`,
      passages: [
        direct("Documented pillar topic", component.documented_topic.text, bazi.topics[index].id),
        ...(name !== "day" ? [composition(pillar.ten_god.name, component.reason, "chinese.ten-gods")] : []),
        ...pillar.hidden_stems.map(({ stem, ten_god }) =>
          composition(`${stem.name} · ${stem.element} · ${ten_god.name}`, ten_god.reason,
            "chinese.hidden-stems", "chinese.ten-gods")),
        ...reading.element_interactions.filter((row) => row.to_pillar === name).map((row) =>
          composition(`${row.from_pillar} · ${row.from_element} → ${row.to_element}`,
            phaseRelationships[row.relation], "chinese.ten-gods")),
      ],
    });
  }
  return { technique: 3, edition: NARRATIVE_EDITIONS[3], sections };
}
