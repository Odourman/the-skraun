#!/usr/bin/env python3
"""Real Stella M0 scanline/pixel observations, never assert full PASS from screenshots."""
from pathlib import Path
from PIL import Image
import numpy as np, re, json, hashlib
root=Path("build/gameplay5/m0/scenes")
result={}
for phase in (18,21,24,27,30,35,40):
 p=root/f"arrow_{phase}"
 src=(p/"SESSION_TYPED.txt").read_text(errors="replace") if (p/"SESSION_TYPED.txt").exists() else ""
 m=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',src)
 scan=int(m[-1]) if m else None
 rgb=np.asarray(Image.open(p/"DEBUGGER_DESKTOP.png").convert("RGB").crop((121,115,441,343)))
 Image.fromarray(rgb).save(p/"REAL_TIA_320x228.png")
 gray=np.all(rgb==[188,188,188],axis=2)
 # Keep raw screenshot + machine state; actual gray color is palette dependent.
 values={}
 for var,addr in (("arrowdx","A3"),("arrowdy","A4"),("arrowx","B8"),("arrowy","B9"),("cooldown","9D"),("segment_on","89"),("segment_off","8A")):
  m=re.findall(r'> print \*\$'+addr+r'\s*\n[^\n]*?\$([0-9a-fA-F]{2})',src,re.I)
  if m:values[var]=int(m[-1],16)
 result[str(phase)]={"scan_end":scan,"state_when_parseable":values,
  "photo_sha256":hashlib.sha256(rgb.tobytes()).hexdigest(),"gray_p0_palette_pixels":int(gray.sum())}
 print("AUTHENTIC_M0",phase,json.dumps(result[str(phase)]))
root.joinpath("M0_PHYSICAL_OBSERVATIONS.json").write_text(json.dumps(result,indent=2))
if any(x["scan_end"] is None for x in result.values()):
 raise SystemExit("M0_NOT_VERIFIED: missing Stella physical scanline trace")
if any(x["scan_end"]!=262 for x in result.values()):
 raise SystemExit("M0_NTSC_FAIL_FOR_TESTED_SCENES: physical frame not 262")
print("M0_BOUNDED_FRAME262_POSSIBLE; physical individual M0 pixel-movement and hit NOT automatically certified")
