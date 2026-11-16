#!/usr/bin/env python3
"""GRAPHICS P3-F1 reproducibility + source hygiene; NOT human aesthetic/STELLA acceptance."""
from pathlib import Path
import json, hashlib, re
from PIL import Image
R=Path(__file__).resolve().parent
S=json.loads((R/'P3_F1_SOURCE_BITMAPS.json').read_text(encoding='utf-8'))
assert set(S['new_candidates'])=={'D1_face_ear_permanent','D2_shoulder_arm_permanent'}
assert set(S['frozen_control'])=={'U1_frozen'}
assert set(S['conceptual_levels'])=={'1','2','3'}
assert [(S['conceptual_levels'][str(i)]['width_color_clocks'],S['conceptual_levels'][str(i)]['scanline_height']) for i in (1,2,3)] == [(8,12),(16,24),(32,36)]
assert S['conventions']['width_bits']==8 and S['conventions']['height_rows']==12
baselineA=['00100100','01111110','01011010','01100111','00111110','11111110','10111100','00111100','00111100','01100110','01000110','11000011']
baselineB=['00100100','01111110','01011010','01100111','00111110','01111111','00111101','00111100','00111100','01100110','01100010','11000001']
U=S['frozen_control']['U1_frozen']
assert U['A']==baselineA and U['B']==baselineB,'Frozen U1 changed'
def canon(a,b):return hashlib.sha256(json.dumps([a,b],separators=(',',':')).encode()).hexdigest()
assert S['baseline']['A_B_rows_canonical_sha256']==canon(baselineA,baselineB)
assert S['baseline']['sha256_of_exact_baseline_json']=='72ebc4dc58200f2761e942b5d6c21ac8e0308fba368d15d976715c850056450f'

def dd(a,b):return [[x,y] for y,(ra,rb) in enumerate(zip(a,b)) for x,(aa,bb) in enumerate(zip(ra,rb)) if aa!=bb]
def h(a,b):return len(dd(a,b))
def four(v):
 z=[v['A'],v['A_left'],v['B'],v['B_left']]
 return [[h(a,b) for b in z] for a in z]
inc=(R/'P3_F1_GRAPHICS_ONLY_DATA.inc').read_text('utf-8')
for line in inc.splitlines():
 q=line.strip()
 assert not q or q.startswith(';') or (q.startswith('SkraunP3F1_') and q.endswith(':')) or re.fullmatch(r'dc\.b %[01]{8}',q),f'Unexpected non-art code: {q}'
items={'U1_frozen':U,**S['new_candidates']}
for name,v in items.items():
 for pose in 'AB':
  bits=v[pose]
  assert len(bits)==12 and all(len(row)==8 and set(row)<={'0','1'} for row in bits),(name,pose,'bad 8x12')
  assert v[pose+'_left']==[r[::-1] for r in bits],(name,pose,'mirror changed')
  for facing in ('RIGHT','LEFT'):
   rows=bits if facing=='RIGHT' else v[pose+'_left']
   for order in ('TOP_FIRST','BOTTOM_FIRST'):
    a=rows if order=='TOP_FIRST' else rows[::-1]
    label=f'SkraunP3F1_{name}_{pose}_{facing}_{order}:\n'
    assert label in inc
    found=re.findall(r'dc\.b %([01]{8})',inc.split(label,1)[1].split('\n\n',1)[0])
    assert found==a,(label,'include mismatch')
   imagefile=R/f'NATIVE_8x12_{name[:2] if name != "U1_frozen" else "U1"}_{pose}_{facing}.png'
   # source image naming: D1/D2 first two chars, U1 first two chars
   assert imagefile.is_file(),imagefile
   with Image.open(imagefile) as im:
    assert im.size==(8,12) and im.mode=='RGB'
    im.verify()
   with Image.open(imagefile) as im:
    for y,row in enumerate(rows):
     for x,c in enumerate(row):assert im.getpixel((x,y))==((210,210,209) if c=='1' else (17,25,35)),(name,pose,facing,x,y)
 assert v['A_B_changed_cells_xy']==dd(v['A'],v['B']) and v['A_B_changes']==h(v['A'],v['B'])
 assert v['original_hash_A_B']==canon(v['A'],v['B'])
 if name!='U1_frozen':
  assert v['A'][:5]==v['B'][:5],name+' face/horns are blinking'
  assert any(y in (5,6) for x,y in dd(v['A'],v['B'])) and any(y in (10,11) for x,y in dd(v['A'],v['B']))
  assert v['vs_original_U1_changes']=={p:h(v[p],U[p]) for p in 'AB'}
assert S['new_candidates']['D1_face_ear_permanent']['A'][0][2]=='1'
assert S['new_candidates']['D1_face_ear_permanent']['A'][0][6]=='1'
for p in 'AB':
 rows=S['new_candidates']['D1_face_ear_permanent'][p]
 assert rows[2][2]=='0' and rows[2][5]=='0'
 assert all(rows[y][3]==rows[y][4]=='0' for y in (3,4))
 d2=S['new_candidates']['D2_shoulder_arm_permanent'][p]
 assert d2[:4]==U[p][:4] # U1 head/eye/mouth unchanged
assert all(S['new_candidates']['D2_shoulder_arm_permanent']['A'][y]==S['new_candidates']['D2_shoulder_arm_permanent']['B'][y] for y in (4,7,8))
# Blinded answer key, 12 unique samples, source numbering verified against deterministic seed.
import random
blind=[(n,p,f) for n in items for p in 'AB' for f in ('RIGHT','LEFT')]
random.Random(S['preview']['blind_seed']).shuffle(blind)
key=(R/'01_BLIND_ANSWER_KEY.md').read_text('utf-8')
for i,(n,p,f) in enumerate(blind,1):
 assert f'| {i:02d} | {n[:2]} | {p} | {f} |' in key,(i,n,p,f)
# Independently recompute ledger against all four orientations.
ledger=json.loads((R/'HAMMING_AUDIT.json').read_text('utf-8'))
assert set(ledger['families'])==set(items)
for name,v in items.items():
 audit=ledger['families'][name]
 assert audit['four_case_pairwise_matrix']==four(v)
 assert audit['A_RIGHT__A_LEFT']==h(v['A'],v['A_left'])
 assert audit['B_RIGHT__B_LEFT']==h(v['B'],v['B_left'])
 assert audit['A_RIGHT__B_LEFT']==h(v['A'],v['B_left'])
 assert audit['A_RIGHT__B_RIGHT']==h(v['A'],v['B'])
 assert audit['A_RIGHT__B_RIGHT_HEAD_ONLY_ROWS_0_4']==h(v['A'][:5],v['B'][:5])
assert len(list(R.glob('NATIVE_8x12_*.png')))==12
for p in R.glob('*.png'):
 with Image.open(p) as im:im.verify()
assert len(list(R.glob('GIF_*.gif')))==6
for p in R.glob('GIF_*.gif'):
 with Image.open(p) as gif:
  assert gif.n_frames==2,(p,gif.n_frames)
  for k in range(2):
   gif.seek(k);assert gif.info.get('duration')==140,(p,k,gif.info.get('duration'))
  assert gif.size==(240,164)
assert S['preview']['tv_approx_pixels']==[640,480] and S['preview']['native_screen_cc_scanlines']==[160,192]
manifest=R/'SHA256SUMS.txt';assert manifest.is_file()
names=set()
for line in manifest.read_text('utf-8').splitlines():
 sha,name=line.split('  ',1)
 f=R/name;assert f.is_file() and name not in names
 assert hashlib.sha256(f.read_bytes()).hexdigest()==sha,name+' hash differs'
 names.add(name)
actual={p.name for p in R.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt'}
assert names==actual,('manifest incomplete',sorted(actual-names),sorted(names-actual))
assert not any(p.suffix.lower() in ('.jpg','.jpeg') or 'ORIGINAL_HANDDRAWN' in p.name for p in R.iterdir())
print(f'PASS source/package ONLY. {len(names)} SHA256 entries, EXACTLY 2 new families, frozen U1, all four facings, no extra up/down, 12 native 8x12 PNGs and 6 two-frame GIFs. No perceptual/ROM/Stella pass.')
