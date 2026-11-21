"""Consumer palm reading composition over confirmed observations."""
from typing import Literal
from pydantic import BaseModel, ConfigDict
from future import palmistry


class PalmInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    confirmed: bool
    hand: dict
    fingertips: Literal["conic", "unknown"] = "unknown"
    mount_lean: Literal["saturn_jupiter", "saturn_sun", "sun_mercury", "unknown"] = "unknown"


THEMES = {
    "practical": ("Practical judgment", "Cheiro returns to the idea of working with what can be seen and tested."),
    "imaginative": ("Imagination", "These formations bring imagination into the foreground of Cheiro’s account."),
    "steady": ("Steadiness", "The source emphasizes continuity and steadiness in these formations."),
    "changeable": ("Change and variation", "These formations carry a theme of variation rather than one settled pattern."),
    "warm": ("Warmth", "The source uses warmth as a theme for these formations."),
    "reserved": ("Reserve", "These formations carry a quieter, more reserved tone in the source."),
    "active": ("Action", "The source emphasizes movement from an idea into action."),
    "reflective": ("Reflection", "The source gives more room to deliberation and reflection."),
    "affection": ("Affection", "These formations belong to the source’s symbolic language of affection."),
    "ambitious": ("Aspiration", "Cheiro uses aspiration and directed effort as the theme of this formation."),
    "versatile": ("Versatility", "Cheiro’s mixed outline lends this part of the account a sense of variety."),
    "passionate": ("Intensity", "The source gives intensity a place in its account of this heart-line formation."),
    "disappointment": ("Disappointment", "The source uses disappointment as a symbolic theme for this line."),
    "cautious": ("Caution", "Cheiro associates this start with care before taking action."),
    "impulsive": ("Spontaneity", "Cheiro gives spontaneous action a place in this reading of the starting gap."),
}

FIGURES = {
    ("head_life_gap", "joined"): "the joined start of the head and life lines",
    ("head_life_gap", "medium"): "the separation at the start of the head and life lines",
    ("head_life_gap", "wide"): "the wide separation at the start of the head and life lines",
    ("lines.head.curvature", "straight"): "the straight head line",
    ("lines.head.curvature", "slight_slope"): "the gentle slope of the head line",
    ("lines.head.curvature", "very_sloping"): "the steep slope of the head line",
    ("lines.head.curvature", "straight_then_sloping"): "the head line’s straight start and sloping finish",
    ("lines.heart.origin", "jupiter"): "the heart line below your index finger",
    ("lines.heart.origin", "between_jupiter_saturn"): "the heart line between your index and middle fingers",
    ("lines.heart.origin", "saturn"): "the heart line below your middle finger",
    ("lines.life.branch_to", "jupiter"): "the life-line branch toward the index finger",
}

COMBINATIONS = {
    "square_conic": ("Study and inspiration",
        "Cheiro links the square outline with sustained study and the conic fingertips with inspiration. Read together, the pair makes room for creative work built on practice.", "p. 30, scan page 56"),
    "saturn_jupiter": ("Aspiration tempered by prudence",
        "Cheiro reads the Saturn area inclining toward Jupiter as a blend in which prudence tempers the Jupiter theme.", "p. 65, scan page 113"),
    "saturn_sun": ("Art and serious reflection",
        "Cheiro combines Saturn’s serious or solemn tone with the artistic emphasis of the Sun area.", "p. 65, scan page 113"),
    "sun_mercury": ("Imagination applied",
        "Cheiro brings the Sun area’s artistic emphasis into the Mercury area’s practical or scientific pursuits.", "p. 65, scan page 113"),
}

HEART_CHAPTERS = {
    "steady": ("Steady affection", "Cheiro reads this part of the heart line through the theme of lasting affection."),
    "changeable": ("Affection and change", "In Cheiro’s account, this formation gives affection a more changeable course."),
    "passionate": ("Intensity of feeling", "Cheiro describes this start of the heart line in terms of intensity."),
    "warm": ("Warmth in affection", "Cheiro treats this formation as a sign of warmth in his account of affection."),
    "reserved": ("Reserve in affection", "Cheiro’s account gives reserve a place alongside affection here."),
    "disappointment": ("Affection and interruption", "Cheiro uses disappointment as a symbolic theme for the interruption you described."),
}


def compose(hand):
    matched = hand["readings"]
    observations = {}
    for trace in hand["rule_trace"]:
        if trace["status"] != "matched":
            continue
        keys = [(c["path"], c["observed"]) for c in trace["conditions"]]
        descriptions = [FIGURES[key] for key in keys if key in FIGURES]
        if not descriptions:
            descriptions = [f"the {value} outline" for path, value in keys if path == "shape.type"]
        observations[trace["rule_id"]] = descriptions
    groups = {}
    for rule in matched:
        for theme in rule["tags"]:
            if theme in THEMES:
                groups.setdefault(theme, []).append(rule["id"])
    by_rule_set = {}
    for theme, ids in groups.items():
        by_rule_set.setdefault(tuple(ids), []).append(theme)
    chapters = []
    for ids, themes in by_rule_set.items():
        figures = list(dict.fromkeys(text for id_ in ids for text in observations[id_]))
        if "affection" in themes and len(themes) == 2:
            other = next(t for t in themes if t != "affection")
            title, body = HEART_CHAPTERS.get(other, THEMES[other])
        else:
            title = " and ".join(THEMES[t][0].lower() for t in themes).capitalize()
            body = " ".join(THEMES[t][1] for t in themes)
        figure = figures[0] if len(figures) == 1 else None
        if figure and themes == ["imaginative"]:
            body = f"In this tradition, {figure} gives the reading an imaginative thread."
        elif figure and "heart line" in figure and set(themes) == {"steady", "affection"}:
            body = f"Cheiro associates {figure} with lasting affection."
        elif figures:
            body = f"{body} You noted {' and '.join(figures)}."
        chapters.append(dict(title=title, body=body, rule_ids=list(ids)))
    connections = [
        dict(body=f"{THEMES[a][0]} and {THEMES[b][0].lower()} suggest different emphases in the historical reading. The observations leave room for both.",
             rule_ids=row["rule_ids"])
        for row in hand["interpretive_tensions"]
        for a, b in [row["topics"]]
        if a in THEMES and b in THEMES
    ]
    return dict(
        title="Patterns in the hand" if matched else "A reading needs clearer observations",
        chapters=chapters, connections=connections,
        matched_sections=list(dict.fromkeys(row["section"] for row in matched)),
        abstained=not matched,
    )


def read(request):
    if not request.confirmed:
        raise ValueError("Confirm the observations you can see before opening the reading.")
    native = palmistry.read(dict(schema_version=1, profile=palmistry.PROFILE,
                                 hands=[request.hand]))
    narrative = compose(native["hands"][0])
    keys = []
    if request.fingertips == "conic" and request.hand.get("shape", {}).get("type") == "square":
        keys.append("square_conic")
    if request.mount_lean != "unknown":
        keys.append(request.mount_lean)
    supplement = []
    for key in keys:
        title, body, locator = COMBINATIONS[key]
        rule_id = f"fate.cheiro.supplement.v1.{key}"
        supplement.append(dict(id=rule_id, text=body, locator=locator, exceptions=[
            "Requires the exact declared combination. An unclear or reversed relationship is left open."
        ]))
        narrative["chapters"].append(dict(title=title,body=body,rule_ids=[rule_id]))
    if supplement:
        narrative.update(title="Patterns in the hand", abstained=False)
    return dict(native=native, narrative=narrative, supplement=supplement)
