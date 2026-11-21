import frozen from "../../../../knowledge/numerology_readings_v1.json";

export const NUMBER_EDITION = "fate-decoz-personal-code-v1";
const site = "https://www.worldnumerology.com/";
const core = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33];
const lifePath = [
  "The long arc emphasizes self-direction. Decoz places particular weight on taking responsibility for a path you choose.",
  "The long arc centers on patience and working with different points of view. Sensitivity to other people is part of how this path makes room for cooperation.",
  "Creative expression is central to this path. Decoz pairs the ease of finding a voice with the discipline needed to develop it.",
  "This path emphasizes building through method and effort. Its practical approach favors steady progress even when a shortcut looks inviting.",
  "The path centers on variety and the freedom to explore. Curiosity and adaptability matter when circumstances shift.",
  "Care and service give this path its direction. Decoz also emphasizes leaving room for others to make their own choices.",
  "Investigation is central to this path. Reflection and sustained attention help it move from unanswered questions toward understanding.",
  "This path emphasizes leadership and material stewardship. Decoz reads the management of resources as a recurring concern.",
  "The path places personal effort in a wider human context. Its symbols emphasize compassion and commitment to causes that serve others.",
  "Decoz associates this path with sensitivity and an ability to inspire. The emphasis is on what an insight sets in motion for others.",
  "This path concerns giving a large vision a durable form. Bringing other people into a shared undertaking is part of the work.",
  "This path links service with teaching. Its emphasis is on extending care and sharing what has been learned in ways others can use.",
];
const soul = [
  "Decoz puts autonomy at the center of this desire. The pull is toward making choices on your own terms and accepting responsibility for them.",
  "This desire emphasizes peaceful surroundings and close companionship. Considered from the inside, harmony is something worth tending.",
  "Play and making things with words are sources of pleasure in this account. Decoz also asks how the same expressive energy might give deeper feelings a voice.",
  "A stable routine and a dependable place in other people's lives sit at the center of this account. Practical order is part of what makes the work satisfying.",
  "The inner emphasis is freedom to encounter something unfamiliar. Variety, movement and the chance to follow a curiosity are central to this desire.",
  "Care for home and close relationships is a strong motive in this account. Decoz also makes room for the caregiver's own needs.",
  "The desire is to understand what lies beneath a first explanation. Study, analysis and time alone with a question are part of that satisfaction.",
  "This desire sets its sights on substantial undertakings and tangible results. It includes the wish to organize resources on a larger scale.",
  "This account draws satisfaction from contributing to a wider good. Its ideals extend beyond a single circle of friends or interests.",
  "A wish to reconcile differences sits alongside an attraction to ideas and worthwhile causes. Decoz gives sensitivity a place in that inner life.",
  "The central desire is to make something whose effects endure. Decoz frames its ambition as a wish to give a consequential idea practical form.",
  "The inner theme is giving through care and teaching. The account also asks how to sustain that commitment while taking care of your own needs.",
];
const personality = [
  "The first impression emphasizes capability and self-possession. Decoz pairs that presence with the risk of seeming unreceptive.",
  "People are described as first meeting a considerate and attentive presence. Listening and gentleness give this number its outward character.",
  "This first impression has the energy of a lively conversation. Decoz emphasizes wit and warmth, with room for more depth beyond the opening exchange.",
  "Reliability and a practical manner are the qualities others notice here. Decoz emphasizes being judged by the quality of the work.",
  "This outward style conveys curiosity and ease with new company. Its readiness for variety can also be read as restlessness.",
  "The outward emphasis is reassurance. Warmth and a sense of fairness make this the figure others may approach for comfort.",
  "A reserved, thoughtful presence is central to this account. Decoz describes someone whose interest in a question may be easier to see than their feelings.",
  "This first impression conveys confidence and authority. Decoz associates it with appearing able to take charge of a practical situation.",
  "Decoz describes a composed, expressive bearing. It can be read as grace or as distance, depending on the encounter.",
  "The outward account emphasizes sensitivity and a gentle approach. Decoz describes a welcome that can coexist with guarded confidence.",
  "This first impression centers on steadiness and competence. The source describes the kind of presence others may rely on to keep work on course.",
  "The outward emphasis is protective warmth and fairness. Decoz pairs that reassuring presence with the possibility of taking on too much for others.",
];
const birthdays = [
  "The day emphasizes taking the lead and putting ideas to practical use.",
  "The day marks a talent for cooperation and making a tense setting gentler.",
  "The emphasis is an eye for arrangement and artistry in everyday surroundings.",
  "The talent lies in careful execution and taking obligations seriously.",
  "The day emphasizes adapting quickly and finding words that engage other people.",
  "The emphasis is care expressed through useful help and close relationships.",
  "The day gives attention to reflection and the development of inner conviction.",
  "The emphasis is independent judgment and originality in practical enterprise.",
  "The day pairs practical action with concern for a wider community.",
  "The account highlights the resolve to take charge and work toward independence.",
  "The emphasis is listening with unusual sensitivity and offering considered counsel.",
  "The day emphasizes finding artistic possibilities in ordinary work and home life.",
  "A preference for solid foundations sits alongside a talent for making things.",
  "The talent is ease with people and variety, especially where there is freedom to move.",
  "The account holds together a wish to belong and a persistent curiosity about what lies elsewhere.",
  "The day emphasizes concentration and the patience to investigate beyond appearances.",
  "Practical judgment involves seeing both the whole enterprise and the details that make it work.",
  "The emphasis is breadth of interests and learning across more than one field.",
  "Decoz uses this day to examine how independence can coexist with mutual reliance.",
  "The day emphasizes noticing emotions that others are reluctant to put into words.",
  "The talent concerns imagination expressed through conversation and creative work.",
  "The day associates vision with the ability to build something substantial with others.",
  "The emphasis is versatility in new circumstances and ease with a range of people.",
  "Care and responsibility are pronounced, with attention to the boundary between help and overinvolvement.",
  "The account emphasizes deep inquiry and a reluctance to accept first impressions as answers.",
  "The day places practical ambition beside the claims of affection and compassion.",
  "The emphasis is discovering a specialty through contact with varied people and experiences.",
  "The account singles out independent idealism and the value of encouragement for an unconventional aim.",
  "The day emphasizes lasting interest in questions of philosophy and spiritual meaning.",
  "The talent is artistic expression across forms such as writing, performance or visual work.",
  "The day describes reliable work as a foundation others can depend on.",
];

function entry(text: string, path: string, locator: string, exceptions: string[] = []) {
  return { text, url: site + path, locator, edition: "Hans Decoz · World Numerology", exceptions };
}

export const numberRules: Record<string, ReturnType<typeof entry>> = {
  ...Object.fromEntries(core.flatMap((value, index) => [
    [`decoz.life-path.${value}`, entry(lifePath[index], `numerology-life-path/life-path-number-${value}/`, `The Meaning of Life Path Number ${value}`)],
    [`decoz.soul-urge.${value}`, entry(soul[index], `numerology-soul-urge/meaning-of-soul-urge-${value}/`, `Soul Urge ${value} · numbered article`)],
    [`decoz.personality.${value}`, entry(personality[index], `numerology-personality/meaning-of-personality-number-${value}/`, `Personality ${value} · numbered article`)],
  ])),
  ...Object.fromEntries(birthdays.map((text, i) => [
    `decoz.birthday.${i + 1}`, entry(text, `numerology-birthday-numbers/birthday-number-${i + 1}/`, `Birthday number ${i + 1} · numbered article`, ["Uses the original day of the month. The reduced companion has no separate reading here."]),
  ])),
  ...Object.fromEntries(Object.entries(frozen.expression.meanings).map(([value, text]) => [
    `decoz.expression.${value}`, entry(text, "numerology-expression/", `The Meaning of Your Expression Numbers · ${value}`),
  ])),
  ...Object.fromEntries(Object.entries(frozen.year.meanings).map(([value, text]) => [
    `decoz.year.${value}`, entry(text, "personal-numerology-forecast/", `Meaning of Your Personal Year Cycles · ${value}`, ["Timeless symbolic topic only. The calendar year starts January 1."]),
  ])),
  "decoz.name-roles": entry("", "numerology-articles/numerology-core-numbers.html", "The Most Important Numbers In Your Chart"),
  "decoz.current-name": entry("", "pdf-sample-reports/ULT-sample-for-download.pdf", "Part V · How Your Current Name Affects You"),
  "decoz.birthday-role": entry("", "numerology-life-path/", "Your Life Path number, and its connection to other numbers in your chart"),
  "decoz.month-method": entry("", "free-forecasts/monthly-numerology-forecast.html", "Calculate Your Personal Monthly Cycles",
    ["The published forecasts also discuss the surrounding Personal Year. No standalone universal Month theme is assigned here."]),
  "decoz.day-method": entry("", "free-forecasts/daily-number-forecast/", "How to Calculate Your Personal Day Number, Step 4",
    ["The published forecasts also use the compound day, Personal Month and Daily Challenge. This reading presents the calculated value only."]),
};
