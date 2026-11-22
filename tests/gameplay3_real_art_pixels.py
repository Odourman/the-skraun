#!/usr/bin/env python3
"""Strict physical native 8x16 P1-pixel audit, REAL 320x228 Stella TIA crop.
Input: Stella screenshot, exact source JSON from frozen Graphics II.
No mockups, no screenshot scaling for oracle, no RAM/PC injections.
"""
from pathlib import Path
from PIL import Image
import numpy as np
import json,hashlib,re
root=Path("build/gameplay3/art")
ref=json.loads(Path("build/gameplay3/variants/POSE_SOURCE_MANIFEST.json").read_text())
results={}
for name,meta in sorted(ref.items()):
 p=root/name
 f=p/"DEBUGGER_DESKTOP.png"
 assert f.is_file(), ("NO_AUTHENTIC_STELLA_FRAME",name)
 rgb=np.asarray(Image.open(f).convert("RGB").crop((121,115,441,343)))
 assert rgb.shape==(228,320,3)
 Image.fromarray(rgb).save(p/"REAL_TIA_320x228.png")
 mask=np.all(rgb==([121,194,251] if meta["actor"]=="knight" else [61,151,60]),axis=2)
 top=meta["source_top_first"]
 if meta["mirrored"]:
  top=[int(f"{v:08b}"[::-1],2) for v in top]
 expectation=np.array([[bool(v & (1<<(7-x))) for x in range(8) for _ in (0,1)] for v in top])
 assert expectation.shape==(16,16)
 hits=[]
 for y in range(108,137):
  for x in range(192,272):
   part=mask[y:y+16,x:x+16]
   if part.shape==(16,16) and np.array_equal(part,expectation):
    hits.append((x,y))
 cnt=int(mask[105:150,192:288].sum())
 entry={"pose":meta["pose"],"actor":meta["actor"],"mirror":meta["mirrored"],
        "physical_pixel_count_region":cnt,"expected_total":meta["physical_expected_pixels"],
        "exact_pixel_matches":hits,"physical_crop_sha256":hashlib.sha256(rgb.tobytes()).hexdigest()}
 log=(p/"SESSION_TYPED.txt")
 if log.exists():
  match=re.search(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',log.read_text(errors="replace"))
  entry["scanline_count"]=int(match.group(1)) if match else None
 else:entry["scanline_count"]=None
 results[name]=entry
 print("PHYSICAL_STELLA",name,json.dumps(entry))
 assert cnt==meta["physical_expected_pixels"],("P1_COLOUR/COUNT_ERROR",name,entry)
 assert len(hits)==1,("NO_EXACT_NATIVE_PIXEL_SOURCE_MATCH",name,hits)
 assert entry["scanline_count"]==262,("NOT_REAL_NTSC_262",name,entry["scanline_count"])
(root/"GAMEPLAY3_NATIVE_PIXEL_ORACLE.json").write_text(json.dumps(results,indent=2))
print("GAMEPLAY3_SIX_MASKS_BOTH_FACINGS_TRUE_STELLA_P1_PIXEL_PASS: 12 source-faithful physical frames")
