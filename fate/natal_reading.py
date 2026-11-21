"""Versioned, deterministic editorial reading over a verified Western natal result."""
from itertools import combinations

from future.natal import placement
from future.western import traditional_configuration_context
from .natal_rules import ANGLES, ASCENDANT, ASPECTS, CHART_RULER, HOUSES, MODERN, RULERSHIP, SIGNS

PROFILE = "fate-western-natal-v1"


def aspect_id(aspect):
    return f"aspect:{'-'.join(aspect['bodies'])}:{int(aspect['angle'])}"


def summarize(chart):
    reading = dict(profile=PROFILE, tradition=MODERN, chapters=[], focuses={}, sources={}, patterns=[])
    settings = chart["settings"]
    if settings["tradition"] != MODERN or settings["zodiac"] != "tropical" or settings["application"] != "natal":
        return reading

    planets = chart["planets"]
    asc = placement(chart["angles"]["ascendant"])["sign"]
    aspects = {}
    for aspect in chart["aspects"]:
        bodies = tuple(aspect["bodies"])
        angle = aspect["angle"]
        rule = ASPECTS.get((*bodies, angle)) or ASPECTS.get((*reversed(bodies), angle))
        aspects[frozenset(bodies), angle] = (aspect, rule)
    used = set()

    def passage(rule):
        reading["sources"][rule.id] = rule.reference()
        return dict(title=rule.title, body=rule.body, coverage="direct", rule_ids=[rule.id])

    def editorial(title, body, *rules):
        for rule in rules:
            reading["sources"][rule.id] = rule.reference()
        return dict(title=title, body=body, coverage="editorial", rule_ids=[r.id for r in rules])

    def chapter(key, heading, blocks):
        if blocks:
            reading["chapters"].append(dict(id=key, title=heading, passages=blocks))

    def pair(a, b, angle):
        return aspects.get((frozenset((a, b)), angle), (None, None))[1]

    def planet_rules(body):
        p = planets.get(body)
        if not p:
            return ()
        return tuple(r for r in (SIGNS.get((body, p["sign"])), HOUSES.get((body, p["house"]))) if r)

    def blocks(*rules, mark=True):
        if mark:
            used.update(r.id for r in rules if r)
        return [passage(r) for r in rules if r]

    ruler = traditional_configuration_context(chart)["house_rulers"][0]
    if ruler["cusp_sign"] == asc and settings["rulership"] == "traditional":
        name = ruler["ruler"]
        p = planets[name]
        reading["chart_ruler"] = dict(body=name, sign=p["sign"], house=p["house"],
                                      rule_ids=[RULERSHIP.id, CHART_RULER.id])
        for rule in (RULERSHIP, CHART_RULER):
            reading["sources"][rule.id] = rule.reference()

    def move_to_work(body):
        p = planets.get(body)
        return p and p["house"] in (6, 10)

    sun = planet_rules("Sun")
    moon = planet_rules("Moon")
    mercury = planet_rules("Mercury")
    sun_house = HOUSES.get(("Sun", planets["Sun"]["house"])) if "Sun" in planets else None
    mercury_house = HOUSES.get(("Mercury", planets["Mercury"]["house"])) if "Mercury" in planets else None

    identity = []
    if (sun_sign := SIGNS.get(("Sun", "Cancer"))) in sun and sun_house == HOUSES["Sun", 9]:
        identity.append(editorial("Roots and horizons",
            "The Cancer Sun puts care and a sense of belonging at the heart of its symbolism. In the ninth house, the same Sun is read through study, travel and other ways of widening one’s view. Read side by side, the passages leave room for keeping close ties while looking beyond what is familiar.",
            sun_sign, sun_house))
    else:
        identity.extend(blocks(*(r for r in sun if not (r == sun_house and move_to_work("Sun")))))
    identity.extend(blocks(ASCENDANT.get(asc)))
    chapter("identity", "Purpose and presence", identity)
    emotion = blocks(*moon)
    venus = pair("Moon", "Venus", 60) or pair("Moon", "Venus", 120)
    guarded = pair("Moon", "Saturn", 90) or pair("Moon", "Saturn", 180)
    if venus and guarded:
        emotion.append(editorial("Warmth and reserve",
            "The chart gives closeness two different settings. Moon–Venus describes the ease of meeting another person with sympathy. Moon–Saturn makes room for caution about receiving that same care. The two can be read side by side.", venus, guarded))
        used.update((venus.id, guarded.id))
    else:
        emotion.extend(blocks(venus, guarded))
    chapter("emotion", "Feeling and closeness", emotion)

    mercury_aspects = [
        rule for aspect, rule in aspects.values()
        if rule and "Mercury" in aspect["bodies"]
    ]
    chapter("communication", "The way ideas take shape",
            blocks(*(r for r in mercury if not (r == mercury_house and move_to_work("Mercury"))), *mercury_aspects))

    saturn = next((rule for angle in ANGLES if (rule := pair("Sun", "Saturn", angle))), None)
    chapter("work", "Work and direction",
            blocks(sun_house if move_to_work("Sun") else None,
                   mercury_house if move_to_work("Mercury") else None, saturn))

    themes = []
    jupiter = pair("Sun", "Jupiter", 0)
    if jupiter and saturn:
        themes.append(editorial("Room to grow, room for limits",
            "The Sun meets Jupiter’s appetite for possibility and Saturn’s concern with what can be sustained. Heese explicitly qualifies the Jupiter reading when Saturn is involved. Read together, these contacts give a place to both the scale of a goal and the care it takes to carry it.", jupiter, saturn))
        used.update((jupiter.id, saturn.id))
    themes.extend(blocks(*(pair("Sun", "Moon", angle) for angle in ANGLES)))
    chapter("themes", "Themes in conversation", themes)

    direct = [rule for _, rule in aspects.values() if rule and rule.id not in used]
    chapter("aspects", "Other connections in the sky", blocks(*direct))

    for name, p in planets.items():
        related = [aspect_id(a) for a, rule in aspects.values() if rule and name in a["bodies"]]
        reading["focuses"][name] = dict(passages=blocks(*planet_rules(name), mark=False), connections=related)
    reading["focuses"]["Ascendant"] = dict(passages=blocks(ASCENDANT.get(asc), mark=False), connections=[])
    for house in range(1, 13):
        occupants = [name for name, p in planets.items() if p["house"] == house]
        house_parts = [rule for name in occupants if (rule := HOUSES.get((name, house)))]
        reading["focuses"][f"house:{house}"] = dict(passages=blocks(*house_parts, mark=False), connections=[])
    for aspect, rule in aspects.values():
        neighbors = [aspect_id(other) for other, other_rule in aspects.values()
                     if other_rule and other is not aspect and set(aspect["bodies"]).intersection(other["bodies"])]
        reading["focuses"][aspect_id(aspect)] = dict(passages=blocks(rule, mark=False), connections=neighbors[:3])

    # Report the native edges only. No pattern personality or dominance score.
    for (ends, angle), (opposition, _) in aspects.items():
        if angle != 180:
            continue
        for apex in planets.keys() - ends:
            squares = [aspects.get((frozenset((end, apex)), 90)) for end in opposition["bodies"]]
            if all(squares):
                reading["patterns"].append(dict(kind="T-square", apex=apex,
                    contacts=[aspect_id(opposition), *(aspect_id(a) for a, _ in squares)]))
    reading["patterns"].sort(key=lambda p: (p["apex"], p["contacts"]))
    return reading
