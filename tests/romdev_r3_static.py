"""P02-R3 static 6507 cycle ledger from actual DASM symbols and all 13 centers.
Physical A/B scanlines are separate 76-cycle deadlines. No 262-frame result is CPU proof.
"""
from pathlib import Path
import re,csv,collections
BUDGET=76; names=("overlap","partial","stagger")
def symbols(n):
    s={}
    for line in Path("build/r3-"+n+".sym").read_text().splitlines():
        m=re.match(r"^([A-Za-z][\w]*)\s+([0-9A-Fa-f]{4})\s+",line)
        if m:s[m[1]]=int(m[2],16)
    return s
def bytes_at(bin,sym,label,count):
    i=sym[label]-0xF000
    assert 0<=i<4096-count,(label,i)
    return list(bin[i:i+count])
def crossing(address,i):
    return int((address&255)+i>255)
summary=[];details=[]
for n in names:
    source=Path("experiments/romdev_r3_"+n+".asm").read_text()
    rom=Path("build/r3-"+n+".bin").read_bytes()
    assert len(rom)==4096
    s=symbols(n)
    rowmap=bytes_at(rom,s,"RingRowMap",177)
    sprmap=bytes_at(rom,s,"SpriteRowMap",177)
    assert all(0<=i<=18 for i in rowmap)
    assert all(0<=i<=88 for i in sprmap)
    assert len(bytes_at(rom,s,"Troll3",177))==177
    assert bytes_at(rom,s,"EnemyArt0",8)!=bytes_at(rom,s,"EnemyArt1",8)
    assert bytes_at(rom,s,"EnemyArt1",8)!=bytes_at(rom,s,"EnemyArt2",8)
    assert any(x for x in bytes_at(rom,s,"M_"+("halo" if n!="stagger" else "union")+"_R2_104",19)), "actual right PF2 must be nonzero x104"
    worst_A=worst_B=0; worst_pf0=worst_pf1=worst_pf2=0;count=0
    skip=set()
    # Four gap lines at each actual hardware RESP1/HMOVE transition.
    for target in ([40,130] if n=="stagger" else [40] if n=="partial" else []):
        skip.update(range(target-3,target+1))
    for c in range(56,105,4):
      for x in range(176,0,-2):
        y=rowmap[x]
        b=x-1
        if x in skip:
            assert b in skip,(n,x,b,skip)
            continue
        kinds=["union"] if n=="stagger" else ["halo","scenery"]
        for layer in kinds:
            # PHYSICAL LINE A: GRP0, ring index, PF0-left clear, 5 indirect data groups, dex, WSYNC
            a=4+crossing(s["Troll3"],x)+3
            a+=4+crossing(s["RingRowMap"],x)
            a+=2+3
            aa=a
            for g in ("L1","L2","R0","R1","R2"):
                ptr=s[f"M_{layer}_{g}_{c}"]
                a+=5+crossing(ptr,y)+3
                if g=="R0":pf0a=a
                if g=="R1":pf1a=a
                if g=="R2":pf2a=a
            a+=2+3
            # PHYSICAL LINE B: same PF data row Y; preload VDEL P1 from RAM for NEXT two-row pair.
            bb=4+crossing(s["Troll3"],b)+3+2+3
            for g in ("L1","L2","R0","R1","R2"):
                ptr=s[f"M_{layer}_{g}_{c}"]
                bb+=5+crossing(ptr,y)+3
                if g=="R0":pf0b=bb
                if g=="R1":pf1b=bb
                if g=="R2":pf2b=bb
            bb+=4+crossing(s["SpriteRowMap"],b)+4+3+2
            # one BNE (3 cycles), or CPX immediate + BNE for split vertical regions
            split=(n=="stagger" and b in (131,41)) or (n=="partial" and b==41)
            bb+=(2 if split else 0)
            bb+=3 if b>1 and not split else (2 if b==1 else 3)
            bb+=3
            worst_A=max(worst_A,a);worst_B=max(worst_B,bb)
            worst_pf0=max(worst_pf0,pf0a,pf0b)
            worst_pf1=max(worst_pf1,pf1a,pf1b)
            worst_pf2=max(worst_pf2,pf2a,pf2b)
            details.append((n,c,x,b,layer,y,a,bb,pf0a,pf1a,pf2a,pf0b,pf1b,pf2b))
            count+=1
    # 76-cycle budget pertains to each ACTIVE raster; transitions are four outside-halo lines.
    # Include status without suppressing a genuine failure.
    result="PASS" if max(worst_A,worst_B)<=76 else "FAIL"
    # Worst deadlines in CPU cycles incl 68 hblank color clocks -> xPF0=80,PF1=96,PF2=128:
    # PF0 right starts at 80 TIA clocks: (68+80)/3, PF1 at96, PF2 at128.
    beam={"PF0":(68+80)/3,"PF1":(68+96)/3,"PF2":(68+128)/3}
    timing_ok=worst_pf0<beam["PF0"] and worst_pf1<beam["PF1"] and worst_pf2<beam["PF2"]
    if not timing_ok:result="FAIL"
    print(n, "STATIC SYMBOL-PATH",result,"A",worst_A,"B",worst_B,"margin",76-max(worst_A,worst_B),
          "latest right PF0/PF1/PF2 writes",worst_pf0,worst_pf1,worst_pf2,"beam deadlines",beam,"paths",count)
    summary.append((n,result,worst_A,worst_B,76-max(worst_A,worst_B),worst_pf0,worst_pf1,worst_pf2,timing_ok,count))
    assert timing_ok,(n,"beam write too late",summary[-1])
    assert worst_A<=76 and worst_B<=76,(n,"6507 kernel cannot fit 76 cycles",summary[-1])
    # Precise 128-byte RIOT allocation from source fixed labels: 23 variables $80..$96 +89 buffer bytes $A0..$F8.
    print("RIOT allocated: 23 state bytes + 89 P1-buffer bytes =112/128 used,16 free (NOT enough proven for full AI/physics).")
    print("P1 frame duty designed:",["20Hz each 3-way overlap","30Hz+30Hz overlapping pair, 60Hz separate third","60Hz each 3 staggered bands"][names.index(n)])
    print("Visible HUD: 16 lines separate but no score logic; no claim it increases arena scanline cycles.")
with open("build/R3_STATIC_ASSEMBLED_WORST_CASE_SUMMARY.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(("variant","pass","worst_A","worst_B","min_margin","latest_R0","latest_R1","latest_R2","PF_deadlines_safe","enumerated_paths"));w.writerows(summary)
with open("build/R3_ALL_ASSEMBLED_SCANLINE_PATHS.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(("variant","TIA_player_center","A_countdown","B_countdown","PF_layer","PF_row_index","cycles_A","cycles_B","PF0right_A","PF1right_A","PF2right_A","PF0right_B","PF1right_B","PF2right_B"));w.writerows(details)
print("SCENE: RAM-buffer P1 construction in VBLANK and region transition cycles outside ellipse have no audited per-instruction debugger trace; direct Stella frames still required.")
print("At worst same-Y P1 two additional 6507 actors cannot be drawn in one frame: fixed one P1 slot; 3-way rotation = 20Hz per actor, even before arrow/orb.")
print("Minimal per-scanline missile ENAM0 or ball ENABL enable+positioning >=5 cycles each; arithmetic margins above are pre-projectile.")
print("PF alternate: 30Hz each for independently colored gold ring and blue obstacles on separate FRAMES; no same-pixel true concurrent layering.")
print("ROM scaling: 8 independent layouts cannot be assumed to share precomputed mask aliases, even if each 4K diagnostic fits.")
