#!/usr/bin/env python3
"""Two materially different TIA P1 raster-copy trials, NOT canonical gameplay.
H1 same-Y NUSIZ1 copies. H2 3 disjoint Y bands in one P1 stream.
No independent actor X/color/state in either; fail closed on those semantics.
"""
from pathlib import Path
import json,re
root=Path("build/gameplay3/hypotheses");root.mkdir(parents=True,exist_ok=True)
src=Path("experiments/gameplay3_bank1.asm").read_text()
m=json.loads(Path("experiments/gameplay3/P1_K1T_R1_FROZEN_SOURCE.json").read_text())["actors"]
# H1 same-Y: 3 hardware P1 copies; TIA cannot give the three copies different
# bitmaps or COLUP1 on the same scanline unless scheduled register updates fit.
a=src.replace("        jsr SelectEnemyArt ; offscreen identity/pose, never after GRP1 beam deadline",
 "        jsr SelectEnemyArt ; offscreen identity/pose, never after GRP1 beam deadline\n        lda #$03\n        sta NUSIZ1     ; three copies, close spacing, one P1 bitmap (NOT 3 identities)")
a=a.replace("        lda KnightX       ; diagnostic P1 knight follows X",
            "        lda #67            ; H1 stress positions approx x67,x83,x99, not Ranger101")
assert a!=src
(root/"H1_sameY_three_NUSIZ_copies.asm").write_text(a)
# H2 separated-Y: one hardcoded 193-entry P1 scan table with 3 distinct art
# identities at disjoint scan rows, but NO independent X movement and NO
# individually configurable same-Y P1 copies.
masks=[
 m["knight"]["neutral"]["rom_bottom_first_hex"],
 m["ranger"]["neutral"]["rom_bottom_first_hex"],
 m["knight"]["neutral"]["rom_bottom_first_hex"],
]
def dc(seq):
 return "        dc.b "+",".join(seq)+"\n"
pattern=r"(?s)DummyScan:\nKnightNeutralScan:.*?ds 104,0\s+; index192[^\n]*"
repl=("DummyScan:\nKnightNeutralScan:\n"
      "        ds 33,0\n"+dc(masks[0])+
      "        ds 44,0\n"+dc(masks[1])+
      "        ds 44,0\n"+dc(masks[2])+
      "        ds 24,0 ; 193 rows TOTAL, separate-Y three P1 sources")
b=re.sub(pattern,repl,src,count=1)
assert b!=src
start=b.index("SelectEnemyArt:\n");end=b.index("        ORG $F700",start)
sel=("SelectEnemyArt:\n"
     "        lda #<KnightNeutralScan\n        sta EnemyRowPtr\n"
     "        lda #>KnightNeutralScan\n        sta EnemyRowPtr+1\n"
     "        lda #0\n        sta REFP1\n        lda #$9E\n        sta COLUP1\n"
     "        rts\n")
b=b[:start]+sel+b[end:]
(root/"H2_separatedY_three_mask_stream.asm").write_text(b)
(root/"HYPOTHESIS_CONSTRAINTS.json").write_text(json.dumps({
"H1":{"technique":"NUSIZ1 three copies close same-Y","actor_count_visible_possible":3,
      "independent_actors":False,"per_actor_bitmap":False,"per_actor_color":False,
      "expected_note":"~x67,83,99 but 3 shared K1-T rows; NOT authentic x101 Ranger"},
"H2":{"technique":"three disjoint 16-scanline sprite bands in one precomputed 193-row source",
      "actor_count_visible_possible":3,"independent_actors":False,
      "per_actor_bitmap":True,"per_actor_color":False,
      "per_actor_x":False,"expected_note":"three distinct source rows but one shared P1 X and color"}
},indent=2))
print("H1/H2 are renderer LIMIT probes, NOT a real three-independent-enemy implementation.")
