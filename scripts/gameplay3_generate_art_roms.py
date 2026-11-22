#!/usr/bin/env python3
"""Generate EXACT K1-T/R1 native 8x16 row diagnostics in F8, 6 poses x 2 facings.
Each variant is a genuine independently assembled executable, not a mockup.
No writes to gameplay RAM via Stella debugger. Art input is frozen JSON only.
"""
from pathlib import Path
import json,re
root=Path("build/gameplay3/variants")
root.mkdir(parents=True,exist_ok=True)
masks=json.loads(Path("experiments/gameplay3/P1_K1T_R1_FROZEN_SOURCE.json").read_text())["actors"]
template=Path("experiments/gameplay3_bank1.asm").read_text()
pat=r"(?s)DummyScan:\nKnightNeutralScan:.*?ds 104,0\s+; index192[^\n]*"
assert re.search(pat,template)
start=template.index("SelectEnemyArt:\n")
stop=template.index("        ORG $F700",start)
manifest={}
for actor in ("knight","ranger"):
 for pose in ("neutral","warning","strike") if actor=="knight" else ("neutral","draw","release"):
  obj=masks[actor][pose]
  vals=[int(s[1:],16) for s in obj["rom_bottom_first_hex"]]
  top=[int(s[1:],16) for s in obj["hex_top_first"]]
  assert vals==top[::-1],(actor,pose)
  for flip in (0,1):
   name=actor+"_"+pose+("_mirror" if flip else "_native")
   src=re.sub(pat,"DummyScan:\nKnightNeutralScan:\n        ds 73,0\n        dc.b "+",".join(f"${x:02X}" for x in vals)+"\n        ds 104,0          ; index192 read must be zero",template,count=1)
   # Variant bypasses source gameplay actor choice ONLY in this separate diagnostic build.
   # K1 game engine/score and full baseline graphics remain active, input intact.
   reg="$08" if flip else "$00"
   color="$9E" if actor=="knight" else "$C6"
   trial="SelectEnemyArt:\n        lda #<KnightNeutralScan\n        sta EnemyRowPtr\n        lda #>KnightNeutralScan\n        sta EnemyRowPtr+1\n        lda #"+reg+"\n        sta REFP1\n        lda #"+color+"\n        sta COLUP1\n        rts\n"
   src=src[:src.index("SelectEnemyArt:\n")]+trial+src[src.index("        ORG $F700",src.index("SelectEnemyArt:\n")):]
   (root/(name+".asm")).write_text(src)
   manifest[name]={"actor":actor,"pose":pose,"mirrored":bool(flip),
                   "source_top_first":top,"source_bottom_first":vals,
                   "foreground_source_bits":sum(x.bit_count() for x in vals),
                   "physical_expected_pixels":sum(x.bit_count() for x in vals)*2}
(root/"POSE_SOURCE_MANIFEST.json").write_text(json.dumps(manifest,indent=2))
print("Exact 12 native/mirrored assembly variants prepared",list(manifest))
