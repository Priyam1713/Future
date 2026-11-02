"""Lightweight installed-runtime metadata/notice audit; not legal advice or a CVE scan."""
from importlib import metadata as m
from pathlib import Path
import hashlib,json

rows=[]
for line in Path('requirements.txt').read_text().splitlines():
    if not line.strip() or line.startswith('#'):continue
    name,version=line.split('==');dist=m.distribution(name)
    if dist.version!=version:raise ValueError(f'{name}: installed version differs from release pin')
    notices=[]
    for f in dist.files or []:
        if '.dist-info/' in str(f).replace('\\','/') and any(x in str(f).lower() for x in ('license','notice','copying')):
            data=Path(dist.locate_file(f)).read_bytes()
            notices.append({'path':str(f).replace('\\','/'),'sha256':hashlib.sha256(data).hexdigest()})
    if not notices:raise ValueError(f'No installed notice located for {name}')
    rows.append({'name':name,'version':version,'declared_license':dist.metadata.get('License-Expression') or dist.metadata.get('License'),
        'metadata_url':f'https://pypi.org/project/{name}/{version}/','notice_files':notices})
Path('knowledge/dependency_audit.json').write_text(json.dumps({'date':'2026-11-02','scope':'Source/local CLI Core v1; no bundled binary installer, kernel or third-party book redistribution',
    'runtime':rows,'kernel':{'name':'JPL DE440s','bundled_in_git':False,'source':'https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440s.bsp',
        'sha256':'c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2','policy':'Explicit direct download; preserve attribution. Any future kernel packaging needs a separate distributor-specific rights review.',
        'references':['https://ssd.jpl.nasa.gov/faq.html','https://naif.jpl.nasa.gov/naif/rules.html']},
    'source_material':'Metadata and short original factual/symbolic paraphrases only; copyrighted books and complete modern translations are not bundled.',
    'swiss':'Optional independent-reference generation only; not a runtime import, dependency or vendored library. No Swiss code distributed.',
    'project_license':'No project license has been granted by this audit; repository owner retains that decision. Third-party licenses do not license Future itself.',
    'distribution_actions':['Preserve complete installed upstream license/notice files with any future binary/dependency bundle, including NumPy component notices, Apache tzdata and MPL certifi notices.',
        'Review obligations for any modified third-party files; this release changes none.',
        'Do not infer commercial textbook/translation rights from web access.'],
    'deferred':['Binary packaging/commercial-distribution review','Automated vulnerability audit; no CVE-free assertion'],
    'result':'Metadata/notice checks passed; no prohibited runtime dependency introduced. Local/source core release scope only.'},indent=2)+'\n',encoding='utf-8')
