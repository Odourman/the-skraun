"""P02-R1: direct assembled-symbol-based worst-case static 6502 path ledger.
Distinct from Stella Debugger directly observed frame lengths.
"""
from pathlib import Path
import re,csv
centers=range(56,105,4)
types={"fast":"romdev_r1_fast_pf.asm","score":"romdev_r1_score_contrast.asm","p1":"romdev_r1_p1_stress.asm","opt":"romdev_r1_optimized_pf.asm"}
def symbols(f):
    out={}
    for l in Path(f).read_text().splitlines():
        m=re.match(r'^([A-Za-z][\w]*)\s+([0-9A-Fa-f]{4})\s+',l)
        if m:out[m[1]]=int(m[2],16)
    return out
def row_map(f):
    s=Path(f).read_text().split("RingRowMap:\n")[1].split("Troll2:\n")[0]
    values=[]
    for l in s.splitlines():
        if "dc.b" in l:
            values.extend(int(z,16) for z in re.findall(r"\$([0-9A-Fa-f]{2})",l.split(";")[0]))
    assert len(values)==193
    return values
rows=[]
for name,src in types.items():
    sym=symbols("build/romdev-r1-"+name+".sym")
    mp=row_map("experiments/"+src)
    worst=0;pf0deadline=0;pf1deadline=0;p1last=0
    for c in centers:
        for x in range(192,0,-1):
            index=mp[x]
            t=4+int(((sym["Troll2"]&255)+x)>255)+3  # LDA abs,X + STA GRP0
            t+=4+int(((sym["RingRowMap"]&255)+x)>255)
            t+=2+3 # LDA #0 + STA PF0
            for key in ("L1","L2","R0","R1"):
                t+=5+int(((sym[f"{key}_{c}"]&255)+index)>255)+3 # (zp),Y and STA
                if key=="R0":pf0=t
                if key=="R1":pf1=t
            t+=2+3  # LDA #0 STA PF2
            if name=="p1":
                t+=4+int(((sym["Troll2"]&255)+x)>255)+3  # extra P1 load/store
                p1store=t
            else:p1store=0
            t+=2+(3 if x>1 else 2)+3 # DEX / BNE / next WSYNC
            rows.append((name,c,x,t,pf0,pf1,p1store))
            worst=max(worst,t);pf0deadline=max(pf0deadline,pf0);pf1deadline=max(pf1deadline,pf1);p1last=max(p1last,p1store)
    assert worst<=76,("scanline overrun",name,worst)
    assert pf0deadline<=49 and pf1deadline<=54,("right PF missed handoff",name,pf0deadline,pf1deadline)
    print(name,"STATIC CALCULATION max cycles",worst,"margin",76-worst,
          "right PF0 latest",pf0deadline,"right PF1 latest",pf1deadline,"P1 data latest",p1last)
    if name=="p1":
        assert worst>=70,("synthetic P1 not included in ledger")
        print("R1-C: one active P1 bitmap fetch leaves",76-worst,"CPU cycles; separate knight/archer copies or arrow+orb not proved.")
print("B3b basis 63/76 cycles and 13 margin; R1-C P1-only near the boundary; no real enemies/HUD implemented.")
print("SCENERY: 1716 static combined-mask bytes / layout, eight unique layouts => 13728 bytes; 4K insufficient for direct duplication.")
print("RUNTIME 4-byte PF scenery OR >= 16 load cycles + OR instructions, cannot be added to 63-cycle baseline unchanged.")
print("COLORS: SCORE mode changes PF color per screen half (COLUP0 left, COLUP1 right), not per ring vs obstacle at overlap.")
print("R1 response engine gate: AND #$01 => a 4-TIA-clock move every 2 frames while held; poll-to-change 1..2 full frames (source logic), independently validate in Stella Debugger.")
with open("build/R1_STATIC_PATHS.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(("candidate","tia_center","countdown_x","cycles_including_WSYNC","latest_right_PF0","latest_right_PF1","P1_write_cycle"));w.writerows(rows)
