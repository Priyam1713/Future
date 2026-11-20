"""Consumer requests over pinned archival references and the native sky engines."""

from datetime import datetime, timezone
from typing import Annotated, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field

from future import (astrocartography, aura, face_reading, feng_shui, graphology,
                    horary, iridology, moleosophy, mundane, palmistry, phrenology, podomancy)


MANUSCRIPTS = {
    8: palmistry, 9: face_reading, 10: phrenology, 11: moleosophy,
    12: podomancy, 13: graphology, 14: aura, 15: iridology,
}
SKY_BODIES = list(astrocartography.BODIES)
MOUNTAINS = feng_shui.assets()[1]['rows']


class Input(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class ArchiveInput(Input):
    oracle: Literal[8, 9, 10, 11, 12, 13, 14, 15]
    selection: str = Field(min_length=1, max_length=80)
    hand: Literal['left', 'right'] | None = None


class Site(Input):
    latitude: float = Field(gt=-90, lt=90)
    longitude: float = Field(ge=-180, le=180)
    zone: str = Field(min_length=1, max_length=80)


class Moment(Site):
    local: str = Field(pattern=r'^\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?$')
    fold: int | None = Field(default=None, ge=0, le=1)


class HoraryInput(Input):
    oracle: Literal[5]
    question: str = Field(min_length=1, max_length=320)
    moment: Moment


class MundaneInput(Input):
    oracle: Literal[6]
    year: int = Field(ge=1851, le=2148)
    site: Site
    cycle: Literal['ingresses', 'conjunctions']


class MapInput(Input):
    oracle: Literal[7]
    moment: Moment


class CompassInput(Input):
    oracle: Literal[40]
    bearing: int = Field(ge=0, le=3599)
    uncertainty: int = Field(ge=0, le=1800)
    north: Literal['source_diagram', 'true', 'magnetic', 'unknown']
    role: Literal['source_heading', 'building_facing', 'building_sitting', 'door', 'observer', 'unknown']


Request = Annotated[HoraryInput | MundaneInput | MapInput | ArchiveInput | CompassInput, Field(discriminator='oracle')]


def humanize(value):
    return value.replace('_', ' ').replace('-', ' ').capitalize()


def archive_options(oracle):
    data = MANUSCRIPTS[oracle].DATA
    if oracle == 8:
        return [
            ('head.length.short', 'Head line', 'Barely reaches the middle of the palm'),
            ('head.curvature.straight', 'Head line', 'Straight, clear and unbroken'),
            ('head.curvature.very_sloping', 'Head line', 'Strongly sloping'),
            ('heart.origin.jupiter', 'Heart line', 'Begins at the mount of Jupiter'),
            ('heart.origin.saturn', 'Heart line', 'Begins at the mount of Saturn'),
            ('life.branch_to.jupiter', 'Life line', 'Branch toward Jupiter'),
            ('life.continuity.unbroken', 'Life line', 'Unbroken'),
        ]
    if oracle == 9:
        return [(key, 'Region index', humanize(key)) for key in data['regions']]
    if oracle == 10:
        return [(f'{panel}/{key}', sheet['label'], f'{key} · {data["entries"][key]["original_name"]}')
                for panel, sheet in data['schematics'].items() for key in sheet['locations']]
    if oracle == 11:
        return [(key, humanize(row['region_id']), row['original_label']) for key, row in data['entries'].items()]
    if oracle == 12:
        return [(key, 'Original examples', data['entries'][key]['source_label']) for key in data['source_examples']]
    if oracle == 13:
        return [(key, humanize(row['features'][0]), row['term']) for key, row in data['terms'].items()]
    if oracle == 14:
        return ([(key, 'Colour key', row['color']) for key, row in data['terms'].items()]
                + [(key, 'Published figures', row['title']) for key, row in data['source_examples'].items()])
    return [(key, f'{humanize(row["eye"])} iris on the printed plate', row['printed_label'].title())
            for key, row in data['entries'].items()]


def archive_request(oracle, selection, hand=None):
    if selection not in {row[0] for row in archive_options(oracle)}:
        raise ValueError('Choose a card from this source edition.')
    base = dict(schema_version=1, profile=MANUSCRIPTS[oracle].PROFILE, task='historical_reference')
    if oracle == 8:
        if hand is None:
            raise ValueError('Declare the left or right hand.')
        line, field, value = selection.split('.')
        observation = {'presence': 'present', field: value}
        if selection == 'head.curvature.straight':
            observation.update(clarity='clear', continuity='unbroken')
        return dict(schema_version=1, profile=palmistry.PROFILE, hands=[
            dict(side=hand, lines={line: observation})])
    if hand is not None:
        raise ValueError('Hand side applies only to the palm room.')
    if oracle == 9:
        return dict(base, mode='manual', orientation=dict(view='frontal', side_frame='subject', mirrored=False),
                    observations=[dict(region_id=selection, side='both' if selection in ('eyes', 'cheeks') else 'midline',
                                       visibility='visible')])
    if oracle == 10:
        panel, key = selection.split('/')
        return dict(base, schematic=panel, selections=[dict(label_id=key)])
    if oracle == 11:
        return dict(base, mode='manual', orientation=dict(frame='subject', view='unknown', mirrored=False),
                    selections=[dict(entry_id=selection)])
    if oracle == 12:
        return dict(base, mode='source_example', example_id=selection)
    if oracle == 13:
        return dict(base, mode='manual', script='latin', writing_direction='ltr', observations=[
            dict(feature=graphology.DATA['terms'][selection]['features'][0], category=selection)])
    if oracle == 14:
        base['task'] = 'symbolic_reference'
        return (dict(base, mode='source_example', example_id=selection) if selection.startswith('figure-')
                else dict(base, mode='manual', components=[dict(color=selection)]))
    row = iridology.DATA['entries'][selection]
    return dict(base, mode='manual', diagram='frontispiece', view='source_plate_upright',
                selections=[dict(eye=row['eye'], label_id=row['label_id'])])


def source_note(row, source, text, locator='locator'):
    return dict(text=text, locator=row.get(locator) or source.get('locator', ''),
                sourceId=row.get('source_id') or source['id'], url=source.get('url', ''))


def archive_view(oracle, result, selection):
    group, label = next((g, name) for key, g, name in archive_options(oracle) if key == selection)
    source = result['source']
    if oracle == 8:
        readings = result['hands'][0]['readings']
        notes = [source_note(row, source, row['text']) for row in readings]
        lead = ('In Cheiro’s edition: ' + readings[0]['text'] if notes
                else 'The observation is recorded. This edition offers no matched interpretation for this choice.')
        return dict(title=label, status='Declared line observation', lead=lead, sources=notes or [
            source_note({}, source, result['observation_guide']['line_definitions'][selection.split('.')[0]])])
    if oracle == 9:
        row = result['regions'][0]['historical_reference']
        notes = [source_note(row, source, row['historical_association'])]
        lead = row['region_description']
    elif oracle == 10:
        row = result['results'][0]['entry']
        lead = row['location']['description']
        notes = [source_note(row, source, row['original_name'] + ' · ' + row['category'], 'legend_locator')]
    elif oracle == 11:
        row = result['results'][0]['entry']
        lead = 'Fontaine indexes this region under “' + row['original_label'] + '”.'
        notes = [source_note(row, source, row['historical_association'])]
    elif oracle == 12:
        row = result['results'][0]['entry']
        lead = 'This wording appears in the foot and sole passages of the anonymous edition.'
        notes = [source_note(row, source, row.get('historical_association', row['source_label']))]
    elif oracle == 13:
        row = result['observations'][0]['reference']
        lead = row['definition']
        notes = [source_note(row, source, row['historical_context'] or lead)]
    elif oracle == 14:
        row = result['source_example'] or result['components'][0]['reference']
        lead = row['description']
        notes = [source_note(row, source, lead)]
    else:
        row = result['selections'][0]['reference']
        lead = row['description']
        notes = [source_note(row, source, 'Printed label: ' + row['printed_label'])]
    return dict(title=label, status=group if oracle == 14 else 'Historical reference',
                lead=lead, sources=notes)


def read_archive(oracle, selection, hand=None):
    engine = MANUSCRIPTS[oracle]
    native = archive_request(oracle, selection, hand)
    result = (engine.read if oracle == 8 else engine.reference)(native)
    return result, archive_view(oracle, result, selection)


def compass_request(q):
    return dict(schema_version=1, profile=feng_shui.PROFILE, catalog_id=feng_shui.DATA['catalog_id'],
                catalog_version=1, catalog_sha256=feng_shui.CATALOG_HASH, mode='manual', task='classify',
                bearing_tenths=q.bearing, uncertainty_tenths=q.uncertainty,
                north_reference=q.north, bearing_role=q.role)


def mountain_view(row):
    sources = {s['id']: s for s in feng_shui.assets()[1]['sources']}
    source = sources[row['source_id']]
    start, end = (row[field] / 10 for field in ('lower_tenths', 'upper_tenths'))
    line = f'{start:.1f}° to {end:.1f}°' + (', crossing north' if row['wraps_north'] else '')
    return dict(title=row['source_label'], status='24-mountain reference', lead=line, sources=[
        source_note(row, source, line, 'source_locator')])


def sky_read(q, ephemeris):
    site = q.site if isinstance(q, MundaneInput) else q.moment
    try:
        ZoneInfo(site.zone)
    except (ValueError, ZoneInfoNotFoundError) as exc:
        raise ValueError('Choose a recognized IANA timezone.') from exc
    location = (site.zone, site.latitude, site.longitude)
    if isinstance(q, HoraryInput):
        return horary.assess(ephemeris, q.question, 'advice-intent', q.moment.local, *location, fold=q.moment.fold)
    if isinstance(q, MundaneInput):
        if q.cycle == 'ingresses':
            return mundane.ingresses(ephemeris, q.year, *location)
        start, end = (datetime(y, 1, 1, tzinfo=timezone.utc) for y in (q.year, q.year + 1))
        return mundane.conjunctions(ephemeris, start, end, *location)
    return astrocartography.generate(ephemeris, q.moment.local, *location,
                                     fold=q.moment.fold, bodies=SKY_BODIES)


def read(q, western):
    if isinstance(q, ArchiveInput):
        result, view = read_archive(q.oracle, q.selection, q.hand)
        # Palm observations can refer to the visitor. Save and reopen the source entry alone.
        return dict(result=result, view=view, reference=q.selection)
    if isinstance(q, CompassInput):
        result = feng_shui.read(compass_request(q))
        row = result['readings'][0]
        views = [mountain_view(m) for m in row['possible_mountains']]
        return dict(result=result, mountainViews=views, references=row['possible_mountain_ids'])
    with western.lock:
        return dict(result=sky_read(q, western.get_ephemeris()))
