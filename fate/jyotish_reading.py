"""Bounded consumer interpretation over the frozen Parashari chart."""
from future.vedic import PROFILE, TABLES

EDITION = "P.V.R. Narasimha Rao, Vedic Astrology: An Integrated Approach (2000, author-hosted 2010 update)"
URL = "https://vedicastrologer.org/articles/vedic_astro_textbook.pdf"
VERSION = "fate-jyotish-v1"

HOUSE_TOPICS = (
    "embodied presence", "family resources and speech", "courage and communication",
    "home and a sense of peace", "learning and devotion", "service and opposition",
    "partnership", "inheritance and hidden knowledge", "teachers and principles",
    "work and action in society", "friendships and aspirations", "meditation and release",
)
GRAHA_TOPICS = {
    "Sun": "selfhood", "Moon": "the mind and emotional ease", "Mercury": "speech and learning",
    "Venus": "relating and companionship", "Mars": "courage", "Jupiter": "teachers and traditional learning",
    "Saturn": "service and loss", "Rahu": "hidden knowledge and journeys", "Ketu": "hidden knowledge and liberation",
}
SOURCES = {
    "vedic.houses": (19, "§1.3.3 p.7, counting from the rising sign"),
    "vedic.nakshatra": (22, "§1.3.6 pp.10–11, Table 2"),
    "vedic.dignity": (46, "§3.3 pp.34–35, Table 6"),
    "vedic.drishti": (112, "§10.2 pp.100–101, Example 34"),
    "vedic.d9": (67, "§6.2.9 p.55, Example 16; §6.3 Table 11 pp.60–61"),
    "vedic.vimshottari": (222, "§§16.2–16.3 pp.210–212, Table 38, Example 50"),
    "fate.jyotish.v1.houses": (80, "§7.2 pp.68–69, house topics"),
    "fate.jyotish.v1.lagna-lord": (83, "§7.3.5 pp.71–72, Lagna lord and Paaka Lagna"),
    "fate.jyotish.v1.grahas": (95, "§8.4 pp.83–84, Tables 15–16, natural significations"),
    "fate.jyotish.v1.period-context": (226, "§16.5.1 p.214, general principles"),
}


def reading(chart):
    if chart.get("profile") != PROFILE:
        return None
    planets = chart["planets"]
    navamsa = chart["d9"]["planets"]
    moon = chart["moon_nakshatra"]
    timing = chart["vimshottari"]
    lord = TABLES["rulers"][chart["ascendant"]["sign_index"]]

    def passage(title, text, rules, *inputs):
        return dict(title=title, text=text, rule_ids=rules, inputs=inputs, coverage="compositional")

    rising = passage("The house of the Lagna lord",
        f'{lord} rules {chart["ascendant"]["sign"]} Lagna and occupies house {planets[lord]["house"]}. '
        f'Rao treats the ruler as another reference for the self. Here its placement brings {HOUSE_TOPICS[planets[lord]["house"]-1]} into that inquiry.',
        ["vedic.houses", "fate.jyotish.v1.lagna-lord", "fate.jyotish.v1.houses"], "ascendant.sign_index", f"planets.{lord}.house")
    lunar = passage("The Moon as a reference",
        f'The Moon is in {planets["Moon"]["sign"]}, in the {moon["name"]} mansion, pada {moon["pada"]}. '
        f'Rao uses the Moon as a reference for the mind. {moon["lord"]} rules this mansion and starts the birth-period sequence.',
        ["vedic.nakshatra", "fate.jyotish.v1.grahas", "vedic.vimshottari"], "planets.Moon.sign", "moon_nakshatra")

    grahas = {}
    for name, p in planets.items():
        d9 = navamsa[name]
        contacts = [dict(index=i, **row) for i, row in enumerate(chart["graha_aspects"])
                    if row["from"] == name or name in row["targets"]]
        cross = f'{name} occupies {p["sign"]} in Rashi and {d9["sign"]} in Navamsa.'
        if d9["same_rashi_as_d1"]:
            cross = f'{name} holds {p["sign"]} in both charts, across two distinct house frames.'
        if ("exaltation_sign" in p["dignity"]["flags"] and "debilitation_sign" in d9["sign_dignities"]
                or "debilitation_sign" in p["dignity"]["flags"] and "exaltation_sign" in d9["sign_dignities"]):
            cross += " The two frames give different dignity indications, so each is read in its own context."
        grahas[name] = dict(
            topic=GRAHA_TOPICS[name], house_topic=HOUSE_TOPICS[p["house"] - 1],
            d1=dict(dignities=p["dignity"]["flags"], moolatrikona=p["dignity"]["moolatrikona"],
                    rules_houses=p["rules_houses"], ruler=p["sign_ruler"]),
            d9=dict(dignities=d9["sign_dignities"], ruler=d9["sign_ruler"]),
            nodal=name in ("Rahu", "Ketu"), contacts=contacts,
            comparison=passage("Across the two charts", cross, ["vedic.d9", "vedic.dignity"],
                               f"planets.{name}", f"d9.planets.{name}"),
        )
    active = timing["current"]
    main, sub = active["mahadasa"]["lord"], active["antardasha"]["lord"]
    period = passage("Read the lords where they sit",
        f'{main} sets the main period and {sub} the subdivision at the selected instant. '
        f'Rao brings the active lords’ natal placements into the reading. '
        + (f'Here both periods return to house {planets[main]["house"]}, with its emphasis on {HOUSE_TOPICS[planets[main]["house"]-1]}.'
           if planets[main]["house"] == planets[sub]["house"]
           else f'The two lords point to different house topics: {grahas[main]["house_topic"]}, and {grahas[sub]["house_topic"]}.'),
        ["fate.jyotish.v1.period-context", "vedic.vimshottari", "fate.jyotish.v1.houses"],
        "vimshottari.current", f"planets.{main}.house", f"planets.{sub}.house")
    return dict(profile=VERSION, lagna_lord=lord, chapters=[rising, lunar, period], grahas=grahas,
                timing=dict(target=timing["target_utc"], year_days=timing["year_days"],
                            main=[active["mahadasa"], *timing["upcoming"]["mahadasas"]],
                            sub=timing["current_md_antardashas"], upcoming=timing["upcoming"]["antardashas"]),
                sources={key: dict(locator=loc, url=f"{URL}#page={page}", edition=EDITION)
                         for key, (page, loc) in SOURCES.items()})
