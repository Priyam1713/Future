"""Factual table transcription from identified historical diagrams; no scores."""
from pathlib import Path
import json
names={'S':'Saturn','J':'Jupiter','A':'Mars','U':'Sun','V':'Venus','M':'Mercury','L':'Moon'}
egyptian=['J6 V12 M20 A25 S30','V8 M14 J22 S27 A30','M6 J12 V17 A24 S30','A7 V13 M19 J26 S30',
 'J6 V11 S18 M24 A30','M7 V17 J21 A28 S30','S6 M14 J21 V28 A30','A7 V11 M19 J24 S30',
 'J12 V17 M21 S26 A30','M7 J14 V22 S26 A30','M7 V13 J20 A25 S30','V12 J16 M19 A28 S30']
lilly=['J6 V14 M21 A26 S30','V8 M15 J22 S26 A30','M7 J14 V21 S25 A30','A6 J13 V20 M27 S30',
 'S6 M13 V19 J25 A30','M7 V13 J18 S24 A30','S6 V11 J19 M24 A30','A6 V14 J21 M27 S30',
 'J8 V14 M19 S25 A30','V6 M12 J19 J25 A30','S6 M12 V20 J25 A30','V8 J14 M20 A26 S30']
# Capricorn's fourth term is Saturn (not Jupiter): retain explicit transcription.
lilly[9]='V6 M12 J19 S25 A30'
def decode(rows):return [[[names[p[0]],int(p[1:])] for p in row.split()] for row in rows]
data={'version':1,'technique_id':1,'bounds':{
 'egyptian':{'source':'https://www.skyscript.co.uk/im/2014/egyptianterms.gif','locator':'The Egyptian terms, twelve rows; endpoints in parentheses','rows':decode(egyptian)},
 'lilly-ptolemaic':{'source':'https://www.skyscript.co.uk/im/dignities2.gif','locator':'Lilly CA p.104: The Terms of the Planets','rows':decode(lilly),
 'exception':'Named Lilly transmission, not an assertion that all Ptolemy manuscripts agree.'}},
 'domicile':['Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Saturn','Jupiter'],
 'exaltation':{'Sun':[0,19],'Moon':[1,3],'Mercury':[5,15],'Venus':[11,27],'Mars':[9,28],'Jupiter':[3,15],'Saturn':[6,21]},
 'faces':{'sequence':['Mars','Sun','Venus','Mercury','Moon','Saturn','Jupiter'],'width':10,
          'source':'https://www.skyscript.co.uk/im/dignities2.gif','locator':'The Faces of the Planets'},
 'triplicities':{
 'dorothean':{'fire':['Sun','Jupiter','Saturn'],'earth':['Venus','Moon','Mars'],'air':['Saturn','Mercury','Jupiter'],'water':['Venus','Mars','Moon']},
 'lilly':{'fire':['Sun','Jupiter',None],'earth':['Venus','Moon',None],'air':['Saturn','Mercury',None],'water':['Mars','Mars',None]}},
 'triplicity_source':'https://www.skyscript.co.uk/triplicities.html',
 'triplicity_locator':'Ancient Assignment of Triplicity Rulers; Lilly two-ruler variant checked against p.104 diagram',
 'intervals':'Zero-based degrees, lower inclusive and upper exclusive; exact 30 degrees belongs to next sign.',
 'rights':'Factual mathematical table data, not reproduced page imagery or copyrighted book text.'}
Path('knowledge/doctrine_tables.json').write_text(json.dumps(data,indent=2)+'\n')
