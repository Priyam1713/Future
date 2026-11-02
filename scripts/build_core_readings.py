"""Small source-reviewed 80/20 interpretation addition; factual paraphrases only."""
import json
from pathlib import Path

sources=[
    ('cafe-core-houses','Cafe Astrology editorial','Houses of the Natal Chart','https://cafeastrology.com/?da_image=houses-of-the-natal-chart'),
    ('cafe-core-sun','Cafe Astrology editorial','The Sun in Astrology','https://cafeastrology.com/sun.html'),
    ('cafe-core-moon','Cafe Astrology editorial','The Moon in Astrology','https://cafeastrology.com/moon.html'),
    ('cafe-core-mercury','Cafe Astrology editorial','Mercury in Astrology','https://cafeastrology.com/mercury.html'),
    ('cafe-core-progressions','Cafe Astrology editorial','Secondary Progressions','https://cafeastrology.com/secondaryprogressions.html'),
    ('shea-core-faq','Mary Fortier Shea','Solar Return FAQ','https://www.maryshea.com/frequently-asked-questions')]
sources=[dict(id=i,author=a,edition=e+'; checked 2026-11-02',url=u,ingestion='metadata_only',
              rights_note='Short original procedural/symbolic summaries only; no full articles or textbook text ingested.') for i,a,e,u in sources]
rows=[]
def add(id,kind,key,text,source,locator,variation='natal',exceptions=None):
    s=next(s for s in sources if s['id']==source)
    rows.append(dict(id=id,version=1,technique_id=1,tradition='modern psychological',kind=kind,key=str(key),text=text,
        source_id=source,url=s['url'],author=s['author'],edition=s['edition'],rights=s['rights_note'],locator=locator,
        variation=variation,status='source_checked',exceptions=exceptions or ['Symbolic practitioner framework; not a validated personal outcome.']))
topics=['self-presentation and initiative','resources and personal values','communication and nearby connections',
        'home and emotional foundations','creative play and romance','daily work and routines',
        'one-to-one partnerships','shared resources and change','beliefs, study and distant travel',
        'public role and responsibility','friendships and aspirations','privacy and hidden concerns']
for i,topic in enumerate(topics,1):
    add('core.modern.house.'+str(i),'house',i,topic,'cafe-core-houses','The '+str(i)+' house section',
        exceptions=['House topics only; natural sign/planet analogies are not used to calculate house rulers. No health/death prediction.'])
for body,text,source in [('Sun','identity, purpose and creative agency','cafe-core-sun'),
                         ('Moon','emotional needs, habits and instinctive responses','cafe-core-moon'),
                         ('Mercury','thinking, learning and communication','cafe-core-mercury')]:
    add('core.modern.symbol.'+body.lower(),'planet_symbol',body,text,source,'Opening meaning; sign and house paragraphs')
for phase,text in [('new','beginning a symbolic chapter'),('crescent','adjusting to emerging possibilities'),
                   ('first quarter','active construction'),('gibbous','refining the developing approach'),
                   ('full','fruition and culmination'),('disseminating','sharing experience'),
                   ('last quarter','reconsidering established approaches'),('balsamic','reflection and release')]:
    add('core.progression.phase.'+phase.replace(' ','-'),'phase',phase,text,'cafe-core-progressions',
        'Significant secondary progressions, item 3: The Progressed Lunation Cycle','secondary progressions')
add('core.return.house-focus','return_method','house-focus','Read the return as its own chart; emphasize planetary houses.',
    'shea-core-faq','FAQ 5–6','solar returns', ['Shea method: tropical, nonprecessed Placidus. Other house systems are not attributed to her.'])
for body,text in [('Mercury','review and reorganize thinking'),('Venus','reconsider internal values'),('Mars','reflect on anger and self-directed motivation')]:
    add('core.return.retrograde.'+body.lower(),'return_retrograde',body,text,'shea-core-faq','FAQ 7','solar returns',
        ['Only selected inner-planet retrograde symbolism; no outer-planet interpretation inferred.'])
Path('knowledge/core_interpretations.json').write_text(json.dumps(dict(version=1,sources=sources,records=rows,
    gaps=['Modern planetary meanings beyond Sun/Moon/Mercury deferred; sign and house components remain available.',
          'Direct natal/progression/return planet-pair delineations remain unsupported; transit rules are not reused as natal readings.',
          'Hellenistic readings use the existing named doctrine/time-lord reports, not imported modern symbolism.']),indent=2)+'\n',encoding='utf-8')
