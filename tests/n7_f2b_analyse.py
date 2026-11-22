#!/usr/bin/env python3
"""Developer-only actual Stella debugger SCREENSHOT pixel evidence.
No simulated sprites, no promises of 3-person success without RGB/X match.
"""
from PIL import Image
from pathlib import Path
import sys, json, hashlib
root=Path(sys.argv[1]) / 'stella-s2-12'
files=sorted(root.glob('FRAME_*.png'))
assert len(files)==13,(len(files),"initial + 12 stepped frames required")
data=[]
for i,f in enumerate(files):
    raw=Image.open(f).convert('RGB')
    assert raw.size==(1400,1000),(f,raw.size)
    # Stella 6.7.1 debugger actual 320x228 TIA pane, as captured in COL1.
    tia=raw.crop((121,115,441,343))
    assert tia.size==(320,228)
    hist=tia.getcolors(320*228)
    assert hist is not None
    counted=sorted(hist,reverse=True)
    colors=[(n,rgb) for n,rgb in counted if n>=8]
    tia.save(root/f'TIA_{i:03d}.png')
    data.append(dict(index=i,image=f.name,unique=len(hist),colors=colors[:12],
                     sha256=hashlib.sha256(tia.tobytes()).hexdigest()))
    assert len(hist)>1,(f,"No output in actual Stella TIA region")
(root.parent/'PHYSICAL_PIXEL_SUMMARY.json').write_text(json.dumps(data,indent=2))
print("STELLA debugger actual frames",len(files),"unique TIA RGB counts:",[v['unique'] for v in data])
print("Frame TIA SHA256:",[v['sha256'][:12] for v in data])
print("NOT YET A PASS: 3 independently-positioned full bitmaps/color must be compared with source/positions.")
