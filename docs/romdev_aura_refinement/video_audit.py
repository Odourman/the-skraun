"""Decode every frame from delivered 60fps MP4 and join to same-run RIOT.
Palette tolerant due to H264 chroma; exact sprite/pixel fixtures are separate.
Uses actual rendered SpriteHeight, rather than overscan's next HaloFrames.
"""
import argparse, subprocess, numpy as np, json, csv
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('riot');p.add_argument('out');p.add_argument('--version',choices=['B3','R1','R2'],required=True);a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
s=np.fromfile(a.riot,dtype=np.uint8).reshape(-1,128);heights=(24,40,60) if a.version=='B3' else (21,35,52); widths=(16,32,64) if a.version=='B3' else (14,28,56)
proc=subprocess.Popen(['ffmpeg','-v','error','-i',a.video,'-vf','scale=160:228:flags=neighbor','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
yy,xx=np.indices((228,160));arena=(yy>=23)&(yy<206)
rows=[]; suspects={}; phase_runs=[]
for i,state in enumerate(s):
 data=proc.stdout.read(160*228*3)
 if len(data)!=160*228*3:raise RuntimeError(f'decoded only {i} frames')
 img=np.frombuffer(data,dtype=np.uint8).reshape(228,160,3).astype(np.int16);r,g,b=img.transpose(2,0,1);prev=s[max(i-1,0)]
 # Colour masks for compressed video, thresholds exclude dark/white and actual world palette.
 gold=(r>170)&(g>125)&(b<150)&(r-g>12)&(g-b>42)&arena
 silver=(r>90)&(g>90)&(b>90)&(np.maximum(np.maximum(r,g),b)-np.minimum(np.minimum(r,g),b)<23)&arena
 blue=(b>200)&(g>140)&(r>70)&(b-r>65)&arena
 strike=(r>165)&(g<125)&(b<150)&(r-g>60)&arena
 x,y,l=map(int,state[:3]);l=int(l);h=int(state[8]);actual_level=next((j+1 for j,hs in enumerate(zip((12,20,30),heights)) if h in hs),l if l in (1,2,3) else 1)
 is_aura=h==heights[actual_level-1];pause=int(state[62]);dead=not (state[85] or state[92] or state[99]&1);stable_pause=dead and 0<pause<90 and int(prev[62])>0
 # Center from the measured native rendering; width and height margins allow encoding and overscan relocation.
 cx=x-3 if actual_level==1 else x-2.5;cy=y+30.5
 bounds=(abs(xx-cx)<=widths[actual_level-1]/2+3)&(abs(yy-cy)<=heights[actual_level-1]/2+4)
 bodybounds=(abs(xx-cx)<=(4,8,16)[actual_level-1]+4)&(abs(yy-cy)<=(6,10,15)[actual_level-1]+4)
 # Position changed by respawn / stage transition in overscan: do not assert exact box.
 stable_pos=abs(int(prev[0])-x)<=1 and abs(int(prev[1])-y)<=1 and prev[42]==state[42] and prev[44]==state[44]
 gold_n=int(gold.sum()); silver_n=int(silver.sum()); gold_far=int((gold&~bounds).sum());blue_n=int(blue.sum());strike_n=int(strike.sum())
 ghost=bool(stable_pause and not is_aura and gold_n>8)
 pause_extra=bool(stable_pause and is_aura and stable_pos and gold_far>8)
 pause_other=bool(stable_pause and blue_n>12) # night terrain can be blue: retain only as diagnostic
 body_missing=bool(i>12 and state[44] and stable_pos and not is_aura and int((silver&bodybounds).sum())<8 and not state[51])
 aura_missing=bool(i>12 and state[44] and is_aura and stable_pos and int((gold&bounds).sum())<10)
 parity_error=bool(is_aura and int(state[13])%2!=1)
 # Knight palette sizes: more than 2*8*16 pixels is impossible for 2 normal P1 copies.
 oversized_blue=bool(blue_n>2*8*16+40 and prev[42] in (1,2,5,6))
 row=dict(frame=i,seconds=round(i/60,4),level=l,render_level=actual_level,stage=int(state[42]),parity=int(state[13])%2,halo=int(state[30]),height=h,pause=pause,dead=bool(dead),stable_pause=bool(stable_pause),render_aura=bool(is_aura),gold_pixels=gold_n,gold_outside_aura=gold_far,silver_pixels=silver_n,blue_pixels=blue_n,strike_pixels=strike_n,ghost=ghost,pause_extra_gold=pause_extra,body_missing=body_missing,aura_missing=aura_missing,parity_error=parity_error,oversized_blue=oversized_blue)
 rows.append(row)
 for k in ('ghost','pause_extra_gold','body_missing','aura_missing','parity_error','oversized_blue'):
  if row[k]:
   found=suspects.setdefault(k,[]);found.append(i)
   if len(found)<=6:Image.fromarray(img.astype('uint8')).save(out/f'{k}-{i:05}.png')
if proc.stdout.read(1):raise RuntimeError('extra decoded frames')
assert proc.wait()==0
with (out/'frames.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary=dict(decoded=len(rows),ram_frames=len(s),aura=sum(r['render_aura'] for r in rows),stable_dead_pause=sum(r['stable_pause'] for r in rows),stable_dead_pause_no_aura=sum(r['stable_pause'] and not r['render_aura'] for r in rows),adjacent_aura=sum(rows[i]['render_aura'] and rows[i-1]['render_aura'] for i in range(1,len(rows))),flags={k:{'count':len(v),'first':v[:12],'last':v[-1]} for k,v in suspects.items()})
(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
