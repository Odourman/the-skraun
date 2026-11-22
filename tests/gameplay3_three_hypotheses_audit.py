#!/usr/bin/env python3
"""H1/H2 evidence, not a three-independent-actor PASS oracle."""
from pathlib import Path
from PIL import Image
import numpy as np, re, hashlib, json
root=Path("build/gameplay3/hyp_physical")
report={}
for label in ["H1_sameY_three_NUSIZ_copies","H2_separatedY_three_mask_stream"]:
    p=root/label
    rgb=np.asarray(Image.open(p/"DEBUGGER_DESKTOP.png").convert("RGB").crop((121,115,441,343)))
    Image.fromarray(rgb).save(p/"REAL_TIA_320x228.png")
    blue=np.all(rgb==[121,194,251],axis=2)
    green=np.all(rgb==[61,151,60],axis=2)
    gray=np.all(rgb==[210,210,209],axis=2)
    rows=np.flatnonzero(blue.any(axis=1)).tolist()
    groups=[]
    for y in rows:
        if not groups or y>groups[-1][-1]+1:groups.append([y])
        else:groups[-1].append(y)
    text=(p/"SESSION_TYPED.txt").read_text(errors="replace") if (p/"SESSION_TYPED.txt").exists() else ""
    m=re.search(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',text)
    data={"blue_p1_pixels":int(blue.sum()),"green_pf_pixels":int(green.sum()),
          "gray_p0_pixels":int(gray.sum()),"blue_y_groups":[[g[0],g[-1]+1] for g in groups],
          "real_scanlines":int(m.group(1)) if m else None,
          "rgb_sha256":hashlib.sha256(rgb.tobytes()).hexdigest()}
    report[label]=data
    print("PHYSICAL_ATTEMPT",label,json.dumps(data))
    print("FALSE_CANONICAL_PASS_PROHIBITED",label,
          "NUSIZ1 reproduces same bitmap" if label.startswith("H1") else "vertical copies share X and P1 color")
    if data["real_scanlines"]!=262:print("TIMING_FAIL",label,data["real_scanlines"])
    if label.startswith("H1"):
       print("H1_EXPECTED_3x_IDENTICAL_K1",116*3,"actual",data["blue_p1_pixels"])
       print("H1_PF_REGRESSION",data["green_pf_pixels"],"vs frozen stage1 PF 2832")
    else:
       print("H2_EXPECTED_2_K1_PLUS_1_R1_BITS_IN_BLUE",(58+53+58)*2,"actual",data["blue_p1_pixels"])
(root/"H1_H2_REAL_STELLA_NEGATIVE_ORACLE.json").write_text(json.dumps(report,indent=2))
assert len(report)==2
# This is negative for full 3-actor semantics regardless of sprite count:
# H1 cannot give distinct identities; H2 cannot give independent x/colour.
print("DEVELOPER_OBSERVED_BOUNDED_NEGATIVE: neither H1 nor H2 proves independent K1,K2,R same-Y.")
