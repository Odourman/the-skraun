#!/usr/bin/env python3
"""Actual SAME-SHA baseline/candidate Stella scanline comparison, no fabricated timing PASS."""
from pathlib import Path
from PIL import Image
import json,re,hashlib
root=Path("build/gameplay5/scenes")
out={}
for tag in ("frozen","candidate"):
 out[tag]={}
 for phase in (18,21,24,27,30):
  p=root/tag/f"ranger_{phase}"
  src=(p/"SESSION_TYPED.txt").read_text(errors="replace") if (p/"SESSION_TYPED.txt").exists() else ""
  hits=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',src)
  scan=int(hits[-1]) if hits else None
  im=Image.open(p/"DEBUGGER_DESKTOP.png").convert("RGB")
  rgb=im.crop((121,115,441,343))
  rgb.save(p/"REAL_TIA_320x228.png")
  out[tag][str(phase)]=dict(scan_end=scan,photo_sha256=hashlib.sha256(rgb.tobytes()).hexdigest(),
   gui_trace=(p/"SCANLINES_DEBUGGER.png").exists())
  print("REAL_STELLA",tag,phase,"scan",scan,"pixels_sha",out[tag][str(phase)]["photo_sha256"])
(root/"GAMEPLAY5_TIMING_COMPARE.json").write_text(json.dumps(out,indent=2))
print("NOTE: _scanEnd alone is NOT proof of 6507 76-cycle/register deadlines; capture raw console screenshot.")
if any(z["scan_end"] is None for t in out.values() for z in t.values()):
 raise SystemExit("Missing actual _scanEnd from Stella; cannot claim timing PASS")
