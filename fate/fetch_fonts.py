"""One-time asset provenance utility; runtime never fetches external fonts."""
import json
import re
import urllib.request
from pathlib import Path

def main():
    directory=Path(__file__).parent/'web/public/fonts'
    directory.mkdir(parents=True,exist_ok=True)
    url='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&family=Inter:wght@100..900&display=swap'
    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})
    css=urllib.request.urlopen(request).read().decode()
    sources={}
    for block in re.findall(r'/\* latin \*/\s*(@font-face\s*\{[^}]+\})',css):
        font_url=re.search(r'url\(([^)]+)\)',block)[1]
        name='inter-latin.woff2' if "'Inter'" in block else 'cormorant-italic-latin.woff2' if 'font-style: italic' in block else 'cormorant-latin.woff2'
        (directory/name).write_bytes(urllib.request.urlopen(font_url).read())
        sources[name]=font_url
    for family in ['inter','cormorantgaramond']:
        license_url=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/OFL.txt'
        (directory/f'{family}-OFL.txt').write_bytes(urllib.request.urlopen(license_url).read())
        sources[f'{family}-OFL.txt']=license_url
    (directory/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
    print('Vendored',len(sources),'font files and licenses')

if __name__=='__main__': main()
