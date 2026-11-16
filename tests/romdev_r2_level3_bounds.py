"""P02-R2-C: HYPOTHETICAL level-3 halo coverage/edge/ROM bound.
Not a level-3 implementation, not a gameplay radius declaration.
"""
from pathlib import Path
import csv
P0_L3=(32,36) # TIA color clocks by physical NTSC scanlines
L2=(40,64)
L3_PROXY=(48,72)
THICKNESS_PROXY=4
assert L3_PROXY[0]>max(P0_L3[0],L2[0])
assert L3_PROXY[1]>max(P0_L3[1],L2[1])
rows=[]
columns=[("PF0 left",0,16),("PF1 left",16,48),("PF2 left",48,80),
         ("PF0 right",80,96),("PF1 right",96,128),("PF2 right",128,160)]
for center in range(56,105,4):
    left=center-L3_PROXY[0]//2
    right=center+L3_PROXY[0]//2
    cols=[name for name,start,end in columns if left<end and right>=start]
    requires_extra=any(name in ("PF0 left","PF2 right") for name in cols)
    rows.append([center,left,right,",".join(cols),requires_extra])
    print(f"proxy center {center}: outer extent {left}..{right}, PF groups {cols}, needs PF beyond R1 4-table assumption={requires_extra}")
with open("build/R2_LEVEL3_HYPOTHETICAL_EDGE_AND_MASKS.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(("TIA_center","proxy_left","proxy_right","intersected_PF_groups","additional_groups_beyond_4_mask_renderer"));w.writerows(rows)
# R1 compact vertical symmetry: 33 rows for 64 physical; L3 72 physical => 37 including blank sentinel.
rows_L2=33;rows_L3=37;centers=13
L2_bytes=centers*4*rows_L2
L3_4=centers*4*rows_L3
L3_6=centers*6*rows_L3
print("HYPOTHETICAL STRICTLY ADVISORY geometry: L3 P0 32x36 TIA-clock/scanline, current L2 ring 40x64; research proxy L3 ring 48x72 and 4-clock outline thickness")
print("MASK DATA bytes no-scene BEFORE DEDUP: 13x4x33 L2",L2_bytes,"13x4x37 L3",L3_4,"delta",L3_4-L2_bytes)
print("If all 6 PF groups required: 13x6x37",L3_6,"bytes, delta to L2",L3_6-L2_bytes)
print("8 layouts naively duplicated: 4-group",8*L3_4,"6-group",8*L3_6,"bytes before code, P0, enemies and HUD.")
print("All 13 diagnostic centres fit screen 0..160 for 48 wide, but at x104 right extent touches PF2-right that the current 4-mask kernel forces to ZERO.")
print("Free horizontal gameplay positions beyond this diagnostic grid could clip; no permanent movement bounds/collision rules authorized.")
print("Level3 is NOT TESTED in a real ROM. Different radius, thickness or Y movement may demand different register data and higher CPU deadlines.")
