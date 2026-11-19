import data from "./reference-v1.json";
import type { Evidence } from "../codex/reference";
import type { ChamberSnapshot, CoinSnapshot } from "./contracts";

export const { vedic, bazi, iching, runes } = data;
export const pillarNames = ["year", "month", "day", "hour"] as const;
export const stone = (id: string) => runes.stones.find((row) => row.id === id)!;
export const figure = (n: number) => iching.figures[n - 1];
export const isMoving = (value: number) => value === 6 || value === 9;
type Source = { id: string; url: string | null; author: string };
type Text = { text: string; source_id: string; locator: string };

export function citation(
  label: string,
  row: Text,
  sources: Source[],
  alternative = false,
): Evidence {
  const source = sources.find((source) => source.id === row.source_id);
  return {
    label,
    quote: row.text,
    wording: row.text,
    sourceId: row.source_id,
    locator: row.locator,
    url: source?.url ?? "",
    alternative,
  };
}

export function coinTexts(snapshot: CoinSnapshot) {
  const [initial, resulting] = snapshot.figures.map(figure);
  const moving = snapshot.values.flatMap((value, i) =>
    isMoving(value)
      ? [
          citation("Changing line " + (i + 1), initial.lines[i], [
            iching.source,
          ]),
        ]
      : [],
  );
  if (moving.length === 6 && initial.special_all_changing)
    moving.push(
      citation("All six lines change", initial.special_all_changing, [
        iching.source,
      ]),
    );
  return { initial, resulting, moving };
}

export function chapterName(s: ChamberSnapshot) {
  switch (s.oracle) {
    case 2:
      return (
        vedic.mansions[s.mansion[0]] +
        " Moon · " +
        vedic.signs[s.asc[1]] +
        " Lagna"
      );
    case 3:
      return bazi.pairs[s.pairs[2]].stem.name + " Day Master";
    case 18:
      return s.figures[0] === s.figures[1]
        ? figure(s.figures[0]).name
        : s.figures.map((n) => figure(n).name).join(" → ");
    case 19:
      return s.runes.map((id) => stone(id).name).join(" · ");
  }
}

export function chamberEvidence(s: ChamberSnapshot): Evidence[] {
  switch (s.oracle) {
    case 2:
      return vedic.rules
        .filter((rule) =>
          [
            "vedic.sidereal",
            "vedic.nakshatra",
            "vedic.d9",
            "vedic.vimshottari",
          ].includes(rule.id),
        )
        .map((rule) =>
          citation(
            rule.id,
            { ...rule, text: rule.method },
            vedic.sources,
            true,
          ),
        );
    case 3:
      return [
        bazi.masters[bazi.pairs[s.pairs[2]].stem.index],
        ...bazi.topics,
      ].map((row, i) =>
        citation(
          i
            ? "Pillar topic · " + bazi.topics[i - 1].pillar
            : "Documented Day Master imagery",
          row,
          bazi.sources,
        ),
      );
    case 18: {
      const { initial, resulting, moving } = coinTexts(s);
      return [
        citation("Initial judgment · " + initial.name, initial.judgment, [
          iching.source,
        ]),
        ...moving,
        ...(initial.number !== resulting.number
          ? [
              citation(
                "Relating judgment · " + resulting.name,
                resulting.judgment,
                [iching.source],
              ),
            ]
          : []),
      ];
    }
    case 19:
      return s.runes.map((id) => {
        const r = stone(id);
        const entry = r.historical_reference;
        return {
          ...citation(
            r.name + " · modern editorial reflection",
            {
              text: r.composition.reflection,
              source_id: entry.source_id,
              locator: entry.locator,
            },
            runes.sources,
          ),
          quote: r.composition.theme,
          alternative: true,
        };
      });
  }
}
