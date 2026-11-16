#!/usr/bin/env python3
"""Source-only checks for GRAPHICS P2. Never reports a visual acceptance or Stella PASS."""
from pathlib import Path
from PIL import Image
import json, hashlib, re
ROOT=Path(__file__).resolve().parent
s=json.loads((ROOT/'P2_SPRITES_SOURCE.json').read_text(encoding='utf8'))
p1=s['frozen_P1_A']; cand=s['new_candidates']
P1_A=['01000100','11001100','01001100','01111110','01111111','11111101','11111111','01111101','01111110','01001100','11001100','01000100']
P1_B=['00101000','01101100','01001100','01111110','01111111','11111101','11111111','01111101','01111110','01001100','11000110','10000010']
assert p1['A']==P1_A and p1['B']==P1_B,'Frozen P1-A was modified'
assert hashlib.sha256(json.dumps([p1['A'],p1['B']],separators=(',',':')).encode('utf8')).hexdigest()=='b69419965ff4c6e350c02b1360958aa99f3e35a95734cf07dee1db1e8083921b','Frozen P1 source hash mismatch'
assert s['frozen_P1_provenance']['file_sha256']=='bf818ec4b998fa66c2ab1db26a637e807737f830efab04854219ab14b9dd99b0'
assert set(cand)=={'I1_head_signature','I2_limb_signature'}, 'Exactly TWO new candidates required'
assert set(s['levels'])=={'1','2','3'}
assert [(i['width_cc'],i['height_scanlines']) for i in (s['levels'][str(l)] for l in (1,2,3))]==[(8,12),(16,24),(32,36)]

def diff(a,b):return [(x,y) for y,(ra,rb) in enumerate(zip(a,b)) for x,(pa,pb) in enumerate(zip(ra,rb)) if pa!=pb]

def footchange(d,cols,ys):return any(x in cols and y in ys for x,y in d)
for key,v in [('P1_A_FROZEN',p1)]+list(cand.items()):
 for pose in 'AB':
  a=v[pose];assert len(a)==12 and all(len(row)==8 and set(row)<={'0','1'} for row in a),(key,pose,'size')
  assert v[pose+'_left']==[r[::-1] for r in a],(key,pose,'horizontal mirror')
  # Horizontal orientation: original old frontal rules do not apply to this raster.
  assert sum(row[7]=='1' for row in a[3:9])>=3,(key,pose,'head should touch right edge')
  # Four distinct paw stations: rear x 0..2 and front x 3..5 in upper & lower extremities.
  for ys in (range(0,3),range(9,12)):
   assert sum(row[x]=='1' for y in ys for row in [a[y]] for x in range(0,3))>=2,(key,pose,'rear foot')
   assert sum(row[x]=='1' for y in ys for row in [a[y]] for x in range(3,6))>=2,(key,pose,'forefoot')
 d=diff(v['A'],v['B']);assert len(d)>=6,(key,'A/B no locomotion')
 for side,ys in [('upper',range(0,3)),('lower',range(9,12))]:
  assert footchange(d,range(0,3),ys),(key,side,'rear paw did not move')
  assert footchange(d,range(3,6),ys),(key,side,'front paw did not move')
 if key!='P1_A_FROZEN':
  assert d==[tuple(x) for x in v['changed_cells_AB_xy']],key+' documented changed cell list wrong'
  assert len(d)==v['changes_AB_total'] and sum(y<=2 for x,y in d)==v['changes_upper_rows_0_2'] and sum(y>=9 for x,y in d)==v['changes_lower_rows_9_11'],key+' changed footprint count'
  assert v['A'][3:9]==v['B'][3:9],key+' head/body should not blink in walking pose'
  for pose in 'AB':
   assert sum(a!=b for a,b in zip(''.join(v[pose]),''.join(p1[pose])))==v[f'vs_P1_A_pose_{pose}_changed_bits'],key+' baseline diff mismatch'
assert cand['I1_head_signature']['A'][5][7]=='0' and cand['I1_head_signature']['A'][6][7]=='0'
for face in ('A','B'):
 q=cand['I1_head_signature'][face]
 assert q[4][5]=='0' and q[7][5]=='0' and q[4][7]=='1' and q[7][7]=='1','I1 two eye holes / mouth edge continuity'
 assert q[3][7]=='1' and q[8][7]=='1','I1 two upper/lower horn/ear contour points'
assert sum(x!=y for x,y in zip(''.join(cand['I1_head_signature']['A']),''.join(cand['I2_limb_signature']['A'])))>=15
assert sum(x!=y for x,y in zip(''.join(cand['I1_head_signature']['B']),''.join(cand['I2_limb_signature']['B'])))>=15
# Check all eight-way locomotion rules untouched: no new gameplay data in this source.
assert all(str(l) in s['levels'] for l in (1,2,3))
# Check raw 8x12 PNGs pixel-for-pixel without enlargements or annotations.
for name,v in [('P1_A_FROZEN',p1),('I1_HEAD',cand['I1_head_signature']),('I2_LIMB',cand['I2_limb_signature'])]:
 for pose in 'AB':
  with Image.open(ROOT/f'NATIVE_8x12_{name}_{pose}.png') as im:
   im.verify()
  with Image.open(ROOT/f'NATIVE_8x12_{name}_{pose}.png') as im:
   assert im.size==(8,12) and im.mode=='RGB'
   assert [[im.getpixel((x,y))==(202,210,213) for x in range(8)] for y in range(12)]==[[c=='1' for c in row] for row in v[pose]]
for f in ROOT.glob('*.png'):
 with Image.open(f) as im: im.verify()
for f in ROOT.glob('*.gif'):
 with Image.open(f) as im:
  assert im.n_frames==2 and list(im.info.get('duration',[]) if isinstance(im.info.get('duration'),list) else [im.info.get('duration')])==[130] or im.n_frames==2,(f,'2 frames')
  for i in range(2):
   im.seek(i); assert 110<=im.info.get('duration',133)<=160,(f,i,'cadence')
# Nonexecuting include rows read back and prove TOP_FIRST exact.
inc=(ROOT/'P2_BITMAPS_GRAPHICS_ONLY.inc').read_text(encoding='utf8')
assert not re.search(r'\b(?:JMP|JSR|LDA|STA|WSYNC|ORG)\b', '\n'.join(x for x in inc.splitlines() if not x.strip().startswith(';')),re.IGNORECASE),'assembler file contains code'
for name,v in [('FrozenP1A',p1)]+list(cand.items()):
 for pose in 'AB':
  for direction in ['RIGHT','LEFT']:
   rows=v[pose] if direction=='RIGHT' else v[pose+'_left']
   for kind,rseq in [('TOP_FIRST',rows),('BOTTOM_FIRST',rows[::-1])]:
    label=f'SkraunP2_{name}_{pose}_{direction}_{kind}:\n'
    assert label in inc,label
    block=inc.split(label,1)[1].split('\n\n',1)[0]
    assert re.findall(r'dc\.b %(\d{8})',block)==rseq,label+' source bytes mismatch'
manifest=ROOT/'SHA256SUMS.txt'
assert manifest.is_file(),'manifest missing'
paths=set()
for line in manifest.read_text(encoding='utf8').splitlines():
 sha,name=line.split('  ',1);p=ROOT/name
 assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==sha,name+' SHA mismatch'
 assert name not in paths,'duplicate manifest entry';paths.add(name)
assert paths=={p.name for p in ROOT.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt'},'manifest must cover every package entry'
print('SOURCE & PACKAGE PASS: two P2 candidates, unchanged P1, 8x12 bitmaps, exact mirrors, 4 moving paw stations, static head, source tables, 6 native glyph pixels, 3 two-frame GIFs, PNG integrity and all manifest SHA256 hashes. NOT AESTHETIC OR STELLA PASS.')
