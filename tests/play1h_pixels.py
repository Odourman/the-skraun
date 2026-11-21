#!/usr/bin/python3
from PIL import Image
from pathlib import Path
import json,hashlib,numpy as np
root=Path('build/play1h/moving')
names=['baseline','L1_on','L2_on','A_L3_on','B_L3_right8','C_L3_right8_down8']
data={}
pix={}
for name in names:
 f=root/name/'DEBUGGER_DESKTOP.png'
 assert f.exists(),name
 im=Image.open(f).convert('RGB').crop((121,115,441,343))
 im.save(root/name/'ACTUAL_STELLA_TIA.png')
 a=np.asarray(im)
 gold=(a[:,:,0]==234)&(a[:,:,1]==194)&(a[:,:,2]==84)
 gray=(a[:,:,0]==210)&(a[:,:,1]==210)&(a[:,:,2]==209)
 blue=(a[:,:,0]==121)&(a[:,:,1]==194)&(a[:,:,2]==251)
 def bbox(mask):
  yy,xx=np.where(mask)
  return [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] if len(xx) else None
 data[name]={'P0':bbox(gray),'P1':bbox(blue),'gold_bbox':bbox(gold),'gold_n':int(gold.sum()),'blue_n':int(blue.sum()),'rgb_sha256':hashlib.sha256(a.tobytes()).hexdigest()}
 pix[name]=(gold,gray,blue)
 print(name,data[name])
assert data['baseline']['P0'] and data['baseline']['blue_n']>0
assert data['A_L3_on']['P0'] and data['B_L3_right8']['P0'] and data['C_L3_right8_down8']['P0']
for l,dim in [('L1_on',(16,12)),('L2_on',(32,24)),('A_L3_on',(64,36)),('B_L3_right8',(64,36)),('C_L3_right8_down8',(64,36))]:
 b=data[l]['P0']; assert (b[2]-b[0],b[3]-b[1])==dim,(l,b,dim)
assert data['B_L3_right8']['P0'][0]>data['A_L3_on']['P0'][0],'P0 did not really move X'
assert data['C_L3_right8_down8']['P0'][1]>data['B_L3_right8']['P0'][1],'P0 did not really move Y'
def difference(a,b):
 m1,g1,p1=pix[a];m2,g2,p2=pix[b]
 non=(~(g1|g2|p1|p2))
 delta=np.logical_xor(m1,m2)&non
 return int(delta.sum()),bbox(delta)
result={}
for k,a,b in [('x','A_L3_on','B_L3_right8'),('y','B_L3_right8','C_L3_right8_down8')]:
 cnt,box=difference(a,b)
 result[k]={'unoccluded_gold_pixel_changes':cnt,'bbox':box}
 print('REAL_TIA_A_B_C',k,result[k])
(root/'PLAY1H_REAL_PIXEL_AUDIT.json').write_text(json.dumps({'scenes':data,'unoccluded_diffs':result},indent=2))
print('This script tests actual pixels; nonzero position-dependence alone does NOT prove geometric 360 halo.')
