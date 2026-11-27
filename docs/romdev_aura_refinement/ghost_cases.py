"""Directed setups and controller checks on the actual Stella Libretro core."""
import ctypes as C
import json
import sys
from pathlib import Path
from PIL import Image

core_file, rom_file, side, output = sys.argv[1:]
out = Path(output)
out.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0], core_file, rom_file, '', '1', output]
frontend = Path(__file__).with_name('capture.py').read_text().split('changes={}')[0]
frontend = frontend.replace(' if data:\n  if vid is None:', ' if False:\n  if vid is None:')
frontend = frontend.replace(' if last is not None:', ' if False:')
frontend = frontend.replace(' global vid,last,frames,error\n',' global vid,last,frames,error,raw_frame,raw_size\n if data:\n  raw_size=(w,h); data_bytes=C.string_at(data,pitch*h); raw_frame=b"".join(data_bytes[y*pitch:y*pitch+w*4] for y in range(h))\n')
exec(frontend)

candidate = side == 'candidate'
result = {'rom':rom_file}
def state():
    return C.string_at(ram,128)
def write(a,*values):
    for i,v in enumerate(values):
        C.c_uint8.from_address(ram+a+i-128).value=v
def step(n=1):
    for _ in range(n): core.retro_run()
    return state()
def screen(path):
    Image.frombytes('RGB',raw_size,raw_frame,'raw','BGRX').save(out/path)
def boot():
    keys.clear()
    keys[3]=1
    step(3)
    keys.clear()
    step(8)
def setup(level, pos=(80,88)):
    boot()
    write(0x80,*pos,level)
    write(0x9c,0)
    write(0x9e,0,0)
    write(0xa3,0,0)
    write(0x85,0)
    write(0xbf,0)
    write(0xb3,0)
    write(0xb4,0,3)
    write(0xd0,*([0]*32))
    write(0xec,0,0xfa)
    write(0xc0,*[16,48,6,48,112,144,6,48,16,48,120,164,112,144,120,164])
def hit():
    keys[0]=1
    s=step()
    keys[0]=0
    return s
def trace(s):
    return [s[0x55],s[0x5c],s[0x63],s[0x1e],s[0x1f],s[0x2e],s[0x52],s[0x59],s[0x23]]

import numpy as np
import collections
import json
rows=[]
for l in (1,2,3):
 for phase in (0,1):
  setup(l); step(3); write(0x8d,phase); write(0xb4,2,3); write(0xde,84,88,0,0,255,1); keys[0]=1
  seq=[]
  for i in range(101):
   t=step(); keys[0]=0
   pix=np.asarray(Image.frombytes('RGB',raw_size,raw_frame,'raw','BGRX')); gold=np.all(pix==[234,194,84],2); silver=np.all(pix==[234,234,233],2);gold[:23]=False;gold[206:]=False;silver[:23]=False;silver[206:]=False
   yy,xx=np.where(gold); box=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())] if len(xx) else None
   r=dict(i=i,level=int(t[2]),framecount=int(t[13]),height=int(t[8]),halo=int(t[30]),pause=int(t[62]),ranger=int(t[99]),k1=int(t[85]),k2=int(t[92]),enemy_bottom=int(t[104]),p1height=int(t[39]),gold=int(gold.sum()),silver=int(silver.sum()),goldbox=box)
   seq.append(r)
   if i<18 or i in (25,50,75,89,90,91,92,100):screen(f'L{l}-p{phase}-{i:03}.png')
  clear=[r for r in seq if 0<r['pause']<78 and r['halo']==0 and r['height'] in (12,20,30)]
  rows.append(dict(level=l,phase=phase,kill=next((r['i'] for r in seq if r['ranger']==0),None),pauseframes=len(clear),ghostframes=sum(r['gold']>0 for r in clear),stale_p1=sum(r['enemy_bottom']!=200 for r in clear),sequence=seq))
(out/'ghost_cases.json').write_text(json.dumps(rows,indent=2));print([{k:v for k,v in row.items() if k!='sequence'} for row in rows]);pcm.close();core.retro_unload_game()
