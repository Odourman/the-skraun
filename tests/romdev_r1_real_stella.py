"""P02-R1: genuine Stella image + joystick-flow developer diagnostics.
Slow-motion Stella -speed 10 is ONLY capture pacing, not hardware fps timing.
Synthetic tests never validate enemies, collision, HUD or B3c.
"""
from PIL import Image
from pathlib import Path
from hashlib import sha256
from collections import Counter
import re
CENTERS=set(range(56,105,4))
def gold(p):
    r,g,b=p
    return r>175 and g>120 and 32<b<155 and r>g>b
def gray(p):
    r,g,b=p
    return min(p)>105 and max(p)-min(p)<28
def green(p):
    r,g,b=p
    return g>65 and g>r*1.15 and g>b*1.07
def coords(im,pred):
    return {(x,y) for y in range(im.height) for x in range(im.width) if pred(im.getpixel((x,y)))}
def bbox(ps):
    assert len(ps)>10,"blank / missing sprite"
    xs,ys=zip(*ps)
    return min(xs),min(ys),max(xs)+1,max(ys)+1
def masks_from_rom():
    sym=Path("build/romdev-r1-fast.sym").read_text()
    match=re.search(r"^Troll2\s+([0-9a-fA-F]{4})",sym,re.M)
    assert match,"DASM symbol missing"
    adr=int(match.group(1),16)-0xF000
    return Path("build/romdev-r1-fast.bin").read_bytes()[adr:adr+193]
TROLL=masks_from_rom()
def check(name):
    files=sorted(Path("build").glob(name+"_motion_*.png"))
    assert len(files)==123,(name,len(files),"missing original Stella captures")
    centers=[];shapes={}
    for path in files:
        im=Image.open(path).convert("RGB")
        gg=coords(im,gold)
        graypix=coords(im,gray)
        greenpix=coords(im,green)
        if name=="score":
            # SCORE colors depend on screen half, not on original ring/scenery.
            assert len(graypix)>70 and len(greenpix)>50,("SCORE PF colors not visible",path,len(graypix),len(greenpix))
            continue
        pb=bbox(graypix)
        assert pb[2]-pb[0]==32 and pb[3]-pb[1]==24,("P0 dimensions",path,pb)
        assert pb[1]==99,("P0 Y drift",path,pb)
        ctr=(pb[0]+pb[2])/4
        assert ctr in CENTERS,("center outside diagnostic quantization",path,ctr,pb)
        k=int(ctr)
        ring=bbox(gg)
        if name=="opt":
            assert FAST_SHAPES is not None, "fast ring reference required"
            world={(x,y) for col in (14,22,27)
                   for x in range(col*8,col*8+8)
                   for y in range(97,125)}
            expected=(FAST_SHAPES[k]|world)-graypix
            assert gg==expected,("optimized precomposed scene not equal baseline OR fixed world",path,len(gg^expected))
        else:
            assert ring[2]-ring[0]==80 and ring[3]-ring[1]==64,("ring contour clipping",path,ring)
        if name!="opt":
            assert abs((ring[0]+ring[2])/4-ctr)<=2,("P0/ring not centered",path,ring,pb)
            assert ring[1]==79,("ring Y drift",path,ring)
        pred={(pb[0]+bit*4+dx,pb[1]+j)
              for j in range(24) for bit in range(8) for dx in range(4)
              if TROLL[192-(84+j)] & (0x80>>bit)}
        assert graypix==pred,("sprite row order/raster corruption",path,len(graypix^pred))
        if k in shapes:assert gg==shapes[k],("unequal ring masks across frames",name,k)
        shapes[k]=gg;centers.append(k)
        if name=="p1":
            # Extra P1 is a green synthetic sprite in a separate horizontal slot
            assert len(greenpix)>30,("synthetic P1 not visible",path,len(greenpix))
            gb=bbox(greenpix)
            assert gb[0]>=268 and gb[2]<=320,("P1 positioned unexpectedly",path,gb)
            assert gb[1]<pb[3] and gb[3]>pb[1],("P1 does not share overlapping Y rows",path,gb,pb)
        else:
            assert len(greenpix)==0,("unintended extra green object",path)
    if name=="score":
        print("SCORE-MODE: 123 true Stella screens have both color families; color is per screen half, not per object")
        return
    assert set(centers)==CENTERS,("fast 2-frame joystick missed center states",name,sorted(set(centers)))
    for key,seq in (
        ("right1",centers[1:27]),("left",centers[27:75]),("right2",centers[75:123])):
        delta=[b-a for a,b in zip(seq,seq[1:])]
        if key=="left": assert all(d<=0 for d in delta),(name,key,seq)
        else: assert all(d>=0 for d in delta),(name,key,seq)
        assert max(abs(d) for d in delta)<=8,("capture jumps >2 increments",name,key,seq)
        print(name,key,"centers sampled",seq)
    if name!="opt":
        first=shapes[56]
        for center,mask in shapes.items():
            assert {(x+(center-56)*2,y) for x,y in first}==mask,("PF ring was distorted by joystick",center)
    assert min(centers)==56 and max(centers)==104
    print(name,"PASS all 13 centers, fixed Y, pixel-exact upright P0, genuine slow-motion joystick",len(files))
    return shapes

FAST_SHAPES=None
for kind in ("fast","score","p1","opt"):
    shapes=check(kind)
    if kind=="fast":FAST_SHAPES=shapes
    b=Path("build/romdev-r1-"+kind+".bin").read_bytes()
    assert len(b)==4096
    print(kind,"ROM SHA256",sha256(b).hexdigest())
print("R1 real-Stella visual test PASS (developer self-test); geometry does not prove future scene-object feasibility")
