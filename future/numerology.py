"""Exact arithmetic for a bounded, named Decoz profile."""
from datetime import date
from pathlib import Path
import json,re
PROFILE=json.loads((Path(__file__).resolve().parents[1]/'knowledge/numerology_profile_v1.json').read_text(encoding='utf-8'))

def readings(r):
    data=json.loads((Path(__file__).resolve().parents[1]/'knowledge/numerology_readings_v1.json').read_text(encoding='utf-8'))
    rows=[]
    for scope,table,value in [('expression','expression',r['expression']['result']),('personal_year','year',r['cycles']['year']['result'])]:
        source=data[table]
        rows.append({'scope':scope,'number':value,'coverage':'direct','text':source['meanings'][str(value)],
            'source_id':source['source_id'],'url':source['url'],'locator':source['locator']})
    for scope,text in [('life_path','Birth-date framework; no direct number-specific delineation in this core.'),('soul_urge','Vowel-based motivation context.'),('personality','Consonant-based outward presentation context.'),('birthday','Actual day retained alongside its reduced companion.')]:
        rows.append({'scope':scope,'coverage':'compositional','text':text,'source_id':'numerology-decoz-guide-v1','url':PROFILE['sources'][2]['url'],'locator':PROFILE['sources'][2]['locator']})
    r['readings']=rows;r['interpretation_limits']=data['limitations']
    return r

def reduce(n,masters=True):
    if isinstance(n,bool) or not isinstance(n,int) or n<0:raise ValueError('Nonnegative integer required')
    steps=[n]
    while n>9 and not (masters and n in (11,22,33)):
        n=sum(map(int,str(n)));steps.append(n)
    return {'input':steps[0],'steps':steps,'result':n}

def combine(values,masters=True):
    parts=[reduce(v,masters) for v in values]
    return {**reduce(sum(p['result'] for p in parts),masters),'components':parts}

def calculate(birth,name,basis,target,y_roles='',profile='decoz-component-reduction'):
    if profile!=PROFILE['profile'] or basis not in ('birth','current'):raise ValueError('Unsupported profile/name basis')
    b=date.fromisoformat(birth);t=date.fromisoformat(target)
    if not isinstance(name,str) or not re.fullmatch(r"[A-Za-z]+(?:[-'][A-Za-z]+)*(?: +[A-Za-z]+(?:[-'][A-Za-z]+)*)*",name):
        raise ValueError('Supply ASCII letters with internal spaces/hyphens/apostrophes; no silent normalization')
    if len(y_roles)!=name.upper().count('Y') or any(c not in 'vc' for c in y_roles):raise ValueError('Supply one v/c role per Y, left-to-right')
    roles=iter(y_roles);tokens=[]
    for part in name.upper().split():
        letters=[]
        for c in part:
            if c in "-'":continue
            vowel=next(roles)=='v' if c=='Y' else c in 'AEIOU'
            letters.append({'letter':c,'value':(ord(c)-65)%9+1,'vowel':vowel})
        tokens.append({'part':part,'letters':letters})
    names={}
    for key,kind in [('expression',None),('soul_urge',True),('personality',False)]:
        sums=[sum(c['value'] for c in p['letters'] if kind is None or c['vowel']==kind) for p in tokens]
        names[key]=combine(sums) if any(sums) else {'result':None,'coverage':'unsupported: no qualifying letters'}
    sun=reduce(b.month+b.day,False);year=reduce(sun['result']+t.year,False)
    month=reduce(year['result']+t.month,False);day=reduce(month['result']+t.day,False)
    return {'technique_id':4,'profile':profile,'birth':birth,'target':target,'name':{'original':name,'basis':basis,'y_roles':y_roles,'tokens':tokens},
        'life_path':combine([b.month,b.day,b.year]),'birthday':{'original_day':b.day,'companion':reduce(b.day)},
        **names,'cycles':{'sun':sun,'year':year,'month':month,'day':day,'year_interval':[f'{t.year:04}-01-01',f'{t.year+1:04}-01-01']},
        'sources':PROFILE['sources'],'conventions':PROFILE,'limitations':['Symbolic calculations, not validated personality diagnoses or event probabilities.','Current-name results are overlays, not silently substituted birth-name numbers.']}

def markdown(r):
    lines=['# Numerology', '',f"Profile: {r['profile']}; {r['name']['basis']} name: {r['name']['original']}.",'']
    for k in ('life_path','expression','soul_urge','personality'):lines.append(f"- {k}: {r[k]['result']}; trace {r[k].get('steps',[])}")
    lines+=['',f"Birthday: {r['birthday']['original_day']}; cycles: "+', '.join(f"{k}={r['cycles'][k]['result']}" for k in ('year','month','day'))]
    if 'readings' in r:
        lines+=['']+[f"- {x['scope']} ({x['coverage']}): {x['text']}" for x in r['readings']]
    lines+=['']+[f"- [{s['id']}]({s['url']}): {s['locator']}" for s in r['sources']]
    return '\n'.join(lines)+'\n'
