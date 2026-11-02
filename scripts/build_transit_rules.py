"""Manually reviewed, short research paraphrases of identified transit passages."""
import json
from pathlib import Path
rules=[]
def add(body,target,angles,text,url,locator,author,exceptions=(),conditions=None):
    rules.append(dict(id=f'{author.split()[0].lower()}.{body}.{target}.{"-".join(map(str,angles))}',version=1,technique_id=1,
            tradition='modern psychological',kind='transit',key=f'{body}:{target}:{angles}',transiting=body,
            natal_target=target,aspects=angles,conditions=conditions or {},text=text,url=url,locator=locator,
            author=author,edition='Online practitioner article, checked 2026-11-02',status='source_checked',
            rights='Original concise paraphrase of ideas; no book or page ingestion',
            exceptions=list(exceptions),documentation_scope='general pair, all major aspects' if author=='Robert Hand' else 'aspect-specific planet-pair delineation'))
inner='https://cafeastrology.com/innerplanettransits.html'
# The page is a compiled practitioner resource; do not attribute it to Hand.
for target,angles,text,heading in [
 ('Mercury',[90],'Mental intensity and pressure to decide; avoid treating urgency as clarity.','Square Mercury'),
 ('Mercury',[0],'Fluent ideas and communication.','Conjunct Mercury'),
 ('Mercury',[180],'Difficulty conveying intentions or finding agreement.','Opposition Mercury'),
 ('Mercury',[60,120],'Clearer thought and flowing conversation.','Sextile or Trine Mercury'),
 ('Pluto',[0],'Probing insight, research and analysis.','Conjunct Pluto'),
 ('Pluto',[90],'Suspicion and intrusive preoccupations are symbolic concerns.','Square Pluto'),
 ('Saturn',[0],'Serious deliberation and reorganizing responsibilities.','Conjunct Saturn'),
 ('Saturn',[60,120],'Mental discipline and attention to practical details.','Sextile or Trine Saturn'),
 ('Sun',[90],'Unclear thought and potential friction with authority.','Square Sun')]:
    add('Mercury',target,angles,text,inner,'Mercury Transits '+heading,'Cafe Astrology editorial compilation',
        ['Short transit symbolism; not a diagnosis or an instruction to postpone necessary decisions.'])
saturn='https://cafeastrology.com/saturntransitaspects.html'
for body,target,angles,text,heading in [
 ('Mercury','Uranus',[60,120],'Original ideas and inventive communication.','Mercury Transits Sextile or Trine Uranus'),
 ('Mercury','Neptune',[60,120],'Imaginative thinking and creative expression.','Mercury Transits Sextile or Trine Neptune'),
 ('Venus','Venus',[60,120],'Appreciation of beauty and existing pleasures.','Venus Transits Sextile or Trine Venus'),
 ('Moon','Moon',[60,120],'Reflection and clearer emotional understanding.','Moon Transits Sextile or Trine Moon'),
 ('Moon','Venus',[60,120],'Kindness and appreciation of familiar surroundings.','Moon Transits Sextile or Trine Venus'),
 ('Moon','Mars',[60,120],'Sympathy and appreciation for effective action.','Moon Transits Sextile or Trine Mars'),
 ('Sun','Mercury',[60,120],'Easier dialogue and self-expression.','Sun Transits Sextile or Trine Mercury'),
 ('Sun','Saturn',[0],'Attention to postponed duties.','Sun Transits Conjunct Saturn'),
 ('Sun','Saturn',[60,120],'Practical organization and disciplined effort.','Sun Transits Sextile or Trine Saturn')]:
    add(body,target,angles,text,inner,heading,'Cafe Astrology editorial compilation',
        ['Source symbolism, not an empirically calibrated outcome.'])
for target,angles,text,heading in [
 ('Sun',[0],'Reassess goals, maturity and responsibilities against present realities.','Conjunctions: Sun'),
 ('Sun',[90,180],'Challenges to confidence or authority invite patient restructuring.','Squares & Oppositions: Sun'),
 ('Sun',[60,120],'Practical realism and steadier self-assurance.','Trines & Sextiles: Sun'),
 ('Moon',[0],'Examine support systems and emotional habits.','Conjunctions: Moon'),
 ('Moon',[90,180],'Perceived isolation and domestic burdens call for reflection.','Squares & Oppositions: Moon'),
 ('Mercury',[60,120],'Organize thinking, deepen study and improve skills.','Trines & Sextiles: Mercury'),
 ('Venus',[60,120],'A practical tone in relationships, creative work and finances.','Trines & Sextiles: Venus'),
 ('Mars',[60,120],'Pace effort and build long-term work methodically.','Trines & Sextiles: Mars'),
 ('Jupiter',[0,90,180],'Reorganize priorities and temper expansion with realistic limits.','Saturn Transits to Natal Jupiter')]:
    add('Saturn',target,angles,text,saturn,heading,'Cafe Astrology editorial',
        ['Trines describe smoother adjustment; sextiles require noticing and using opportunities.',
         'No individual outcome is guaranteed; natal circumstances matter.'])
hand='https://www.astro.com/astrologie/in_hand2_jupiter_effects_n.htm?lang=e&nho2=15975670&nhor=1'
add('Jupiter','Venus',[0,60,90,120,180],'Expression of affection and pleasure may become more visible.',hand,
    'Inward, first paragraph: Jupiter to Venus in any form','Robert Hand',
    ['General across-aspect delineation; aspect specificity must come from a separately labeled component.',
     'Indexed article content checked; direct page access presents a browser challenge.'])
add('Jupiter','Saturn',[0,60,90,120,180],'Growth may challenge inhibitions or proceed through disciplined engagement.',hand,
    'Inward, first paragraph: Jupiter to Saturn','Robert Hand',
    ['Two alternatives are preserved; no likelihood assigned.',
     'General pair interpretation, not an aspect-specific claim. Indexed article content checked.'])
Path('knowledge/transit_rules.json').write_text(json.dumps(rules,indent=2)+'\n',encoding='utf-8')
