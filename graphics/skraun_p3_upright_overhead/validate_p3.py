#!/usr/bin/env python3
"""GRAPHICS P3 - deterministic source and package test. NOT aesthetic, ROM or Stella verification."""
from pathlib import Path
from PIL import Image
import json,hashlib,re
R=Path(__file__).resolve().parent
S=json.loads((R/'P3_SOURCE_BITMAPS.json').read_text(encoding='utf8'))
assert set(S['new_candidates'])=={'U1_upright_face_priority','U2_upright_body_priority'},'Exactly 2 new sprites'
assert set(S['controls'])=={'Q1_prior_best_upright','P1_A_negative_prone'}
assert len(S['conceptual_sizes'])==3
assert [(S['conceptual_sizes'][str(i)]['width_color_clocks'],S['conceptual_sizes'][str(i)]['height_scanlines']) for i in (1,2,3)]==[(8,12),(16,24),(32,36)]
Q1_A=['00100100','01111110','01011010','00111100','00111100','11111100','10111111','00111100','00111100','01111110','11011011','10000010']
Q1_B=['00100100','01111110','01011010','00111100','00111100','00111111','11111101','00111100','00111100','01111110','11011011','01000001']
P1_A=['01000100','11001100','01001100','01111110','01111111','11111101','11111111','01111101','01111110','01001100','11001100','01000100']
P1_B=['00101000','01101100','01001100','01111110','01111111','11111101','11111111','01111101','01111110','01001100','11000110','10000010']
assert S['controls']['Q1_prior_best_upright']['A']==Q1_A and S['controls']['Q1_prior_best_upright']['B']==Q1_B
assert S['controls']['P1_A_negative_prone']['A']==P1_A and S['controls']['P1_A_negative_prone']['B']==P1_B
keys=[('Control','Q1_prior_best_upright','Q1_UPRIGHT_REFERENCE'),('Control','P1_A_negative_prone','P1_A_PRONE_NEGATIVE'),('Candidate','U1_upright_face_priority','U1_FACE'),('Candidate','U2_upright_body_priority','U2_BODY')]
inc=(R/'P3_GRAPHICS_ONLY_PIXEL_DATA.inc').read_text(encoding='utf8')
for line in inc.splitlines():
 a=line.strip()
 assert not a or a.startswith(';') or (a.startswith('SkraunP3_') and a.endswith(':')) or re.fullmatch(r'dc\.b %[01]{8}',a),f'Non-art source in .inc: {a}'
for group,name,filename in keys:
 data=S['controls'][name] if group=='Control' else S['new_candidates'][name]
 for pose in 'AB':
  rs=data[pose]
  assert len(rs)==12 and all(len(r)==8 and set(r)<={'0','1'} for r in rs),(name,pose,'8x12')
  assert data[pose+'_left']==[r[::-1] for r in rs],(name,pose,'mirror')
  for side in ('RIGHT','LEFT'):
   rows=rs if side=='RIGHT' else data[pose+'_left']
   for order in ('TOP_FIRST','BOTTOM_FIRST'):
    actual=rows if order=='TOP_FIRST' else rows[::-1]
    lab=f'SkraunP3_{group}_{name}_{pose}_{side}_{order}:\n'
    assert lab in inc,lab
    got=re.findall(r'dc\.b %([01]{8})',inc.split(lab,1)[1].split('\n\n',1)[0]);assert got==actual,(lab,'data mismatch')
   with Image.open(R/f'NATIVE_8x12_{filename}_{pose}_{side}.png') as im:
    assert im.size==(8,12) and im.mode=='RGB'
    for y,r in enumerate(rows):
     for x,b in enumerate(r):assert im.getpixel((x,y))==((210,210,209) if b=='1' else (17,25,35)),(name,pose,side,x,y)
 diffs=[(x,y) for y,(ra,rb) in enumerate(zip(data['A'],data['B'])) for x,(a,b) in enumerate(zip(ra,rb)) if a!=b]
 assert len(diffs)==data['A_B_different_cells'] and diffs==[tuple(x) for x in data['changed_cells_xy']],(name,'diff ledger')
 if group=='Candidate':
  assert data['A'][:5]==data['B'][:5],name+' head blinks'
  assert sum(y in (5,6,7) for x,y in diffs)>=3,name+' arms static'
  assert sum(y in (9,10,11) for x,y in diffs)>=3,name+' legs static'
  assert any(x<=1 for x,y in diffs if y in (5,6,7)) and any(x>=6 for x,y in diffs if y in (5,6,7)),name+' both arms'
  assert any(x<=2 for x,y in diffs if y in (9,10,11)) and any(x>=4 for x,y in diffs if y in (9,10,11)),name+' both feet'
  assert all(data[pose][0][2]==data[pose][0][5]=='1' for pose in 'AB'),name+' two horns'
  assert all(data[pose][11].count('1')>=3 for pose in 'AB'),name+' feet'
  q=S['controls']['Q1_prior_best_upright'];p=S['controls']['P1_A_negative_prone']
  for pose in 'AB':
   assert sum(a!=b for a,b in zip(''.join(data[pose]),''.join(q[pose])))==data['vs_Q1_changed_bits'][pose]
   assert sum(a!=b for a,b in zip(''.join(data[pose]),''.join(p[pose])))==data['vs_P1_changed_bits'][pose]
# U1 face, negative eyes and enclosed mouth. Is a bit-pattern check, NOT a perceptual acceptance.
u=S['new_candidates']['U1_upright_face_priority']
for pose in 'AB':
 assert u[pose][2][2]==u[pose][2][5]=='0'
 assert u[pose][3][3]==u[pose][3][4]=='0'
 assert u[pose][4][3]==u[pose][4][4]=='1'
other=S['new_candidates']['U2_upright_body_priority']
for pose in 'AB':
 assert sum(a!=b for a,b in zip(''.join(u[pose]),''.join(other[pose])))==S['U1_vs_U2_changed_bits'][pose]
 assert S['U1_vs_U2_changed_bits'][pose]>=18
assert len(list(R.glob('NATIVE_8x12_*.png')))==16
for png in R.glob('*.png'):
 with Image.open(png) as im:im.verify()
assert len(list(R.glob('GIF_*.gif')))==6
for gif in R.glob('GIF_*.gif'):
 with Image.open(gif) as im:
  assert im.n_frames==2,gif
  for i in range(2):
   im.seek(i);assert im.info.get('duration')==140,(gif,im.info.get('duration'))
assert (R/'SHA256SUMS.txt').exists()
entries=set()
for line in (R/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
 sha,name=line.split('  ',1);fn=R/name
 assert fn.is_file() and name not in entries
 assert hashlib.sha256(fn.read_bytes()).hexdigest()==sha,name
 entries.add(name)
assert entries=={f.name for f in R.iterdir() if f.is_file() and f.name!='SHA256SUMS.txt'},'missing file in manifest'
assert all('ORIGINAL_HANDDRAWN_REFERENCE' not in name and not name.lower().endswith(('.jpg','.jpeg')) for name in entries),'private original leaked'
print(f'PASS SOURCE/PACKAGE ONLY: two new 8x12, {len(entries)} SHA256-verified files, frozen source controls, mirrors, limbs, 16 native bitmaps, 6 GIFs. NO AESTHETIC/STELLA PASS.')
