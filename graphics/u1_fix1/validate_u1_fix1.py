#!/usr/bin/env python3
"""Validate U1-FIX1 source and package; never assert human facing/identity or Stella correctness."""
from pathlib import Path
import json,re,hashlib
from PIL import Image
R=Path(__file__).resolve().parent
s=json.loads((R/'U1_FIX1_BITMAPS.json').read_text('utf8'))
old=s['frozen_U1'];new=s['single_corrected_U1_FIX1']
assert s['rules']['columns']==8 and s['rules']['rows']==12
assert set(old)==set(new)=={'A','B','A_left','B_left'}
canonA=['00100100','01111110','01011010','01100111','00111110','11111110','10111100','00111100','00111100','01100110','01000110','11000011']
canonB=['00100100','01111110','01011010','01100111','00111110','01111111','00111101','00111100','00111100','01100110','01100010','11000001']
assert old['A']==canonA and old['B']==canonB,'frozen U1 altered'
flip=lambda a:[x[::-1] for x in a]
for z in (old,new):
 for p in 'AB':
  assert len(z[p])==12 and all(len(r)==8 and set(r)<={'0','1'} for r in z[p])
  assert z[p+'_left']==flip(z[p]),'horizontal mirror invalid'
def diff(a,b):return [[x,y] for y,(v,w) in enumerate(zip(a,b)) for x,(i,j) in enumerate(zip(v,w)) if i!=j]
assert diff(old['A'][:5],new['A'][:5])==[[7,3]]
assert diff(old['B'][:5],new['B'][:5])==[[7,3]]
assert new['A'][5]=='01111111' and new['B'][6]=='01111101' and new['B'][11]=='10000011'
assert diff(old['A'],new['A'])==s['changes']['pose_A_changed_cells_xy']
assert diff(old['B'],new['B'])==s['changes']['pose_B_changed_cells_xy']
assert len(diff(new['A'],new['B']))>=4
assert any(y in (5,6) for x,y in diff(new['A'],new['B']))
assert any(y in (10,11) for x,y in diff(new['A'],new['B']))
inc=(R/'U1_FIX1_ART_DATA_ONLY.inc').read_text('utf8')
for ln in inc.splitlines():
 x=ln.strip(); assert not x or x.startswith(';') or (x.startswith('Skraun_U1_FIX1_') and x.endswith(':')) or re.fullmatch(r'dc\.b %[01]{8}',x),f'illegal non-art line {x}'
for p in 'AB':
 for facing in ('RIGHT','LEFT'):
  target=new[p] if facing=='RIGHT' else new[p+'_left']
  for order in ('TOP_FIRST','BOTTOM_FIRST'):
   label=f'Skraun_U1_FIX1_{p}_{facing}_{order}:\n'
   block=inc.split(label,1)[1].split('\n\n',1)[0]
   bits=re.findall(r'dc\.b %([01]{8})',block)
   assert bits==(target if order=='TOP_FIRST' else target[::-1]),label
  raw=R/f'U1_FIX1_NATIVE_8x12_{p}_{facing}.png';assert raw.exists()
  with Image.open(raw) as im:
   assert im.size==(8,12) and im.mode=='RGB'
   for y,row in enumerate(target):
    for x,b in enumerate(row):assert im.getpixel((x,y))==((210,210,209) if b=='1' else (11,20,37))
for fn in R.glob('*.png'):
 with Image.open(fn) as im:im.verify()
assert len(list(R.glob('U1_FIX1_NATIVE_8x12_*.png')))==4
assert len(list(R.glob('GIF_*.gif')))==2
for fn in R.glob('GIF_*.gif'):
 with Image.open(fn) as im:
  assert im.size==(240,164) and im.n_frames==2
  for i in (0,1): im.seek(i);assert im.info['duration']==180
assert len(list(R.glob('*.png')))==10 # 4 raw + 6 preview sheets
assert not any(x.suffix.lower() in ('.jpg','.jpeg') for x in R.iterdir())
manifest=R/'SHA256SUMS.txt';assert manifest.exists()
found=set()
for line in manifest.read_text('utf8').splitlines():
 dig,name=line.split('  ',1);file=R/name
 assert file.is_file() and name not in found
 assert hashlib.sha256(file.read_bytes()).hexdigest()==dig,name+' changed'
 found.add(name)
assert found=={x.name for x in R.iterdir() if x.is_file() and x.name!='SHA256SUMS.txt'}
print('PASS U1-FIX1: one family; head ONE bit; arms/feet targeted; 8x12, two poses, exact mirrors, 4 raw PNG, 6 design panels, 2 GIF, manifest',len(found),'files. VISUAL DIRECTION NOT PROVEN.')
