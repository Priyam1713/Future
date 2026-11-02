"""Small sourced dignity slice using the existing registry, scoped by tradition."""
from pathlib import Path
from .knowledge import Rule

def explain(chart, registry):
    source = {'id':'skyscript-sign-rulers','author':'Skyscript','edition':'Online glossary checked 2026-11-02',
              'url':'https://direct.skyscript.co.uk/glossary/sign-ruler/', 'ingestion':'facts_only',
              'rights_note':'Original concise notes only; no copyrighted text ingestion'}
    registry.add_source(source)
    registry.ingest_text('sign-rulers-notes-v1',source['id'],Path(__file__).resolve().parents[1]/'knowledge/notes/sign-rulers-v1.txt',
                         'Sign Rulers: domicile examples',content_kind='original_research_notes')
    tradition=chart['settings']['tradition']
    if tradition != 'medieval/traditional':
        return []
    for planet,sign in [('Sun','Leo'),('Moon','Cancer')]:
        registry.add_rule(Rule(id=f'traditional.domicile.{planet.lower()}',version=1,technique_id=1,
            variation='natal',tradition=tradition,source_id=source['id'],locator='Sign Rulers: explicit domicile examples',
            statement=f'{planet} in {sign} is in domicile.',operation='sign_equals',parameters={'planet':planet,'sign':sign},
            status='verified',evidence_kind='traditional',fixture_ids=[f'domicile-{planet.lower()}']))
    explanations=[]
    for rule in registry.select_rules(1,'natal',tradition):
        if rule['operation']=='sign_equals':
            p=rule['parameters']
            if chart['planets'][p['planet']]['sign']==p['sign']:
                explanations.append({'rule_id':rule['id'],'version':rule['version'],'statement':rule['statement'],
                    'evidence_kind':'traditional','meaning':'Domicile is a traditional symbolic dignity; predictive accuracy is not established.',
                    'calculated_longitude':chart['planets'][p['planet']]['longitude'],
                    'source':source['url'],'locator':rule['locator'],
                    'retrieved_context':[r['text'] for r in registry.search('domicile',[source['id']])]})
    return explanations
