#!/usr/bin/env python3
"""GRAPHICS P1 SOURCE TESTS ONLY. Not ROM/Stella/independent verification."""
from pathlib import Path
from PIL import Image
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
s=json.loads((R/'SKRAUN_P1_PIXEL_MASKS.json').read_text(encoding='utf-8'))
assert set(s['candidates'])=={'A_rounded_back','B_low_long_back'}
for k,v in s['candidates'].items():
 for pose in ('A','B'):
  rows=v[pose]
  assert len(rows)==12 and all(len(r)==8 and set(r)<={'0','1'} for r in rows)
  assert v['left_'+pose]==[r[::-1] for r in rows],(k,pose,'horizontal mirror')
  # Head right, two negative eyes in head, right boundary and explicit front/rear paw anchors.
  assert rows[5][7]=='1' and rows[7][7]=='1',(k,'snout-right')
  assert rows[5][6]=='0' and rows[7][6]=='0',(k,'two eye holes')
  # Check separated anatomical stations in UPPER and LOWER regions.
  for ys in ([1,2],[9,10]):
   assert any(rows[y][x]=='1' for y in ys for x in [0,1,2]),(k,pose,'rear paw')
   assert any(rows[y][x]=='1' for y in ys for x in [4,5,6]),(k,pose,'fore paw')
  # Mouth omitted; do not silently claim it in image.
 diff=[(x,y) for y in range(12) for x in range(8) if v['A'][y][x]!=v['B'][y][x]]
 assert len(diff)==v['pose_diff_pixels'] and len(diff)>=6,(k,'A/B movement')
 assert any(y in [0,1,2] for x,y in diff) and any(y in [9,10,11] for x,y in diff),(k,'upper+lower gait')
 assert v['left_A']!=v['left_B'],k
for fn in R.glob('*.png'):
 with Image.open(fn) as im: im.verify()
for fn in R.glob('*.gif'):
 with Image.open(fn) as im: assert im.n_frames==2;im.verify()
lines=(R/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines()
listed=set()
for line in lines:
 sha,name=line.split('  ',1)
 path=R/name
 assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==sha,name
 listed.add(name)
assert listed=={p.name for p in R.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt'}
print('PASS graphics-only P1: exact 8x12, head-right, eye gaps, four paw zones, 2-frame step, row mirrors, images, GIFs and SHA-256 manifest')
