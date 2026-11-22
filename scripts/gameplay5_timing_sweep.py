#!/usr/bin/env python3
"""GAMEPLAY-5 A: do not confuse source timer theory with actual physical Stella scanlines.
Generate TWO only physical overscan repartition tests with same total nominal time."""
from pathlib import Path
source=Path("experiments/gameplay5_bank1.asm").read_text()
base=Path("experiments/gameplay5_bank0.asm").read_text()
start="        lda #34             ; ~29 raster lines of overscan incl update work"
end="        sta WSYNC          ; GAMEPLAY-2 measured frame 261 -> add one OVERSCAN line, target 262"
assert source.count(start)==1 and source.count(end)==1
for n in (33,32):
 t=source.replace(start,f"        lda #{n}             ; GAMEPLAY-5 A measured alternate timer repartition, not yet proven")
 t=t.replace(end,end+"\n"+("        sta WSYNC          ; extra synchronized overscan line after shorter timer\n"*(34-n)))
 out=Path("build/gameplay5/timing")/f"timer{n}"
 out.mkdir(parents=True,exist_ok=True)
 (out/"bank1.asm").write_text(t)
 (out/"bank0.asm").write_text(base)
 print("SOURCE_ONLY_VARIANT",n,"extra_wsync",34-n)
