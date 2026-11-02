"""Curated factual extraction, not generated interpretation prose. Rebuild JSON."""
import json
from pathlib import Path
records=[]
def add(identifier,kind,key,text,url,locator,author='William Lilly / adaptation by Deborah Houlding',tradition='medieval/traditional',**extra):
    extra.setdefault('exceptions',[])
    records.append(dict(id=identifier,version=1,technique_id=1,kind=kind,key=key,text=text,url=url,locator=locator,
                        author=author,edition='Christian Astrology 1647 via Skyscript' if 'Lilly' in author else 'Online article',
                        tradition=tradition,status='source_checked',checked_on='2026-11-02',
                        rights='Original concise research paraphrase; no full text ingestion',**extra))
houses=['life and appearance','movable property and money','siblings, neighbours, letters and short journeys',
        'father, land, dwellings and inheritances','children, entertainment and banquets','servants, labourers and small cattle; historical illness symbolism',
        'marriage, opponents and lawsuits','legacies, wills and fear; historical death symbolism',
        'long journeys, religion, dreams and learning','mother, public authority, honour and profession',
        'friends, hopes and allies','hidden enemies, confinement and sorrow']
for i,text in enumerate(houses,1):
    add(f'lilly.house.{i}','house',str(i),text,'https://www.skyscript.co.uk/lilly_houses.html',f'House {i}, CA pp.50–56')
planets={
 'Sun':(['Leo'],'Aries','Libra','authority and rulers; hot and dry','sun_att.html'),
 'Moon':(['Cancer'],'Taurus','Scorpio','changeability; cold and moist','moonatt.html'),
 'Mercury':(['Gemini','Virgo'],'Virgo','Pisces','adaptability, writing, trade and calculation','mercury_att.html'),
 'Venus':(['Taurus','Libra'],'Pisces','Virgo','pleasure, music, adornment and artists','venus_att.html'),
 'Mars':(['Aries','Scorpio'],'Capricorn','Cancer','courage, conflict, soldiers and metalworkers','marsatt.html'),
 'Jupiter':(['Sagittarius','Pisces'],'Cancer','Capricorn','justice, moderation, judges and scholars','jupiter_att.html'),
 'Saturn':(['Capricorn','Aquarius'],'Libra','Aries','solitude, age, labour and melancholy','saturn_att.html')}
for name,(dom,exalt,fall,text,page) in planets.items():
    add(f'lilly.planet.{name}','planet',name,text,'https://www.skyscript.co.uk/'+page,'Nature and People Signified; Dignities',
        domicile=dom,exaltation=exalt,fall=fall,
        exceptions=['Sign-level dignities only. No triplicity, bounds, faces, sect scoring or diagnosis inferred.',
                    'Adaptation page headers repeat inconsistent page numbers; use section locators.'])
meanings={0:'combination of planetary significations; quality depends on the planets',60:'harmonious cooperation, weaker than a trine',
          90:'friction and tension, potentially motivating effort',120:'easy harmonious combination; potential may remain unused',
          180:'opposing pressures and conflicting possibilities'}
for angle,text in meanings.items():
    add(f'campion.aspect.{angle}','aspect',str(angle),text,'https://www.skyscript.co.uk/aspects2.html','Table of Aspects and aspect descriptions',
        author='Nicholas Campion',tradition='modern psychological',
        exceptions=['General aspect symbolism, not a planet-pair-specific transit delineation.'])
    add(f'skyscript.aspect.{angle}','aspect',str(angle),text if angle else 'corporeal union, distinguished from witnessing by aspect',
        'https://www.skyscript.co.uk/glossary/aspect/','Named major-aspect entry',author='Skyscript glossary',
        exceptions=['General aspect symbolism; conjunction traditionally distinguished from aspect.'])
add('campion.application','procedure','application','Applying approaches exactness; separating moves away. Retrograde motion must be considered.',
    'https://www.skyscript.co.uk/aspects2.html','Applying & Separating Aspects',author='Nicholas Campion',tradition='modern psychological')
add('skyscript.orbs','procedure','orbs','Traditional planetary moieties differ from modern aspect-based orbs.',
    'https://www.skyscript.co.uk/glossary/orbs/','Planetary rays and Sun/Moon worked example',author='Skyscript glossary',
    example={'Sun':15,'Moon':12,'combined':13.5})
add('hand.saturn.scope','methodology','Saturn','Saturn transit cycles over natal points and through houses require a long-term perspective.',
    'https://www.astro.com/astrologie/in_hand2_saturn_effects_i.htm?lang=e','Indexed concluding paragraph; full page blocked',
    author='Robert Hand',tradition='modern psychological',
    exceptions=['Search-index verification only; no planet-pair delineation extracted.'])
signs={'Aries':'initiative and competitiveness','Taurus':'settlement, cultivation and material stability',
       'Gemini':'duality and reconciliation of contrasting forces','Cancer':'protectiveness and sensitivity',
       'Leo':'solar strength, prominence and brilliance','Virgo':'discernment, study and analysis',
       'Libra':'balance, evaluation and restoring equilibrium','Scorpio':'intensity, subtlety and self-preservation',
       'Sagittarius':'broad vision, optimism and philosophical freedom','Capricorn':'patient disciplined effort through adversity',
       'Aquarius':'refreshment and enlightenment; air and water symbolism','Pisces':'duality and vacillation between competing directions'}
for name,text in signs.items():
    add(f'houlding.sign.{name}','sign',name,text,'https://www.skyscript.co.uk/'+name.lower()+'.html',
        'Sign symbolism, opening discussion',author='Deborah Houlding',tradition='modern psychological',
        exceptions=['Symbolic sign description, not an inference of a person’s fixed character.'])
Path('knowledge/western_rules.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
