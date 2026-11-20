"""Bounded consumer protocols for the World of Signs. Native engines own every comparison."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from future import (aeromancy, augury, cleromancy, coffee, haruspicy, hydromancy,
                    lithomancy, osteomancy, pyromancy, tasseography)

ENGINES = {
    28: tasseography, 29: coffee, 30: pyromancy, 31: hydromancy, 32: aeromancy,
    34: lithomancy, 35: osteomancy, 37: cleromancy, 38: augury, 39: haruspicy,
}


def readable(value):
    return value.replace('_', ' ').capitalize()


def choices(values, names=None):
    return [[value, (names or {}).get(value, readable(value))] for value in values]


def field(label, values, names=None):
    return dict(label=label, options=choices(values, names))


CASES = {row['case_id']: row for row in osteomancy.DATA['cases']}
PAIRS = {f'{a}+{b}': [a, b] for a, b in (
    ('9A','9B'), ('19A','19B'), ('20A','20B'), ('22A','22B'), ('24A','24B'))}
MARKS = {row['id']: row for row in cleromancy.catalog()}
STONE_ROLES = {k: v for k, v in lithomancy.ROLES.items() if k != 'lodestone'}
BOARD = [f'{x}:{y}' for y in range(2,-3,-1) for x in range(-2,3)]
FOSSILS = {'liver_head': ('liver','liver_head'), 'lung_cleft': ('lung','cleft'), 'whole_heart': ('heart','whole_organ')}
AIR_SHAPES = {'hake': ('cloud','cloud_axis'), 'smoke': ('smoke','smoke_drift_towards'), 'wind': ('wind','named_wind_direction')}
AIR_SETTINGS = {
    'hake': {'east_west': 'East–west axis', 'north_south': 'North–south axis', 'unknown': 'Axis unknown'},
    'smoke': {'east': 'Drifts east', 'west': 'Drifts west', 'unknown': 'Drift unknown'},
    'wind': {'east': 'From the east', 'west': 'From the west', 'unknown': 'Direction unknown'},
}
BIRD_SIGNS = {
    'call': ('call', 'located_on_side'), 'flight_to': ('flight', 'moving_to_side'),
    'flight_from': ('flight', 'moving_from_side'), 'flight_located': ('flight', 'located_on_side'),
}

FIELDS = {
    28: [
        field('Cup region', ['rim','side','bottom','unknown'], {'unknown':'Region unknown'}),
        field('Shape you identified', [*tasseography.SYMBOLS,'unknown'],
              {k:v['name'] for k,v in tasseography.SYMBOLS.items()}),
    ],
    29: [
        field('Vessel observed', ['cup','saucer']),
        field('Grounds you identified', [*coffee.DATA['symbols'],'two_humped_camel','unknown'],
              {'two_humped_camel':'Camel with two humps','adhered_grounds':'Grounds still adhered after inversion'}),
    ],
    30: [
        field('Height in your past record or example', ['high','normal','low','unknown']),
        field('How long it lasted', ['persistent','transient','unknown']),
        field('Physical check in that record', ['unknown','checked','persisted','hazard'],
              {'unknown':'No check recorded','checked':'Checked, no issue reported',
               'persisted':'Persisted after reported correction','hazard':'Active hazard reported'}),
        field('Record type', ['reported_real','hypothetical'], {'reported_real':'Past observation','hypothetical':'Hypothetical example'}),
    ],
    31: [
        field('What you noticed', ['physical_ripples','reflection','physical_mist','perceived_fogginess',
                                  'subjective_image','imagined_image','no_imagery','unknown']),
        field('How you classify it', ['physical','subjective','imagined','unknown']),
        field('Conditions you can confirm', ['source_context','unknown'],
              {'source_context':'Rainwater, dark bowl, soft gaze','unknown':'Leave conditions unspecified'}),
    ],
    32: [
        field('Atmospheric feature', list(AIR_SHAPES), {'hake':'Hake-shaped cloud','smoke':'Smoke drift','wind':'Wind direction'}),
        field('Orientation observed', sorted({k for v in AIR_SETTINGS.values() for k in v})),
        field('Region you declare', ['bedfordshire','scotland','texas','other','unknown']),
    ],
    34: [
        field('Stone beside your lodestone', list(STONE_ROLES), {k:v['item'] for k,v in STONE_ROLES.items()}),
        field('Center relative to the lodestone', BOARD),
    ],
    35: [
        field('Open a source case or a pair', [*CASES,*PAIRS],
              {k:f'Case {k}' for k in CASES} | {k:f'Compare {k.replace("+"," and ")}' for k in PAIRS}),
    ],
    37: [
        field('Mark from your declared lot', list(MARKS), {k:f'{v["glyph"]} · {v["name"]}' for k,v in MARKS.items()}),
    ],
    38: [
        field('Bird label you chose', ['crow','raven','unknown']),
        field('What you recorded', list(BIRD_SIGNS), {'call':'Call located on that side',
              'flight_to':'Flight toward that side','flight_from':'Flight from that side','flight_located':'Flight located on that side'}),
        field('Side relative to you', ['left','right','unknown']),
    ],
    39: [
        field('Feature in a written account', list(FOSSILS), {'liver_head':'Liver head','lung_cleft':'Lung cleft','whole_heart':'Whole heart'}),
        field('Presence in the account', ['present','absent','unknown']),
        field('Other vitals in the account', ['sound','not_sound','unknown']),
    ],
}


class SignInput(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    oracle: Literal[28,29,30,31,32,34,35,37,38,39]
    values: list[str] = Field(max_length=4)


def allowed(room, values):
    fields = FIELDS[room]
    return (len(values) == len(fields)
            and all(value in dict(spec['options']) for spec, value in zip(fields, values))
            and (room != 32 or values[1] in AIR_SETTINGS[values[0]]))


def pinned(engine):
    return dict(catalog_id=engine.DATA['catalog_id'],catalog_version=1,catalog_sha256=engine.CATALOG_HASH)


def native_request(room, v):
    if not allowed(room, v):
        raise ValueError('Complete the explicit selections for this room.')
    request = dict(schema_version=1, profile=ENGINES[room].PROFILE, mode='manual')
    row = dict(id='declared-1')
    if room == 28:
        return dict(request,task='symbolic_cup_reading',vessel='cup',observations=[dict(row,symbol_id=v[1],region=v[0])])
    if room == 29:
        attributes = {'humps':2} if v[1]=='two_humped_camel' else {'adhered_after_inversion': True} if v[1]=='adhered_grounds' else {}
        return dict(request,task='symbolic_coffee_reading',vessel=v[0],
            observations=[dict(row,symbol_id='camel' if v[1]=='two_humped_camel' else v[1],attributes=attributes)])
    if room == 30:
        physical = {
            'checked':dict(explanation='checked_no_issue',correction='not_needed_after_check'),
            'persisted':dict(explanation='addressed',correction='reported_completed',after_correction='persisted'),
        }.get(v[2], {})
        return dict(request,task='symbolic_candle_observation',origin=v[3],
            safety={'active_hazard':True} if v[2]=='hazard' else {},
            observations=[dict(row,phenomenon='flame',
                attributes=dict(substrate='candle_flame',height=v[0],persistence=v[1]),physical=physical)])
    if room == 31:
        session = dict(medium='water',container='dark_bowl',rainwater=True,gaze='soft') if v[2]=='source_context' else {}
        return dict(request,task='water_observation_reference',session=session,
            observations=[dict(row,sequence=1,category=v[0],basis=v[1])])
    if room == 32:
        phenomenon,feature = AIR_SHAPES[v[0]]
        features = {feature:v[1]}
        if v[0]=='wind':
            features['wind_direction_convention']='from'
        if v[0]=='hake':
            features['cloud_appearance']='hake_shaped'
        return dict(request,task='atmospheric_lore_comparison',region=v[2],
            observations=[dict(row,phenomenon=phenomenon,features=features)])
    if room == 34:
        x,y = map(int,v[1].split(':'))
        return dict(request,task='manual_spatial_reading',reading_id='consumer-table',
            frame='integer-centers-x-right-y-up-v1',coverage='subset',
            stones=[dict(id='center',role_id='lodestone',position=dict(x=0,y=0)),
                    dict(id='stone',role_id=v[0],position=dict(x=x,y=y))],
            anchor=dict(kind='personal_stone',stone_id='center'))
    if room == 35:
        selected = PAIRS.get(v[0],[v[0]])
        return dict(request | {'mode':'documentary'},task='compare' if len(selected)>1 else 'reference',case_ids=selected)
    if room == 37:
        return dict(request,**pinned(cleromancy),task='reading',mark=v[0])
    if room == 38:
        phenomenon,relation = BIRD_SIGNS[v[1]]
        return dict(request,**pinned(augury),task='observe',observations=[
            dict(observation_id='declared-1',bird_label=v[0],phenomenon=phenomenon,
                 relative_side=v[2],relation=relation,reference_frame='observer_relative')])
    organ,feature = FOSSILS[v[0]]
    return dict(request,**pinned(haruspicy),task='compare',observations=[
        dict(observation_id='declared-1',tradition='roman',organ=organ,feature=feature,presence=v[1],
             other_vitals=v[2],origin='source_description')])

MATCHED = {'applicable','source_supported','attributed_source_account'}
STATUS = {
    'applicable':'Source conditions match',
    'source_supported':'Source conditions match',
    'attributed_source_account':'Attributed source account',
    'not_applicable':'Conditions differ',
    'insufficient_evidence':'Context incomplete',
    'insufficient_information':'Context incomplete',
    'missing_context':'Context incomplete',
    'conflicting_evidence':'The source accounts differ',
    'unsupported':'Outside this source’s scope',
}
UNMATCHED = {
    'Conditions differ':'No case met the conditions you declared.',
    'Context incomplete':'This reference needs more context before a match can be made.',
    'The source accounts differ':'The native comparison leaves the competing evidence open.',
    'Outside this source’s scope':'The pinned edition gives no supported account for these selections.',
}


def project(room, native):
    sources = native.get('sources') or [native.get('source', {})]
    source_urls = {source['id']:source.get('url','') for source in sources if source.get('id')}
    root = sources[0]
    excerpts = []

    def cite(record, text, status='applicable'):
        if not text:
            return
        excerpts.append(dict(text=text, locator=record.get('locator',root.get('locator','')),
            url=record.get('source_url') or source_urls.get(record.get('source_id'),root.get('url','')),
            sourceId=record.get('source_id',root.get('id','')), status=STATUS.get(status,readable(status))))

    if room == 30 and native['safety']['symbolic_hold']:
        return dict(status='Safety hold', lead=native['safety']['message'], excerpts=[], metric=None)
    if room == 34:
        placement = native['placements'][1]
        distance = native['spatial']['distances'][0]
        role = placement['source_role']
        cite(role,role['association'])
        return dict(status='Relative placement',lead=role['association'],excerpts=excerpts,
            metric={'distanceSquared':distance['distance_squared'],'direction':distance['direction']})
    if room == 35:
        for record in native['records']:
            cite(record,record['components']['charge']['value'], 'documentary_case')
        descriptions = [c['relationship']['scope'] for c in native['comparisons']
                        if c.get('relationship') and c['relationship'].get('scope')]
        return dict(status='Documentary comparison' if descriptions else 'Documentary case',
            lead=descriptions[0] if descriptions else excerpts[0]['text'] if excerpts else 'The inspected excerpt omits the charge.',
            excerpts=excerpts,metric=None)
    if room == 37:
        record = native['selected_mark']
        cite(record,record['source_account'])
        cite(record,record['lexical_qualification'],'qualification')
        return dict(status='Declared lot',lead=record['source_account'],excerpts=excerpts,metric=None)

    observation = native['observations'][0]
    raw_status = observation['status']
    matched = []
    for case in observation.get('cases',observation.get('evaluations',[])):
        record = case.get('reference') or case.get('source_record') or case
        status = case['status']
        actual = case.get('displayed_account') or case.get('account')
        statement = actual or record.get('statement') or record.get('source_account')
        if not statement:
            continue
        if status in MATCHED:
            matched.append(statement)
        cite(record,statement,status)
    status = STATUS.get(raw_status,readable(raw_status))
    lead = (matched[0] if matched and raw_status in MATCHED else
            UNMATCHED.get(status,'The selected declaration is available to compare with the source notes.'))
    return dict(status=status,lead=lead,excerpts=excerpts,metric=None)


def read_sign(query):
    engine = ENGINES[query.oracle]
    result = engine.read(native_request(query.oracle,query.values))
    view = project(query.oracle,result)
    snapshot = None if view['status']=='Safety hold' else dict(
        oracle=query.oracle,profile=engine.PROFILE,values=query.values)
    return dict(result=result,view=view,snapshot=snapshot)
