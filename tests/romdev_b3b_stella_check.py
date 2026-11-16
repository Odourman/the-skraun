"""B3b real Stella 6.7.1 pixel test. Only supported evidence is captured frames.
No independent verification; no inferred screenshot claims.
"""
from pathlib import Path
from PIL import Image
import hashlib, re
CENTERS=set(range(56,105,4))
gold=lambda p:p[0]>175 and p[1]>120 and 32<p[2]<155 and p[0]>p[1]>p[2]
gray=lambda p:min(p)>105 and max(p)-min(p)<28

def coords(path, predicate):
    im=Image.open(path).convert("RGB")
    return im,{(x,y) for y in range(im.height) for x in range(im.width) if predicate(im.getpixel((x,y)))}

def bbox(points):
    if not points: raise AssertionError("no matching pixels")
    xs=[p[0] for p in points];ys=[p[1] for p in points]
    return min(xs),min(ys),max(xs)+1,max(ys)+1

def process(name):
    files=sorted(Path("build").glob(f"{name}_motion_*.png"))
    assert len(files)>=50,(name,len(files),"Stella frames unavailable")
    frames=[]
    for path in files:
        im,g=coords(path,gold)
        _,p=coords(path,gray)
        gb,pb=bbox(g),bbox(p)
        center=(pb[0]+pb[2])/4    # 2 rendered pixels per TIA color clock
        assert center in CENTERS,(path.name,"P0 center",center,pb)
        assert pb[3]-pb[1]==24,(path.name,"vertical sprite row cropping",pb)
        assert pb[2]-pb[0]==32,(path.name,"sprite width",pb)
        assert pb[1]==99,(path.name,"P0 Y changed",pb)
        if name=="ring":
            # all rings should be identical shifted masks
            ring_center=(gb[0]+gb[2])/4
            assert abs(ring_center-center)<=2,(path.name,"center error >2 color clocks",ring_center,center,gb,pb)
            assert gb[2]-gb[0]==80 and gb[3]-gb[1] in (63,64),(path.name,"broken contour",gb)
            assert gb[1] in (79,80),(path.name,"ring Y unexpectedly shifted",gb)
            assert gb[0]>=0 and gb[2]<=320,(path.name,"ring clipping",gb)
        frames.append({"path":path,"center":int(center),"ring":g,"p0":p,"gb":gb,"pb":pb})
    # screenshot identifiers: 000 initial, 001..014 right, 015..045 left,
    # 046..076 right. Confirm real joystick reversals and continuous >2 states.
    group={"right1":[],"left":[],"right2":[]}
    for f in frames:
        n=int(f["path"].stem.split("_")[-1])
        if 1<=n<=15:group["right1"].append(f["center"])
        if 16<=n<=45:group["left"].append(f["center"])
        if 46<=n<=76:group["right2"].append(f["center"])
    for key,cs in group.items():
        assert len(cs)>=8,(name,key,"not enough frames",cs)
        change=[b-a for a,b in zip(cs,cs[1:])]
        if key=="left":
            assert all(delta<=0 for delta in change) and min(cs)<max(cs)-8,(name,key,cs)
        else:
            assert all(delta>=0 for delta in change) and max(cs)>min(cs)+8,(name,key,cs)
        assert all(abs(delta)<=4 for delta in change), (name,key,"skipped centers while holding joystick",cs)
    modes={f["center"] for f in frames}
    print(name,"FRAME COUNT",len(frames),"13 CENTERS SEEN",sorted(modes),"TRAJECTORY",group)
    assert modes==CENTERS,(name,"not all 13 centers captured; increase snapshot sampling",sorted(modes))
    return frames

ring=process("ring")
scenery=process("obstacle")
# Confirm every ring-only contour is a precise playfield-cell horizontal shift.
shapes={}
for f in ring:
    k=f["center"]; g=f["ring"]
    if k in shapes:assert g==shapes[k],("ring varied frame to frame",k,f["path"])
    shapes[k]=g
baseline=shapes[56]
for k,g in sorted(shapes.items()):
    assert {(x+2*(k-56),y) for x,y in baseline}==g,("broken right-half PF timing or geometry",k)
print("RING GEOMETRY: identical translated images for all 13 joystick centers")
# Scenery OR-composition test: fixed world obstacle columns 14,22,27 for y82..109.
# The figure's Y is screen-line 84..107, so use the observed ring baseline
# as vertical screenshot offset rather than guessing Stella crop framing.
y_offset=ring[0]["gb"][1]-64
world={(x,y) for col in (14,22,27) for x in range(8*col,8*col+8) for y in range(82+y_offset,110+y_offset)}
obstacle_by_center={}
for f in scenery:
    k=f["center"];g=f["ring"]
    # A solid P0 foreground pixel legitimately occludes PF pixels.
    # The obstacle mask is visible behind P0 only where P0 bitmap is transparent.
    exp=(shapes[k]|world)-f["p0"]
    overlap=shapes[k]&world
    obstruction=world-shapes[k]
    assert g==exp,(k,f["path"].name,"wrong OR-composition",len(g^exp),bbox(g),bbox(exp))
    obstacle_by_center[k]=(len(overlap),len(obstruction))
assert any(x>0 for x,y in obstacle_by_center.values())
assert all(y>0 for x,y in obstacle_by_center.values())
print("OBSTACLES: actual Stella pixels equal ring OR fixed-scene pixels for all 13 centers")
print("OBSTACLES: overlap/intersection (indistinguishable same-color pixels):",obstacle_by_center)
print("OBSTACLES: composition respects P0 foreground occlusion; PF picture is NOT collision truth")
for filename in ("romdev-b3b-dynamic.bin","romdev-b3b-obstacles.bin"):
    data=Path("build",filename).read_bytes()
    assert len(data)==4096,(filename,len(data))
    print("ROM_SHA256",filename,hashlib.sha256(data).hexdigest())
print("PASS B3b visual/motion + synthetic scenery OR; developer self-test only, not future renderer integration")
