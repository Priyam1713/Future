# Block 20 · The connected Tarot reading

The `fate-waite-connected-v1` edition serves FATE’s existing one- and three-card draws. The native engine, deck, digital draw protocol, orientation stream, replay receipt, artwork and native export retain their existing versions.

## Native and consumer audit

The native Waite profile serves 78 cards, each with an upright and a reversed entry. It supports manual transcripts, deterministic seeded draws, explicit orientation policies, a single Focus, custom three-card labels and a Celtic layout. It carries per-card source text, editorial gloss, provenance, supplementary accounts, ambiguity flags and replay details. Its spread summary joins the per-card material. The previous consumer conclusion emphasized the last card, while the card details repeated general reflection prompts. FATE’s three positions were already What you carry, Where you stand and What to consider. These positions now determine how the passages open, develop and close. [Frozen Tarot core](../../knowledge/tarot_core_v1.json) · [Source registry](../../knowledge/tarot_sources.json) · [Native implementation](../../future/tarot.py)

Waite observes that sequence and placement can modify a card’s meaning and preserves discrepancies between his accounts. He supplies no interpretation for FATE’s three positions. His separate recurrence table gives accord for two Twos, security for three Twos, calm for two Threes and unity for three Threes in natural position. The consumer edition applies those four rows only when the entire three-card spread is upright and the indicated number of distinct numbered Minor Arcana cards matches. The individual card accounts remain visible alongside any rank entry. [Waite’s sequence qualification, p. 294](https://en.wikisource.org/wiki/Page:The_Pictorial_Key_to_the_Tarot.pdf/307) · [Waite’s recurrence table, p. 296](https://en.wikisource.org/wiki/Page:The_Pictorial_Key_to_the_Tarot.pdf/309)

## Coverage

| Status | Basis | Edition behavior |
| --- | --- | --- |
| Supported · direct | 156 card and orientation slots | Always preserves the approved source wording, rule and page for the drawn orientation. The card explorer includes an upright reference for reversed cards and exposes 56 separately archived additional accounts where available. |
| Supported · direct | Four rank recurrence entries | Displays the exact supported rank and count as a separate historical passage. |
| Supported · editorial | One-card Focus | Uses the drawn card’s actual motif or source alternatives as a single symbolic focus. |
| Supported · editorial | Opening, middle and closing | Compares the motifs in their positions and ties the closing to the opening and middle. An exact vocabulary groups clear motifs under accord, discord, movement, stillness, fruition, loss, inquiry and uncertainty. The comparison can show a recurring family and one of three bounded contrasts. |
| Supported · coverage limits | Competing or conditional card meanings | Retains alternatives and qualifications. Editorial family comparisons draw only on unambiguous entries. The source’s Two of Cups reversal fills the original gap, and Waite explicitly carries the Four of Wands meaning into reversal. |
| Experimental | Optional Gemini commentary | Remains a separately consented action. The deterministic reading and saved chapter are complete independently. |
| Deferred | Celtic consumer workflow and further historical rules | The ten dealt positions require a separate significator, crosswise placement, facing-sensitive positions five and six, a right-hand staff and a conditional follow-up. The native core verifies these conventions. A consumer workflow for those choices remains outside this edition. |
| Unsupported | General card-pair doctrines, predictive judgments and other traditions | The edition leaves combinations outside the four verified rank rows to editorial comparison or abstention. |

The historical upright and reversed references are preserved separately. Waite’s distinct Section 4 Two of Cups reversal fills a gap in the main reference. The original Four of Wands text explicitly carries the upright meaning into reversal. [Two of Cups, p. 290](https://en.wikisource.org/wiki/Page:The_Pictorial_Key_to_the_Tarot.pdf/303) · [Four of Wands, p. 190](https://en.wikisource.org/wiki/Page:The_Pictorial_Key_to_the_Tarot.pdf/203) · [Celtic position instructions, Part III §7](https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot/Part_3)

## Local chapters

My Fate stores the card IDs and orientations in position order, with the named roles, exact ordered passages, coverage categories and rule IDs in the schema-2 narrative. The existing local Codex reference resolves the original rules and exceptions. Validation checks the approved contents for the stored spread and edition. Schema-1 chapters retain their earlier view. Questions, draw seeds and Gemini commentary stay in the open visit. The separately labelled native download includes the full replay.

Future wording or rule revisions require a new interpretation edition. The existing edition must remain available to validate and reopen its chapters within the Codex’s 50-chapter and 65,536-character limits.

## Verification

The release evidence records automated coverage, the persistent Chrome restart and desktop/mobile visual checks. To reproduce the captures, run `node scripts/capture-connected-tarot.mjs` from `fate/web` against the production build served on port 8010, or set `FATE_CAPTURE_URL` for another local port. [Acceptance](block20-acceptance.json) · [Browser and screenshot evidence](block20-tarot-media.json)
