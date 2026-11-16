#!/usr/bin/env python3
"""Independent deterministic source-art and asset integrity tests. NOT Atari/Stella verification."""
import json,hashlib,zipfile
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent
s=json.loads((R/'SKRAUN_V03.json').read_text(encoding='utf-8'))
e=json.loads((R/'ENEMIES_V03.json').read_text(encoding='utf-8'))
w=json.loads((R/'WORLDS_V03.json').read_text(encoding='utf-8'))
h=json.loads((R/'HALO_V03.json').read_text(encoding='utf-8'))

def valid(rows,length):
 assert len(rows)==length, (len(rows),length)
 assert all(len(r)==8 and set(r)<=set('01') for r in rows),rows

def count(a,b,indices):return sum(c!=d for i in indices for c,d in zip(a[i],b[i]))
for name,p in s['new_attempts'].items():
 a,b=p['A'],p['B'];valid(a,12);valid(b,12)
 assert p['left_A']==[r[::-1] for r in a] and p['left_B']==[r[::-1] for r in b],name
 for seq in (a,b):
  assert seq[0][2]=='1' and seq[0][5]=='1',name+' missing horns'
  assert sum(c=='1' for c in seq[1])>=4,name+' missing head'
  assert seq[11]!=seq[0],name+' head versus rear paws indistinct'
  assert any(c=='1' for r in seq[9:] for c in r[:2]),name+' left rear foot missing'
  assert any(c=='1' for r in seq[9:] for c in r[6:]),name+' right rear foot missing'
 assert count(a,b,[5,6])>=4 and count(a,b,[9,10,11])>=4,name+' inadequate A/B limb movement'
 assert count(a,b,range(12))>=10,name+' too few overall movement pixels'
for k,rs in e['sprites'].items():valid(rs,12)
for c1,c2 in [('knight_idle','knight_warning'),('archer_idle','archer_draw')]:
 assert count(e['sprites'][c1],e['sprites'][c2],range(12))>=10,(c1,c2)
assert set(w['layouts'])=={'forest','mountain','dream','night'}
for theme,levels in w['layouts'].items():
 assert set(levels)=={'1','2'},theme
 for lab,rows in levels.items():
  assert len(rows)==24 and all(len(r)==40 and set(r)<=set('01') and r==r[::-1] for r in rows),(theme,lab)
  assert 0.015<sum(r.count('1') for r in rows)/960<0.28,(theme,lab,'sparse PF occupancy')
for k,d in h['levels'].items():
 rows=d['mask'];assert len(rows)==24 and all(len(r)==40 and set(r)<=set('01') and r==r[::-1] for r in rows),k
 assert rows==rows[::-1],k
 loc=[(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='1']
 width=4*(max(x for x,y in loc)-min(x for x,y in loc)+1)
 height=8*(max(y for x,y in loc)-min(y for x,y in loc)+1)
 assert (width,height)==(d['metrics']['cc_width'],d['metrics']['scanline_height']),k
 assert abs(1.6*width/height-1)<=0.15,k+' not circular under 4:3 assumption'
assert [h['levels'][str(i)]['metrics']['cc_width'] for i in (1,2,3)]==[40,56,72]
assert [h['levels'][str(i)]['metrics']['scanline_height'] for i in (1,2,3)]==[64,80,112]
for path in R.glob('*.png'):
 with Image.open(path) as im: im.verify()
for path in R.glob('*.gif'):
 with Image.open(path) as im:
  assert im.n_frames==2,(path,im.n_frames)
  im.verify()
manifest=R/'SHA256SUMS.txt'
if manifest.exists():
 lines=manifest.read_text(encoding='utf-8').splitlines()
 filenames=[]
 for line in lines:
  sha,name=line.split('  ',1);fp=R/name
  assert fp.is_file(),name
  assert hashlib.sha256(fp.read_bytes()).hexdigest()==sha,name
  filenames.append(name)
 assert set(filenames)=={p.name for p in R.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt'},'not all files covered'
print('PASS: all Skraun rows, anatomical anchors, mirrored facings, A/B limbs, knight and archer warning, 8 PF layouts, 4:3 ring footprints, 4 two-frame GIFs, PNG decode and manifest (if present).')
