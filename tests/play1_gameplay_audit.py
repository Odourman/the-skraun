#!/usr/bin/python3
from PIL import Image
from pathlib import Path
import json,sys
root=Path(sys.argv[1])/'gameplay'
scenes=['baseline','l1_fire','movement_pickup','level2_fire','level3_after_respawn','halo_fire_target','halo_follow_move']
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
# Physical source-pixel and gameplay regression; no injected RAM states.
def width_height(scene):
  a=data[scene]['P0_gray_bbox']
  assert a is not None,scene
  return (a[2]-a[0],a[3]-a[1])
assert width_height('baseline')==(16,12),('exact frozen L1 U1 changed',data['baseline'])
assert width_height('l1_fire')==(16,12),'L1 sprite corrupted on FIRE'
assert width_height('movement_pickup')==(32,24),'real BL pickup did not grow to level2'
assert width_height('level2_fire')==(32,24),'L2 sprite changed during halo'
assert width_height('level3_after_respawn')==(64,36),'real second BL pickup did not grow to level3'
assert width_height('halo_fire_target')==(64,36),'L3 sprite changed during target hit'
assert width_height('halo_follow_move')==(64,36),'L3 sprite changed while moving under halo'
assert data['baseline']['P1_blue_n']==120,('frozen R3 bitmap source exact should be 120 twofold TIA pixels',data['baseline'])
assert data['movement_pickup']['P1_blue_n']==120,'P1 training source changed near orb'
assert data['level2_fire']['P1_blue_n']==120,'level2 has radius 28, dummy x125 delta29 should survive'
assert data['level3_after_respawn']['P1_blue_n']==120,'target should survive before FIRE'
assert data['halo_fire_target']['P1_blue_n']==0,'active L3 halo did not kill/hide dummy'
assert data['halo_follow_move']['P1_blue_n']==0,'defeated dummy should stay gone'
assert data['baseline']['gold_n']==0,'PF gold leaked while idle'
assert data['movement_pickup']['gold_n']==0,'PF gold leaked with orb state'
assert data['level3_after_respawn']['gold_n']==0,'PF gold leaked before FIRE'
assert data['l1_fire']['gold_n']>2816,'no visible gold ring independent of recolored obstacles at L1'
assert data['level2_fire']['gold_n']>data['l1_fire']['gold_n'],'L2 ring should have more physical PF pixels than L1'
assert data['halo_fire_target']['gold_n']>data['level2_fire']['gold_n'],'L3 ring should have more physical PF pixels than L2'
assert data['halo_follow_move']['gold_n']>2816,'halo should remain ON while P0 moves'
b=data['halo_fire_target']['P0_gray_bbox'];m=data['halo_follow_move']['P0_gray_bbox']
assert m[0]>b[0] and m[1]==b[1],('joystick did not move player under 30f halo',b,m)
print('DEVELOPER_OBSERVED actual joystick PASS: L1->L2->L3 by BL contact, 8x12->16x24->32x36 sources, level-specific PF gold, P1 dummy disappears L3 FIRE, P0 moves while halo ON')
print('LIMITATION / EXPECTED NEGATIVE: current PF2 ring tables are anchored to arena x80/y112 and do not follow P0 X/Y; not a complete playable-halo PASS.')
