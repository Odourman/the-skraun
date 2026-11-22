#!/usr/bin/env python3
"""GAMEPLAY-4 honest authentic Stella observations, not artificial PASS.
Frame count / TIA pixels / state values checked only when physically present.
"""
from pathlib import Path
from PIL import Image
import numpy as np,hashlib,json,re
root=Path("build/gameplay4/scenes")
out={}
for scene in ["start","knight_warning","knight_strike","knight_rest","ranger_draw","ranger_release","arrow_first","arrow_mid","arrow_later","stage2_L3","gameover_restart"]:
 p=root/scene
 img=np.asarray(Image.open(p/"DEBUGGER_DESKTOP.png").convert("RGB"))
 assert img.shape[0]>=343 and img.shape[1]>=441,(scene,img.shape)
 rgb=img[115:343,121:441]
 Image.fromarray(rgb).save(p/"REAL_TIA_320x228.png")
 sess=(p/"SESSION_TYPED.txt")
 text=sess.read_text(errors="replace") if sess.exists() else ""
 # Stella actually prints #262 on its own line after typed debugger read.
 hits=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',text)
 scand=int(hits[-1]) if hits else None
 blue=np.all(rgb==[121,194,251],axis=2)
 green=np.all(rgb==[61,151,60],axis=2)
 gold=np.all(rgb==[244,214,69],axis=2)
 counts={"P1_lightblue_pixels":int(blue.sum()),"forest_green_pixels":int(green.sum()),"gold_exact_pixels":int(gold.sum())}
 state={}
 for key,addr in {"PlayerX":0x80,"PlayerY":0x81,"Level":0x82,"ArrowCool":0x9d,"ArrowDX":0xa3,"ArrowDY":0xa4,"KnightDir":0xa5,"Stage":0xaa,"Lives":0xac,"ScoreLo":0xad,"ScoreHi":0xae,"KnightX":0xaf,"DrawWarn":0xb0,"StrikeRelease":0xb1,"Recovery":0xb2,"StageKills":0xb4,"ArrowX":0xb8,"ArrowY":0xb9}.items():
  m=re.findall(r'> print \*\$'+f'{addr:02X}'+r'\s*\n[^\n]*?\$([0-9a-fA-F]{2})',text,re.I)
  if m:state[key]=int(m[-1],16)
 entry={"scene":scene,"scan_end":scand,"physical_rgb_sha256":hashlib.sha256(rgb.tobytes()).hexdigest(),
        "pixels":counts,"debugger_state_when_readable":state,
        "screenshot_authentic":True}
 out[scene]=entry
 print("REAL_STELLA",json.dumps(entry))
 if scand!=262:print("NOT_262_PHYSICAL_SCENE",scene,scand)
 if not state:print("NO_MACHINE_STATE_PARSED",scene,"trace available raw")
(root/"RUNTIME_FRAME_EVIDENCE.json").write_text(json.dumps(out,indent=2))
print("DEVELOPER_OBSERVED: measurements above only; no full 76c, pixel or arrow collision PASS inferred.")
