#!/usr/bin/python3
"""Developer-run source-independent RGB inspection of actual Stella 320x228 TIA PNG.
A successful diagnostic run is NOT a halo renderer PASS."""
from pathlib import Path
import numpy as np, json, hashlib
from PIL import Image
root=Path("build/play1x/moving")
scenes=["baseline","L1_fire","pickup_L2_off","L2_fire","A_L3_fire","B_L3_x104","C_L3_x112","D_L3_y104","E_L3_wall"]
data={}; masks={}
def bbox(mask):
 ys,xs=np.where(mask)
 if not len(xs):return None
 return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
for name in scenes:
 d=root/name
 pic=d/"DEBUGGER_DESKTOP.png"
 assert pic.exists(),f"Stella image missing {name}"
 src=Image.open(pic).convert("RGB")
 assert src.size==(1400,1000), (name,src.size)
 rgb=np.asarray(src.crop((121,115,441,343)))
 Image.fromarray(rgb).save(d/"ACTUAL_STELLA_TIA.png")
 gray=np.all(rgb==[210,210,209],axis=2)
 blue=np.all(rgb==[121,194,251],axis=2)
 gold=np.all(rgb==[234,194,84],axis=2)
 world=np.all(rgb==[55,61,193],axis=2)
 log=(d/"STELLA.log").read_text()
 fmt=next((s.strip() for s in log.splitlines() if "Display Format:" in s),"NOT AVAILABLE")
 data[name]={"p0_bbox":bbox(gray),"p0_n":int(gray.sum()),"p1_blue_bbox":bbox(blue),"p1_blue_n":int(blue.sum()),"gold_n":int(gold.sum()),"gold_bbox":bbox(gold),"worldblue_n":int(world.sum()),"display":fmt,"RGB_SHA256":hashlib.sha256(rgb.tobytes()).hexdigest()}
 masks[name]=(gold,gray,blue)
 print(name,json.dumps(data[name],ensure_ascii=False))
def gold_diff(a,b):
 g1,p1,q1=masks[a];g2,p2,q2=masks[b]
 active=np.logical_xor(g1,g2)&~(p1|p2|q1|q2)
 return {"unoccluded_changes":int(active.sum()),"bbox":bbox(active)}
pairs=[("A_L3_fire","B_L3_x104"),("B_L3_x104","C_L3_x112"),("A_L3_fire","C_L3_x112"),("B_L3_x104","D_L3_y104")]
results={}
for a,b in pairs:
 k=a+"->"+b;results[k]=gold_diff(a,b)
 print("PIXEL_PAIR",k,json.dumps(results[k]))
for a,b in pairs[:3]:
 # Upper 24..48 arena obstacle row = y55..79 TIA crop, outside halo.
 fixed_a,_,_=masks[a];fixed_b,_,_=masks[b]
 print("UPPER_OBSTACLE",a,b,int(np.logical_xor(fixed_a[65],fixed_b[65]).sum()))
(root/"PLAY1X_DIAGNOSTIC_PIXELS.json").write_text(json.dumps({"scenes":data,"pairs":results},indent=2))
print("DIAGNOSTIC_ONLY: no gameplay or beam PASS is implied by artifacts or this script.")
