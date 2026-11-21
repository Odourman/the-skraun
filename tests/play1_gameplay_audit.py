#!/usr/bin/python3
from PIL import Image
from pathlib import Path
import json,sys
root=Path(sys.argv[1])/'gameplay'
scenes=['baseline','movement_pickup','level3_after_respawn','halo_fire_target']
data={}
for scene in scenes:
  pic=root/scene/'DEBUGGER_DESKTOP.png'
  assert pic.exists(),scene
  full=Image.open(pic).convert('RGB')
  assert full.size==(1400,1000)
  tia=full.crop((121,115,441,343))
  tia.save(root/scene/'ACTUAL_STELLA_TIA.png')
  pix=tia.load()
  gray={(x,y) for y in range(228) for x in range(320) if pix[x,y]==(210,210,209)}
  blue={(x,y) for y in range(228) for x in range(320) if pix[x,y]==(121,194,251)}
  gold={(x,y) for y in range(228) for x in range(320) if pix[x,y][0]>pix[x,y][2]+25 and pix[x,y][1]>pix[x,y][2]+10}
  bbox=lambda s:(min(x for x,y in s),min(y for x,y in s),max(x for x,y in s)+1,max(y for x,y in s)+1) if s else None
  data[scene]={'P0_gray_bbox':bbox(gray),'P0_gray_n':len(gray),'P1_blue_bbox':bbox(blue),'P1_blue_n':len(blue),'gold_n':len(gold),'colors':sorted(tia.getcolors(320*228),reverse=True)[:12]}
  print(scene,data[scene])
(root/'PLAY1_REAL_GAMEPLAY_IMAGE_AUDIT.json').write_text(json.dumps(data,indent=2))
# Baseline/stage checks are strictly actual Stella pixel tests.
assert data['baseline']['P0_gray_bbox'] is not None
assert data['baseline']['P1_blue_n']>0
assert data['movement_pickup']['P0_gray_bbox']!=data['baseline']['P0_gray_bbox'], 'joystick action did not move P0'
assert data['level3_after_respawn']['P0_gray_bbox'] is not None
# Do not claim orb or halo success until independently inspected:
print('ACTUAL STELLA joystick-state capture completed; halo/dummy require visible gold and P1 test.')
