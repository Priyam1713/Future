"""Read-only stdlib comparison of original XLSX cells and frozen JSON inventory."""
import hashlib,json,posixpath,re,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
def column(address):
    letters=re.match('[A-Z]+',address)[0];n=0
    for char in letters:n=n*26+ord(char)-64
    return n
def read_sheets(path):
    result={}
    with zipfile.ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():shared=[''.join(t.text or '' for t in si.iter(NS+'t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find(NS+'sheets'):
            target=rels[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
            target=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl',target))
            root=ET.fromstring(z.read(target));data=root.find(NS+'sheetData');dimension=root.find(NS+'dimension')
            if dimension is None:
                width=max(column(c.attrib['r']) for row in data for c in row);height=max(int(row.attrib['r']) for row in data)
            else:
                address=dimension.attrib['ref'].split(':')[-1];width=column(address);height=int(re.search('[0-9]+',address)[0])
            rows=[[None]*width for _ in range(height)]
            for row in data:
                ri=int(row.attrib['r'])-1
                for cell in row:
                    ci=column(cell.attrib['r'])-1;kind=cell.attrib.get('t','n');v=cell.find(NS+'v');f=cell.find(NS+'f')
                    if f is not None:value='='+(f.text or '')
                    elif kind=='inlineStr':value=''.join(t.text or '' for t in cell.iter(NS+'t')) or None
                    elif v is None:value=None
                    elif kind=='s':value=shared[int(v.text)]
                    elif kind=='b':value=bool(int(v.text))
                    elif kind in ('str','e'):value=v.text
                    elif kind=='n':value=float(v.text) if any(a in v.text.lower() for a in ('.','e')) else int(v.text)
                    else:raise ValueError('Unsupported workbook cell representation: '+kind)
                    rows[ri][ci]=value
            result[sheet.attrib['name']]=rows
    return result
def run():
    path=R/'resources/Prediction_Techniques_Resource_Inventory_v1.xlsx';inventory=json.loads((R/'knowledge/inventory.json').read_text(encoding='utf-8'));sha=hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha==inventory['source_sha256'];sheets=read_sheets(path);assert sheets==inventory['sheets'],'Original workbook cell values differ from frozen inventory'
    assert len(sheets)==6 and [r[0] for r in sheets['60 Methods'][1:]]==list(range(1,61))
    assert [r[0] for r in sheets['6 Exclusions'][1:]]==[25,27,41,42,47,48]
    print('Original workbook SHA256 and all six sheets match frozen inventory cell-for-cell;60 IDs and six exclusions pass')
    return dict(passed=True,source_sha256=sha,sheets=6,methods=60,excluded=[25,27,41,42,47,48],method='Independent read-only stdlib XLSX XML extraction compared cell-for-cell with frozen JSON; no openpyxl dependency')
if __name__=='__main__':run()
