#!/usr/bin/env python3
"""Source/ZIP completeness only, no human aesthetic pass and no Stella verification."""
from pathlib import Path
import json,hashlib,re,random
from PIL import Image
R=Path(__file__).resolve().parent
S=json.loads((R/'SOURCE_8x12.json').read_text('utf8'))
P=S['pixels']
assert set(S['new_candidates'])=={'D1_head_expression','D2_swaying_arms'}
assert set(S['baseline'])=={'U1_frozen'}
assert P['screen_native']==[160,192] and P['screen_tv_approx']==[640,480]
assert [P['level_dimensions'][str(i)] for i in (1,2,3)]==[[8,12],[16,24],[32,36]]
assert S['source_p3_sha256']=='72ebc4dc58200f2761e942b5d6c21ac8e0308fba368d15d976715c850056450f'
oldA=['00100100','01111110','01011010','01100111','00111110','11111110','10111100','00111100','00111100','01100110','01000110','11000011']
oldB=['00100100','01111110','01011010','01100111','00111110','01111111','00111101','00111100','00111100','01100110','01100010','11000001']
u=S['baseline']['U1_frozen'];assert u['A']==oldA and u['B']==oldB, 'Frozen P3 U1 changed'
groups={'U1_FROZEN':u,'D1_NEW':S['new_candidates']['D1_head_expression'],'D2_NEW':S['new_candidates']['D2_swaying_arms']}
inc=(R/'PIXEL_DATA_ONLY.inc').read_text('utf8')
for line in inc.splitlines():
 q=line.strip()
 assert not q or q.startswith(';') or (q.startswith('SkraunP3F1_Post_') and q.endswith(':')) or re.fullmatch(r'dc\.b %[01]{8}',q),'unexpected code '+q
for name,v in groups.items():
 for p in 'AB':
  rows=v[p]
  assert len(rows)==12 and all(len(a)==8 and set(a)<={'0','1'} for a in rows)
  assert v[p+'_left']==[r[::-1] for r in rows],name+' mirror'
  for f in ('RIGHT','LEFT'):
   target=rows if f=='RIGHT' else v[p+'_left']
   short=name[:2]
   fn=R/f'NATIVE_8x12_{short}_{p}_{f}.png'
   assert fn.exists(),fn
   with Image.open(fn) as img:
    assert img.size==(8,12) and img.mode=='RGB'
    for y,row in enumerate(target):
     for x,bit in enumerate(row):
      expect=tuple(P['gray']) if bit=='1' else tuple(P['off'])
      assert img.getpixel((x,y))==expect,(name,p,f,x,y)
   for order in ('TOP_FIRST','BOTTOM_FIRST'):
    tag=f'SkraunP3F1_Post_{name}_{p}_{f}_{order}:\n'
    assert tag in inc,tag
    lines=re.findall(r'dc\.b %([01]{8})',inc.split(tag,1)[1].split('\n\n',1)[0]);assert lines==(target if order=='TOP_FIRST' else target[::-1]),tag
 diffs=[[x,y] for y,(ra,rb) in enumerate(zip(v['A'],v['B'])) for x,(a,b) in enumerate(zip(ra,rb)) if a!=b]
 assert diffs==v['pose_changed_cells'],name+' pose ledger'
 if name!='U1_FROZEN':
  assert len(diffs)>=6,name+' motion insufficient'
  assert any(y in (6,7) for x,y in diffs) and any(y in (10,11) for x,y in diffs),'Arms or legs static'
  assert v['A'][:5]==v['B'][:5],name+' head flickers'
# Candidate-specific authored-feature checks (geometric tests, NOT recognition proof)
d1=S['new_candidates']['D1_head_expression']
for p in 'AB':
 assert d1[p][0].count('1')==2
 assert d1[p][2][2]==d1[p][2][5]=='0'
 assert d1[p][3][3:5]==d1[p][4][3:5]=='00'
 assert d1[p][5]=='01111110'
d2=S['new_candidates']['D2_swaying_arms']
for p in 'AB':assert d2[p][:4]==u[p][:4], 'D2 original U1 top rows drifted'
for y in (4,7,8):assert d2['A'][y]==d2['B'][y], 'stable torso should not blink'
# Raw visual media and source-distance ledger
assert len(list(R.glob('NATIVE_8x12_*.png')))==12
assert len(list(R.glob('GIF_*.gif')))==6
for filename in R.glob('*.png'):
 with Image.open(filename) as im:im.verify()
for gif in R.glob('GIF_*.gif'):
 with Image.open(gif) as im:
  assert im.n_frames==2 and im.size==(240,164)
  for k in (0,1):
   im.seek(k); assert im.info.get('duration')==140
led=json.loads((R/'SOURCE_DISTANCE_AUDIT.json').read_text('utf8'))
assert set(led['families'])=={'U1','D1','D2'}
def hd(a,b):return sum(x!=y for r,s in zip(a,b) for x,y in zip(r,s))
for short,name in [('U1','U1_FROZEN'),('D1','D1_NEW'),('D2','D2_NEW')]:
 q=groups[name];a,al,b,bl=q['A'],q['A_left'],q['B'],q['B_left'];matrix=led['families'][short]['pairwise_hamming_96_cells']
 assert matrix==[[hd(x,y) for y in (a,al,b,bl)] for x in (a,al,b,bl)]
# Reproducible blind key stable order
cases=[(n,p,f) for n in ['U1','D1','D2'] for p in 'AB' for f in ('RIGHT','LEFT')]
random.Random(P['blind_seed']).shuffle(cases)
key=(R/'01_BLIND_ANSWER_KEY.md').read_text('utf8')
assert all(f'| {i:02} | {n} | {p} | {f} |' in key for i,(n,p,f) in enumerate(cases,1))
# Manifest covers every file except itself and must not leak the drawing
manifest=(R/'SHA256SUMS.txt');assert manifest.is_file()
checks={}
for line in manifest.read_text('utf8').splitlines():
 sha,name=line.split('  ',1);f=R/name
 assert f.is_file() and name not in checks
 assert hashlib.sha256(f.read_bytes()).hexdigest()==sha,name+' hash mismatch'
 checks[name]=sha
allfiles={f.name for f in R.iterdir() if f.is_file() and f.name!='SHA256SUMS.txt'}
assert allfiles==set(checks),(allfiles-set(checks),set(checks)-allfiles)
assert not any(name.lower().endswith(('.jpg','.jpeg')) or 'ORIGINAL_HANDDRAWN' in name.upper() for name in checks)
print('PASS SOURCE/PACKAGE: 2 new families, frozen U1, 8x12, 2 poses, 2 mirror facings, 12 native PNG, 6 GIF, 4x4 bit audit,',len(checks),'file checksums. NOT STELLA OR AESTHETIC PASS')
