"""P02-R2 static, assembled-symbol anchored 6507 cycle/beam budget.
No estimated CPU time masquerading as debugger measurement.
Check every 13 ring center, every relevant visible x, both A/B line paths,
exact ROM page crossings and branch/WSYNC cost.
"""
from pathlib import Path
import re,csv,collections
BUDGET=76
def symbols(path):
    d={}
    for line in Path(path).read_text().splitlines():
        m=re.match(r"^([A-Za-z][A-Za-z_0-9]*)\s+([0-9A-Fa-f]{4})\b",line)
        if m:d[m.group(1)]=int(m.group(2),16)
    return d
def mask(src):
    s=Path(src).read_text()
    s=s.split("RingRowMap:\n")[1].split("Troll2:\n")[0]
    rows=[]
    for line in s.splitlines():
        if "dc.b" in line:rows.extend(int(x,16) for x in re.findall(r"\$([0-9A-Fa-f]{2})",line.split(";")[0]))
    assert len(rows)==193,(src,len(rows))
    return rows
variants={
 "baseline":("experiments/romdev_r1_p1_stress.asm",False,False,False),
 "twoline":("experiments/romdev_r2_two_line_p1.asm",True,False,False),
 "dual":("experiments/romdev_r2_two_line_dualcopy.asm",True,True,False),
 "hud":("experiments/romdev_r2_multikernel_hud.asm",False,False,True),
 "interlace":("experiments/romdev_r2_two_line_interlace.asm",True,False,False),
}
def crossing(addr,index):
    return 1 if (addr&255)+index>255 else 0
all_paths=[];summary=[]
for name,(path,pair,dual,hud) in variants.items():
    sym=symbols("build/r2-"+name+".sym")
    mp=mask(path)
    assert "RingRowMap" in sym and "Troll2" in sym and "Visible" in sym if name in ("baseline","hud") else "R2Pair" in sym
    if dual:assert "EnemyArcher" in sym
    maxcycles=0;maxpf0=0;maxpf1=0;maxarch=0;maxknight=0;worstpaths=[]
    for c in range(56,105,4):
        visible=176 if hud else 192
        for x in range(visible,0,-1):
            a_line=not pair or x%2==0
            idx=mp[x if a_line else x+1]
            if name=="interlace" and not a_line:
                # B line draws independently blue scene stencil. Actual src branch:
                # 1 P0 load, 3 left PF clears, X-indexed row test, 3 right-left PF writes,
                # P1 load, color reset and loop tail.
                t=4+crossing(sym["Troll2"],x)+3
                t+=2+3+3+3                    # zero and three left PF clears
                t+=4+crossing(sym["ObstacleRows"],x)
                scene=83<=x<=110
                t+=2 if scene else 3
                if scene:
                    t+=2+3; pf2=t
                    t+=2+3; pf0=t
                    t+=2+3; pf1=t
                else:pf0=pf1=0
                t+=4+crossing(sym["Troll2"],x)+3
                t+=2+3                         # restore next line PF gold color
                t+=2+(3 if x>1 else 2)+3     # DEX/BNE/WSYNC
                maxcycles=max(maxcycles,t);maxpf0=max(maxpf0,pf0);maxpf1=max(maxpf1,pf1)
                all_paths.append((name,c,x,"B",idx,t,pf0,pf1,0,0))
                if t>=74:worstpaths.append((c,x,t))
                continue
            t=4+crossing(sym["Troll2"],x)+3 # P0 load, GRP0
            if a_line:t+=4+crossing(sym["RingRowMap"],x) # first physical line has row map fetch
            t+=2+3  # LDA #0, STA left PF0
            for key in ("L1","L2","R0","R1"):
                t+=5+crossing(sym[key+"_"+str(c)],idx)+3
                if key=="R0":pf0=t
                if key=="R1":pf1=t
            if dual:
                t+=4+crossing(sym["EnemyArcher"],x)+3
                arch=t
            else:arch=0
            t+=2+3 # LDA #0 STA right PF2
            if name!="hud":
                t+=4+crossing(sym["Troll2"],x)+3 # one P1 bitmap written late
                knight=t
            else:knight=0
            if name=="interlace":t+=2+3   # A-line late COLUPF write sets blue for B, after ring edge
            t+=2 # DEX
            if not pair or (x%2==1):t+=3 if x>1 else 2
            t+=3 # NEXT WSYNC
            maxcycles=max(t,maxcycles);maxpf0=max(pf0,maxpf0);maxpf1=max(pf1,maxpf1)
            maxarch=max(maxarch,arch);maxknight=max(maxknight,knight)
            all_paths.append((name,c,x,"A" if a_line else "B",idx,t,pf0,pf1,arch,knight))
            if t>=74:worstpaths.append((c,x,t))
    h=0
    if hud:
        # HUD 16 physical lines: LDA/STA COLUPF, PF0/PF1/PF2, DEX/BNE, next WSYNC
        h=2+3+2+3+2+3+2+3+2+3+3
        maxcycles=max(maxcycles,h)
    print(f"{name:9s} STATIC MAX {maxcycles}/76, MARGIN {76-maxcycles}, latest right PF0={maxpf0}, PF1={maxpf1}, late GRP1 arch={maxarch}, knight={maxknight}, 16-HUD-line={h}, most stressed count={len(worstpaths)}")
    if name=="dual":
        # Actual timing from beam x clock: 68 hblank clocks, then 3 clocks/CPU cycle.
        # First P1 image x56, copy at x120 (NUSIZ1=$04), archer update must land before second copy.
        # "Knight" preloading must happen AFTER x128, for the next scanline's first P1 copy.
        arch_limit=(68+120)/3
        knight_min=(68+128)/3
        print("DUALCOPY CLOCK DEMAND: archer GRP1 write before",round(arch_limit,2),"cpu cycles; Knight preload after",round(knight_min,2),"cpu cycles.")
        print("SECOND COPY DEADLINE", "PASS" if maxarch<arch_limit else "FAIL", "at",maxarch)
        print("PRELOAD AFTER SECOND COPY", "PASS" if maxknight>knight_min else "FAIL", "at",maxknight)
    if maxcycles>76:
        print(f"FAIL: {name} exceeds one original TIA raster line. Do not claim a PASS even if Stella outputs 262 lines.")
    else:
        print(f"STATIC WITHIN 76: {name}, needs direct Stella/Debugger frame and pixel proof")
    summary.append((name,maxcycles,76-maxcycles,maxpf0,maxpf1,maxarch,maxknight,h,len(worstpaths)))
assert len(all_paths)==13*(192*4+176)
with open("build/R2_ALL_ASSEMBLED_RASTER_PATHS.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(("variant","tia_x","physical_countdown_x","two_line_phase","pf_index","cycles_including_next_wsync","right_pf0_write","right_pf1_write","second_P1_GRP1_write","next_P1_GRP1_preload"));w.writerows(all_paths)
with open("build/R2_STATIC_SUMMARY.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(("variant","static_worst_CPU_cycles","margin","latest_right_PF0","latest_right_PF1","second_copy_write","next_knight_preload","hud_kernel_cycle_cost","paths_at_least_74_cycles"));w.writerows(summary)
print("Interlace: 50% vertical row duty for each scene/halo color; NOT 50% frame-rate flicker. Distortion/legibility must be judged from genuine emulator images.")
print("Timing caveat: 262 frame lines alone DO NOT guarantee PF deadlines or two correct independently shaped P1 copies.")
print("Level3 bounded reach: level2 40 TIA clocks wide ring must grow beyond LEVEL3 P0 (NUSIZ0 4x width=32 TIA clocks); leave margin to both screen edges; no new fixed radius proposed.")
print("RAM: original source P1, two-line, dual 10 bytes $80-$89; HUD source 10 bytes. No extra RAM used by line pair or HUD demo.")
print("Distinct P1 copies by NUSIZ1=$04 have exactly 64 TIA-clock X spacing, NOT 2 arbitrary enemy positions; cannot independently address 3 overlapping enemy sprites.")
