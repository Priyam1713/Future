"""First-party natal interpretations, separately versioned from the native rules."""
from dataclasses import dataclass

MODERN = "modern psychological"
EDITION = "Café Astrology, author-published natal articles, checked 2026-11-21"
SITE = "https://cafeastrology.com/"


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    body: str
    path: str
    locator: str
    exceptions: tuple[str, ...] = ()
    author: str = "Annie Heese / Café Astrology"
    edition: str = EDITION
    tradition: str = MODERN

    def reference(self):
        return dict(id=self.id, title=self.title, text=self.body, url=self.path if self.path.startswith("https://") else SITE + self.path,
                    locator=self.locator, author=self.author, edition=self.edition, exceptions=self.exceptions,
                    tradition=self.tradition, version=1)


def house_rules(body, path, passages):
    rules = {}
    for house, (title, text) in enumerate(passages, 1):
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(house, "th")
        heading = f"{body} in the {house}{suffix} House"
        link = path + ("#" + heading.lower().replace(" ", "-") if body == "Sun" else "")
        rules[body, house] = Rule(f"fate.natal.v1.house.{body.lower()}.{house}", title, text, link, heading,
                                  ("Uses the selected house system. Proximity to an angle is not inferred from house membership.",))
    return rules


HOUSES = {
    **house_rules("Sun", "natal-chart-interpretations-houses.html", (
        ("Making an impression", "Identity comes into focus through the way one meets the world and is seen."),
        ("What is worth keeping", "The Sun here links pride with lasting commitments, resources and a sense of worth."),
        ("Learning out loud", "The source reads curiosity and sharing what one knows as expressions of identity."),
        ("A private center", "Home, family and a private life give the Sun a place to put down roots."),
        ("Space to create", "The emphasis is on taking pleasure in an unmistakably personal form of expression."),
        ("Purpose in the everyday", "Daily work and being useful give purpose a concrete form in this reading."),
        ("Identity in partnership", "Negotiation and making room for another person become ways to explore identity."),
        ("Beneath the surface", "The symbolism joins purpose to sustained inquiry into what is usually left unexplored."),
        ("A wider horizon", "Purpose takes the form of inquiry here. Study, travel and the exchange of ideas are ways of looking beyond familiar ground."),
        ("A direction to work toward", "The Sun links identity with responsibility and the wish to work toward a visible goal."),
        ("A place in the wider circle", "Friendships and shared aspirations place identity in a wider social world."),
        ("An inward source of purpose", "Solitude and time away from public demands are settings for an inward kind of purpose."),
    )),
    **house_rules("Moon", "natal-chart-interpretations-houses.html/2", (
        ("Feeling close to the surface", "The source makes feeling part of the immediate response to a new situation."),
        ("The reassurance of resources", "Material steadiness and emotional reassurance are closely connected in this house reading."),
        ("Putting feeling into words", "The source connects emotional response with conversation and the urge to understand what has happened."),
        ("What it means to belong", "The Moon here gives belonging and a place to call home particular emotional weight."),
        ("Sharing what moves us", "Affection and creative expression are ways of giving feeling a visible form."),
        ("The comfort of a useful rhythm", "The Moon here finds reassurance in useful work and an everyday rhythm with enough room to breathe."),
        ("Connection as reassurance", "The emphasis falls on emotional support within one-to-one relationships."),
        ("Trust and deep attachment", "This position brings the need for security into the same setting as a desire for deeper attachment."),
        ("A change of perspective", "The source finds emotional refreshment in encountering ideas and places outside the usual routine."),
        ("Being recognized", "The Moon here associates emotional reassurance with recognition and a role with clear responsibilities."),
        ("Belonging among friends", "The source gives friendships and communities a place in the search for mutual support."),
        ("Time to feel in private", "Solitude gives feelings time to register and settle in this reading."),
    )),
    **house_rules("Mercury", "natal/mercuryinhouses.html", (
        ("Curiosity at first contact", "Curiosity and quick adaptation are the source’s main themes for meeting unfamiliar situations."),
        ("Ideas with practical use", "The emphasis is on working conclusions through at one’s own pace and seeing what can be used."),
        ("The exchange of ideas", "Words, reading and conversation give wide-ranging curiosity somewhere to go."),
        ("Ideas close to home", "The source connects an active imagination with the familiar setting of home."),
        ("The play of language", "Words and wit are treated as material for creative expression."),
        ("Attention to the details", "The account emphasizes sorting, organizing and seeing the details needed to make work fit together."),
        ("Thinking in dialogue", "Conversation and opposing viewpoints are ways to hear an idea more clearly."),
        ("Looking for motives", "Mercury here turns curiosity toward hidden reasons and strategic questions."),
        ("Learning beyond the familiar", "The source links an appetite for learning with exchanging ideas about how the world works."),
        ("A voice in public work", "Mercury gives language a public role here. Explaining, negotiating or making a case are part of the work."),
        ("Thinking with the group", "The source places curiosity amid teams, communities and people with new ideas."),
        ("Keeping a thought in reserve", "The emphasis is on thinking privately and choosing carefully when to give a thought a voice."),
    )),
}

ASCENDANT = {
    sign: Rule(f"fate.natal.v1.asc.{sign.lower()}", "Meeting the world", body,
               f"natal-chart-interpretations.html#{sign.lower()}-ascendant", f"{sign} Ascendant",
               ("Reads the calculated rising sign. Birth-time uncertainty can change the result.",))
    for sign, body in {
        "Aries": "Aries rising gives the first encounter an emphasis on directness and the willingness to begin.",
        "Taurus": "With Taurus rising, the source emphasizes taking time to find one’s footing before embracing change.",
        "Gemini": "Gemini rising brings a quick, curious manner to the first encounter with something unfamiliar.",
        "Cancer": "Cancer rising describes a responsive first impression, with openness shaped by how safe the situation feels.",
        "Leo": "Leo rising emphasizes a visible presence and awareness of how one comes across.",
        "Virgo": "Virgo rising brings attention to the details of a situation before settling into it.",
        "Libra": "Libra rising emphasizes a diplomatic approach and sensitivity to the balance between people.",
        "Scorpio": "Scorpio rising gives the first encounter a tone of watchfulness and reserve, even when the presence itself is strongly felt.",
        "Sagittarius": "Sagittarius rising meets what is unfamiliar with enthusiasm and an eye for what lies beyond it.",
        "Capricorn": "Capricorn rising emphasizes an appearance of competence and care in how one is received.",
        "Aquarius": "Aquarius rising brings an independent manner and interest in people from different walks of life.",
        "Pisces": "Pisces rising emphasizes receptiveness and an imaginative way of meeting a new situation.",
    }.items()
}

SIGNS = {}
for body, sign, page, title, text in (
    ("Sun", "Cancer", "suninsigns.html", "A sense of belonging", "Cancer gives the Sun a language of care and attachment. The source places value on familiar people and places, and the security they can offer."),
    ("Sun", "Taurus", "suninsigns.html", "The steadiness of the familiar", "With the Sun in Taurus, the emphasis is on continuity, tangible comforts and a patient response to change."),
    ("Sun", "Capricorn", "suninsigns_page2.html", "Making something worthwhile", "Capricorn gives the Sun a practical measure of purpose. Being useful and contributing to something durable are central images."),
    ("Moon", "Aries", "mooninsigns.html", "A feeling that wants to move", "With the Moon in Aries, feeling is described as quick to arrive and inclined toward immediate action."),
    ("Moon", "Scorpio", "mooninsigns_pg2.html", "The depth of feeling", "The source reads the Scorpio Moon through emotional intensity and the search for depth underneath surface impressions."),
    ("Mercury", "Aries", "mercuryinsigns.html", "Straight to the point", "Mercury in Aries represents a direct, quick-moving voice with little patience for circling an idea."),
    ("Mercury", "Leo", "mercuryinsigns.html", "A voice with presence", "Mercury in Leo gives ideas an expressive delivery. The source emphasizes making an impression and holding a listener’s attention."),
    ("Mercury", "Capricorn", "mercuryinsigns_page2.html", "Thinking in workable steps", "Mercury in Capricorn gives thought a deliberate pace, with an emphasis on structure and practical conclusions."),
):
    SIGNS[body, sign] = Rule(f"fate.natal.v1.sign.{body.lower()}.{sign.lower()}", title, text,
                            f"articles/{page}", f"{body} in {sign}")

ANGLES = {0: "conjunct", 60: "sextile", 90: "square", 120: "trine", 180: "opposition"}
ASPECTS = {}


def aspects(first, second, texts, path="natal-chart-interpretations-aspects.html", locators=None, exceptions=None):
    for angle, (title, text) in texts.items():
        heading = f"{first} {ANGLES[angle]} {second}"
        anchor = "#" + heading.lower().replace(" ", "-") if path == "natal-chart-interpretations-aspects.html" else ""
        ASPECTS[first, second, angle] = Rule(f"fate.natal.v1.aspect.{first.lower()}.{second.lower()}.{angle}",
                                             title, text, path + anchor, (locators or {}).get(angle, heading),
                                             (exceptions or {}).get(angle, ()))


aspects("Sun", "Moon", {
    0: ("Purpose and need pull together", "The Sun and Moon meet in one direction. The source sees focus in that alignment, with less distance between what feels necessary and what seems worth pursuing."),
    60: ("Making room for both", "Purpose and emotional needs can find common ground here. The source also considers whether keeping the peace can leave a conflict unspoken."),
    90: ("Purpose and need pull differently", "The Sun’s direction and the Moon’s immediate needs can ask for different things. Heese reads the square as a tension that calls for both voices to be heard."),
    120: ("An easy conversation between purpose and feeling", "The trine is read as ease between aims and emotional needs. That ease can be a resource, with the possibility of taking harmony for granted."),
    180: ("Two ends of the same question", "The opposition gives purpose and emotional needs distinct voices. The symbolic work is to make room for two perspectives that can each feel compelling."),
}, exceptions={0: ("A conjunction can span two signs. No same-sign emphasis or lunation phase is inferred.",)})
aspects("Sun", "Mercury", {
    0: ("Thought close to purpose", "Heese reads the conjunction as an active link between thought and intention. Expressing an idea can feel closely bound up with expressing a point of view."),
})
aspects("Sun", "Jupiter", {
    0: ("Looking for what could grow", "The conjunction brings breadth and enthusiasm into the question of purpose. In the source account that optimism can also run ahead of what can be delivered."),
    60: ("Making room for possibility", "The account draws out generosity of outlook and willingness to share what one has learned."),
    90: ("When possibility outruns capacity", "The square brings broad hopes into contact with the practical limits of what can be taken on."),
    120: ("A wider view", "The trine emphasizes broad interests and the pleasure of learning from new experiences."),
}, exceptions={0: ("The author explicitly qualifies the optimistic emphasis when Saturn is involved. No luck, rewards or outcomes are inferred.",)})
aspects("Sun", "Saturn", {
    0: ("Purpose takes responsibility seriously", "The conjunction brings order and accountability close to the way purpose is formulated."),
    60: ("Giving purpose a plan", "The sextile emphasizes taking responsibility and turning a goal into an orderly plan."),
    90: ("The weight of expectation", "Heese reads this square through the pressure of demands and the need to distinguish responsibility from overburden."),
    120: ("A sustainable pace", "The trine links purpose with realistic goals, measured effort and keeping commitments."),
    180: ("Ambition meets a limit", "The opposition brings a wish to act or be seen into contact with restraint. A sense of duty can give ambition structure and can also press too hard."),
})
aspects("Moon", "Venus", {
    60: ("A way back toward connection", "Heese links this sextile with sympathy and the ability to ease strain between people when called upon."),
    120: ("Affection with an easy rhythm", "The trine emphasizes an easy, sympathetic approach to intimacy and restoring harmony."),
}, "natal/moonvenusaspects.html", {60: "Moon sextile or trine Venus", 120: "Moon sextile or trine Venus"})
aspects("Moon", "Saturn", {
    90: ("Caution around closeness", "The Moon–Saturn square is read as emotional reserve. The source makes trust and the willingness to receive care part of the question."),
    180: ("Taking time to trust", "The Moon–Saturn opposition brings a guarded response into the symbolism of closeness and emotional support."),
}, "natal/moonsaturnaspects.html", {90: "Moon square or opposition Saturn", 180: "Moon square or opposition Saturn"})
aspects("Moon", "Mars", {
    0: ("Feeling close to action", "The conjunction links emotional immediacy with initiative. In Heese’s account, that can give feeling a direct, protective expression."),
}, "natal/moonmarsaspects.html")
aspects("Mercury", "Mars", {
    60: ("Ideas with momentum", "Heese pairs decisiveness with the ability to make a point and put an idea in motion."),
    90: ("Conviction in conversation", "The square links mental energy with the speed of a reply. The source distinguishes the courage to make a case from the impulse to turn every exchange into a debate."),
    180: ("A lively exchange", "The opposition puts quick perceptions into the give-and-take of debate, where conviction leaves room for the other voice."),
}, "natal/mercurymarsaspects.html",
    {60: "Mercury sextile or trine Mars", 90: "Mercury square or opposition Mars", 180: "Mercury square or opposition Mars"})

RULERSHIP = Rule("fate.natal.v1.method.ruler", "Traditional sign ruler",
                 "The traditional scheme assigns the rising sign to one of the seven classical planets.",
                 "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/1B*.html#17",
                 "Tetrabiblos I.17, Of the Houses of the Several Planets, Loeb pp. 79–83",
                 ("Domicile convention only. No traditional judgment or modern outer-planet co-ruler is inferred.",),
                 "Claudius Ptolemy / F. E. Robbins", "Loeb Classical Library, 1940", "traditional domicile convention")
CHART_RULER = Rule("fate.natal.v1.method.chart-ruler", "Ruler of the rising sign",
                   "The ruler of the rising sign is used as a link to that planet’s placement.",
                   "articles/sign-rulerships.html", "Planetary Rulers of the Zodiac Signs, paragraph beginning 'When interpreting a birth chart'",
                   ("The app follows the classical rulership column and makes no unsupported ruler-specific synthesis.",))
