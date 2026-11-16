#!/usr/bin/env python3
"""P01-ART1: exact source-to-NATIVE-STELLA GRP0 semantic raster tests.
36 distinct logical states, 3 candidate ROMs, 3 NUSIZ widths, 2 poses,
2 facings; source masks imported unchanged, including Q1 A_left/B_left.
No concept-preview pixels are ever used as evidence of Stella correctness.
"""
import collections, csv, hashlib, json, pathlib, re
from PIL import Image

B=pathlib.Path("build")
source=json.loads(pathlib.Path("experiments/romdev_p01_art1_exact_P1_masks.json").read_text())
q=json.loads(pathlib.Path("experiments/romdev_p01_art1_exact_Q1_v03.json").read_text())
palette=(210,210,209) # Stella 6.7.1 native RGB for NTSC COLUP0=$0C
cases={"A_rounded_back":source["candidates"]["A_rounded_back"],
       "B_low_long_back":source["candidates"]["B_low_long_back"],
       "Q1_splayed_quad":source["baseline_Q1"]}
# Validate Q1 baseline in P1 against actually separately preserved v0.3 source.
for pose in ("A","B"):
    for side in ("right","left"):
        k=pose if side=="right" else "A_left" if pose=="A" else "B_left"
        qq=pose if side=="right" else "left_"+pose
        assert source["baseline_Q1"][k]==q["new_attempts"]["Q1_splayed_quad"][qq],(pose,side,"Q1 provenance")
def bits(s):return [1 if c=="1" else 0 for c in s]
def reflect(rows):return [s[::-1] for s in rows]
def reference(candidate,pose,side):
    obj=cases[candidate]
    if side=="right":return obj[pose]
    k=pose+"_left" if candidate=="Q1_splayed_quad" else "left_"+pose
    assert k in obj,("missing explicit facing key",candidate,k)
    rows=obj[k]
    assert rows==reflect(obj[pose]),(candidate,pose,"source not true mirror")
    return rows
for c in cases:
    for p in ("A","B"):
        for f in ("right","left"):
            rows=reference(c,p,f)
            assert len(rows)==12 and all(len(x)==8 and set(x)<={"0","1"} for x in rows)
# Distinguishing source-level vertical reversal is microscopic for A pose A.
h=lambda a,b:sum(x!=y for row1,row2 in zip(a,b) for x,y in zip(row1,row2))
dists={c:{p:h(reference(c,p,"right"),reference(c,p,"right")[::-1]) for p in ("A","B")} for c in cases}
assert dists["A_rounded_back"]["A"]==4,("MAIN issue #17 4-cell difference",dists)
assert dists["A_rounded_back"]["B"]==20
assert dists["B_low_long_back"]=={"A":28,"B":36}
assert dists["A_rounded_back"]["A"]>0
print("SOURCE SOURCE-ROW VFLIP HAMMING:",dists,"Q1 A_left keys read explicitly.")
# Negative control is the exact authorized A pose A row-order wrong, 4 of 96 cells.
# This does not modify the ROM or source: verify that our full logical-row oracle
# fails on a reversed reference even though pixel count/bbox stay unchanged.
assert sum(map(str.count, reference("A_rounded_back","A","right"),["1"]*12)) == sum(map(str.count,reference("A_rounded_back","A","right")[::-1],["1"]*12))
assert reference("A_rounded_back","A","right") != reference("A_rounded_back","A","right")[::-1]
states=[]
def rows_from_png(path,logical_rows,repeat,scale):
    im=Image.open(path).convert("RGB")
    assert im.size==(320,228),("NOT genuine 1x Stella screenshot size",path,im.size)
    px=im.load()
    lit={(x,y) for y in range(228) for x in range(320) if px[x,y]==palette}
    assert lit,("P0 absent",path)
    rowheight=12*repeat
    pixelwide=16*scale
    observed_min_x=min(x for x,y in lit)
    # These exact reference sources contain ink at both horizontal extremities
    # somewhere; true P0 group-left is thus equal to min gray pixel x.
    assert max(x for x,y in lit)-observed_min_x+1==pixelwide,(path,"visible P0 width")
    firstink=next(i for i,r in enumerate(logical_rows) if "1" in r)
    y0=min(y for x,y in lit)-firstink*repeat
    expected=set()
    actual_rows=[]
    for ri in range(12):
        rowbits=""
        for bit in range(8):
            want=logical_rows[ri][bit]=="1"
            tile={(observed_min_x+bit*2*scale+dx,y0+ri*repeat+dy)
                  for dy in range(repeat) for dx in range(2*scale)}
            n=len(tile&lit)
            assert n in (0,len(tile)),(path,ri,bit,"tearing/misaligned/partial P0 cell",n)
            rowbits+="1" if n else "0"
            if want:expected|=tile
        actual_rows.append(rowbits)
    assert lit==expected,(path,"ACTUAL STELLA 12 RASTER ROWS mismatch",actual_rows,logical_rows,
                         "differing original pixels",len(lit^expected))
    assert actual_rows==logical_rows
    # Deliberately reversed A pose A must be rejected by EXACT pixel oracle.
    if ("A_rounded_back" in str(path) and "state_0_A" in str(path)):
        assert actual_rows!=logical_rows[::-1],("negative test erroneously accepts 4-cell vflip",path)
    return {"x":observed_min_x,"y":y0,"ink":len(lit),"rows":actual_rows,"width":pixelwide,"logical_h":rowheight}
for candidate,obj in cases.items():
    seen={}
    for stage in range(6):
        level=stage//2+1
        side="right" if stage%2==0 else "left"
        repeat,scale=((1,1),(2,2),(3,4))[level-1]
        for pose in ("A","B"):
            key=f"state_{stage}_{pose}"
            path=B/("frames_"+candidate)/(key+".png")
            assert path.is_file(),("MISSING ACTUAL Stella capture",path)
            rows=reference(candidate,pose,side)
            info=rows_from_png(path,rows,repeat,scale)
            seen[(level,side,pose)]=info
            states.append({"candidate":candidate,"level":level,"side":side,"pose":pose,"path":str(path),
                          "x":info["x"],"y":info["y"],"ink_pixels":info["ink"],"logical_h":info["logical_h"],
                          "pixel_width":info["width"],"all_12_exact_rows_pass":True})
    assert len(seen)==12
    for level in (1,2,3):
        for pose in ("A","B"):
            r=seen[(level,"right",pose)]["rows"]
            l=seen[(level,"left",pose)]["rows"]
            assert l==reflect(r),(candidate,level,pose,"actual STELLA P0 left not pixel-perfect mirror")
            assert seen[(level,"right",pose)]["x"]==seen[(level,"left",pose)]["x"],(candidate,level,pose,"mirror moves player")
            assert seen[(level,"right",pose)]["y"]==seen[(level,"left",pose)]["y"],(candidate,level,pose,"mirror y drift")
    # First-stage consecutive 24 original emulator frames: A for 8, B for 8, A for 8,
    # while staying at first level and right-facing. Their actual captured pixel art
    # must match the respective P0 image rather than source-only inferred animation.
    walkrows=[]
    for idx in range(24):
        pose="A" if ((3+idx)//8)%2==0 else "B" # first frame StageFrame=3
        path=B/("frames_"+candidate)/(f"walk_{idx:02d}.png")
        assert path.is_file(),("MISSING consecutive Stella frame",path)
        info=rows_from_png(path,reference(candidate,pose,"right"),1,1)
        assert info["x"]==seen[(1,"right","A")]["x"],(candidate,idx,"walking but diagnostic P0 X drift")
        walkrows.append(info["rows"])
    assert sum(w==reference(candidate,"A","right") for w in walkrows)==16,(candidate,"unexpected A-frame cadence")
    assert sum(w==reference(candidate,"B","right") for w in walkrows)==8,(candidate,"unexpected B-frame cadence")
    # Extract code-safe source-mirroring, not silent fallbacks.
    assert seen[(1,"right","A")]["rows"] != seen[(1,"right","B")]["rows"],(candidate,"animation is static")
    print("STELLA EXACT BITMAP 12/12 PASS",candidate,"+24 1-frame walk images, 1x/2x/4x NUSIZ, exact 12row mirror")
assert len(states)==36
with open(B/"P01_ART1_36_REAL_STELLA_EXACT_PIXEL_STATES.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(states[0]));w.writeheader();w.writerows(states)
(B/"P01_ART1_ORIENTATION_NEGATIVE_CONTROL.json").write_text(json.dumps({
  "candidate":"A_rounded_back","pose":"A","row_flip_hamming_cells":4,
  "size_preserving_vertical_inversion_rejected":True,"tested_source_96bit_rows":reference("A_rounded_back","A","right"),
  "deliberately_inverted_rows":reference("A_rounded_back","A","right")[::-1],
  "verified_against_actual_original_stella_pixels":True},indent=2))
print("P01-ART1 HARDWARE IMAGE CHECK PASS: 36 exact 12-row states +72 genuinely consecutive walk frames.")
print("The art identity question remains with MAIN: source sprites unedited and not aesthetically approved.")
