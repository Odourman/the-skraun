# THE SKRAUN GRAPHICS v0.2 – source-data validation
# Runs only over art JSON. Does not test ROM or Stella.
import json
from pathlib import Path
root=Path(__file__).resolve().parent
s=json.loads((root/"skraun_sprites_v02.json").read_text(encoding="utf-8"))["candidates"]
for name,data in s.items():
 for pose in ("A","B"):
  rows=data[pose]
  assert len(rows)==12 and all(len(r)==8 and set(r)<=set("01") for r in rows),(name,pose)
  assert data[pose+"_left"]==[r[::-1] for r in rows],(name,pose,"mirror")
  assert rows[0][2]==rows[0][5]=="1",(name,pose,"ears")
  assert rows[0]!=rows[11],(name,pose,"head-feet anchor")
  assert any(r[0]=="1" or r[1]=="1" for r in rows[10:]),(name,pose,"left foot")
  assert any(r[6]=="1" or r[7]=="1" for r in rows[10:]),(name,pose,"right foot")
 assert s[name]["A"]!=s[name]["B"],(name,"pose")
 assert any(data["A"][k]!=data["B"][k] for k in (5,6)),(name,"front limbs")
 assert any(data["A"][k]!=data["B"][k] for k in (9,10,11)),(name,"hind limbs")
enemies=json.loads((root/"enemy_sprites_v02.json").read_text())["sprites"]
for name,rows in enemies.items():
 assert len(rows)==12 and all(len(r)==8 for r in rows),name
worlds=json.loads((root/"worlds_playfield_40x24.json").read_text())["worlds"]
assert len(worlds)==4
for world,data in worlds.items():
 assert len(data["layouts"])==2
 for name,rows in data["layouts"].items():
  assert len(rows)==24 and all(len(r)==40 and r==r[::-1] for r in rows),(world,name)
halo=json.loads((root/"halo_masks_and_metrics_v02.json").read_text())["families"]
for family,info in halo.items():
 widths,heights=[],[]
 for level in ("1","2","3"):
  data=info["levels"][level]
  rows=data["mask"]
  assert len(rows)==24 and all(len(r)==40 and r==r[::-1] for r in rows),family
  widths.append(data["measurement"]["width_color_clocks"])
  heights.append(data["measurement"]["height_scanlines"])
 assert widths==sorted(widths) and heights==sorted(heights),family
print("PASS: source art bitmap shapes, A/B, mirror, row anchors, enemies, worlds and halo footprints")
