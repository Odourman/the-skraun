"""Static 6502 cycle ledger, derived from DASM symbols and exact indexed addresses.
NOT a Stella-measured cycle trace. Hardware deadline concerns are separately labelled.
"""
from pathlib import Path
import re,csv
CENTERS=tuple(range(56,105,4))
KEYS=("L1","L2","R0","R1")
def symbols(path):
    s={}
    for line in Path(path).read_text().splitlines():
        m=re.match(r'^([A-Za-z][A-Za-z_0-9]*)\s+([0-9a-fA-F]{4})\s+',line)
        if m:s[m[1]]=int(m[2],16)
    return s

def mapbytes(src):
    text=Path(src).read_text()
    chunk=text.split("RingRowMap:\n",1)[1].split("Troll2:\n",1)[0]
    vals=[]
    for line in chunk.splitlines():
        if "dc.b" in line:vals.extend(int(x,16) for x in re.findall(r'\$([0-9a-fA-F]{2})',line.split(';')[0]))
    assert len(vals)==193,(len(vals),src)
    return vals

def analysis(name):
    sym=symbols(f"build/romdev-b3b-{name}.sym")
    rmap=mapbytes(f"experiments/romdev_b3b_{'dynamic' if name=='dynamic' else 'obstacles'}.asm")
    raw=[]
    for c in CENTERS:
        for x in range(192,0,-1):
            row=rmap[x]
            t=0
            t+=4+(int((sym["Troll2"]&255)+x>255)) # LDA Troll2,x
            t+=3 # STA GRP0
            t+=4+(int((sym["RingRowMap"]&255)+x>255))
            t+=2+3 # LDA #0 ; STA PF0
            for key in KEYS:
                t+=5+int((sym[f"{key}_{c}"]&255)+row>255) # indirect indexed
                t+=3 # STA PF1/PF2/PF0/PF1 respectively
                if key=="R0":pf0=t
                if key=="R1":pf1=t
            t+=2+3 # LDA #0 ; STA PF2
            t+=2 # DEX
            t+=3 if x>1 else 2 # BNE
            t+=3 # following STA WSYNC, includes all active cycles
            raw.append((name,c,x,row,t,pf0,pf1))
    return raw

a=analysis("dynamic")
b=analysis("obstacles")
assert len(a)==len(b)==13*192
assert [x[1:] for x in a]==[x[1:] for x in b],"unexpected per-line overhead from fixed scenery"
assert max(q[4] for q in a)<=76,"worst-case visible line overflows 76 cycles"
maximum=max(q[4] for q in a)
late0=max(q[5] for q in a);late1=max(q[6] for q in a)
print("STATIC 6502 COUNT: max",maximum,"of 76; min margin",76-maximum,
      "per visible line incl WSYNC; 13 x 192 paths, no frame-profiling claim")
print("RIGHT-HALF PF0 latest write cycle:",late0,"required <=49 according to TIA handoff timing")
print("RIGHT-HALF PF1 latest write cycle:",late1,"target <=54 due color clock 164")
assert late0<=49,("PF0 handoff risk",late0)
assert late1<=54,("PF1 handoff risk",late1)
print("WRITE COUNT: six PF register writes, one GRP0 and one WSYNC per visible scanline")
print("NO extra visible-line cycles for fixed scenery OR composition: masks precomputed in ROM")
print("P1 available; no enemy sprite writes in visible kernel")
for name in ("dynamic","obstacles"):
    print(name, "ROM bytes",Path(f"build/romdev-b3b-{name}.bin").stat().st_size,
          "zero-page RAM $80-$89 =10 used, 118 free (isolated test only)")
print("ROM table payload: 13 * 4 * 33 =1716 masks; 2 * 193=386 sprite+rowmap; 8*13=104 pointer entries; 13 P0 X entries")
print("FUTURE COST: a runtime four-byte scenery OR would add >=4 memory accesses*4 cycles = >=16 cycles/scanline;")
print("          67+16=83 > 76 (not feasible in this unchanged kernel).")
print("         Fixed per-layout composed masks scale ~1716 bytes per backdrop; 8 layouts =13,728 bytes, before gameplay.")
with Path("build/B3B_STATIC_CYCLE_LEDGER.csv").open("w",newline="") as f:
    w=csv.writer(f)
    w.writerow(("candidate","center_tia","line_index_X","mask_row","cycles_including_next_WSYNC","right_PF0_store_cycle","right_PF1_store_cycle"))
    w.writerows(a+b)
print("PASS: static cycle-path enumeration from DASM symbol addresses; Stella frame timing must be measured separately")
