"""P02-R1-C static object-slot and minimal cycle lower-bound engineering reservation.
Built on real assembled symbol-ledger CSV, NOT a simulated completed game.
"""
from pathlib import Path
import csv
from collections import defaultdict
rows=list(csv.DictReader(Path("build/R1_STATIC_PATHS.csv").open()))
worst=defaultdict(int); deadlines=defaultdict(lambda:{"PF0":0,"PF1":0})
for r in rows:
    name=r["candidate"]
    worst[name]=max(worst[name],int(r["cycles_including_WSYNC"]))
    deadlines[name]["PF0"]=max(deadlines[name]["PF0"],int(r["latest_right_PF0"]))
    deadlines[name]["PF1"]=max(deadlines[name]["PF1"],int(r["latest_right_PF1"]))
assert worst["p1"]>=worst["fast"]+7
budget=76
scenarios=[
("PF ring + P0 (actual assembler)","fast",0,"P0, PF", "yes", "Only a level-2 ring, no true scenery layer"),
("PF ring + P0 + ONE synthetic P1 (actual assembler)","p1",0,"P0, P1, PF", "yes", "Second bitmap shares Y but a fixed X; no AI"),
("Above + enable one arrow missile (lower bound)","p1",5,"P0, P1, M0, PF", "theoretical", "LDA #2/STA ENAM0; no position, motion or collision"),
("Above + orb ball (lower bound)","p1",10,"P0, P1, M0, BL, PF", "theoretical", "LDA/STA twice only, no object positioning"),
("Above + second distinct P1 bitmap (minimum)","p1",7,"P0, P1 reused, PF", "not hardware-independent", "Additional abs,X/STA GRP1 only; no RESP1/HMOVE or positioning"),
("Two knights, archer, arrow, orb + minimal HUD glyph (lower bound)","p1",2*7+5+5+7,"P0, P1, M0, BL, PF", "no", "Requires 3 distinct opponents; only 1 P1 player remains, 2 extra loads do not solve horizontal slots"),
("Runtime scenery OR for four registers (strict minimum)","fast",16,"P0, PF", "no", "Four extra reads; excludes any OR opcode and memory setup"),
("Row-wise PF color change (minimal, no P1)","fast",5,"P0, PF", "yes but no independent layers", "LDA immediate+STA COLUPF recolors BOTH scene and halo on row"),
("Row-wise PF color plus P1 synthetic load","p1",5,"P0, P1, PF", "theoretical", "LDA immediate+STA color, no dynamic table; leaves zero on worst line"),
]
table=[]
for title,base,additional,slots,phys,remarks in scenarios:
    wc=worst[base]+additional
    status="CYCLE FAIL" if wc>budget else "CYCLE ONLY"
    if "not hardware-independent" in phys or (phys=="no" and wc<=budget):status="HARDWARE SLOT BLOCKED"
    table.append([title,base,worst[base],additional,wc,budget-wc,status,slots,remarks])
    print(f"{status}: {title}: >= {wc}/76, margin <= {budget-wc}; {slots}; {remarks}")
assert worst["fast"]<=63 and worst["p1"]>=70
assert any(x[6]=="CYCLE FAIL" for x in table)
assert any("SLOT" in x[6] for x in table) or worst["p1"]+2*7>76
with open("build/R1_OBJECT_HEADROOM_LOWER_BOUNDS.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(("scenario","base_variant","real_static_base_worst","minimum_extra_cycles","conservative_total_minimum","remaining_upper_bound","cycle_status","hardware_slots","limits"))
    w.writerows(table)
print("Physical TIA actors: P0, P1; M0/M1 narrow missiles (share player colors); BL shares PF color/priority; PF one common 40-column bit plane.")
print("NUSIZ player copies repeat the same bitmap on one scanline; they do not provide three independent enemy animations.")
print("Score mode recolors PF by LEFT/RIGHT SCREEN HALF, not by game-object identity. No per-object independent PF color at overlaps.")
print("Minimum new object RAM heuristic (NOT implemented/tested): knight1, knight2, archer, arrow, orb at 3-4 state bytes each = 15..20 RAM bytes plus P0, timing, HUD, collision states.")
print("Collision logic must stay independent of actual PF color/pixels. Rectangle lists can be stored in ROM and tested during VBLANK/overscan, but not profiled in R1.")
print("HUD can use dedicated vertical bands, but no full multi-row HUD drawing was authorized/tested. Same-Y row pressure remains unresolved.")
print("STATIC LOWER-BOUND ESTIMATES ONLY: these extra cost scenarios are not directly emulated integrated gameplay.")
