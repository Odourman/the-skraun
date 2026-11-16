"""A: actual Stella frame-pixel check for the gray overhead troll.
Developer self-test, not independent verification. Fail closed on missing evidence.
"""
from pathlib import Path
from PIL import Image
import re

source=Path("experiments/p01_skraun_gray_topdown.asm").read_text()
def frame(name):
    match=re.search(r"^"+name+r":\s*\n((?:\s*dc\.b %\d{8}\s*\n){12})", source, re.M)
    assert match, name
    return [int(s,2) for s in reversed(re.findall(r"dc\.b %(\d{8})", match.group(1)))]
patterns={(face,pose):frame("Gfx"+face+pose) for face in ("Right","Left") for pose in ("A","B")}
for pose in ("A","B"):
    assert patterns["Left",pose]==[int(f"{b:08b}"[::-1],2) for b in patterns["Right",pose]]

def bitmap(path):
    im=Image.open(path).convert("RGB")
    pts=[]
    for y in range(im.height):
        for x in range(im.width):
            r,g,b=im.getpixel((x,y))
            if min(r,g,b)>100 and max(r,g,b)-min(r,g,b)<26:
                pts.append((x,y))
    assert pts, ("no visible troll",path)
    xs=[x for x,y in pts]; ys=[y for x,y in pts]
    bounds=(min(xs),min(ys),max(xs)+1,max(ys)+1)
    return im,bounds

def sample(im,bb,level):
    x0,y0,x1,y1=bb
    scale={1:1,2:2,3:4}[level]
    assert (x1-x0,y1-y0)==(16*scale,12*level), (x0,y0,x1,y1,level)
    return tuple(sum((128>>col) for col in range(8)
                     if isgray(im.getpixel((x0+2*scale*col+scale,y0+row*level)))
                    ) for row in range(12))

def isgray(rgb):
    r,g,b=rgb
    return min(r,g,b)>100 and max(r,g,b)-min(r,g,b)<26

for level in (1,2,3):
    im,bb=bitmap(f"build/size_{level}.png")
    print("SIZE",level,bb)
    assert (bb[2]-bb[0],bb[3]-bb[1])==(16*{1:1,2:2,3:4}[level],12*level)
    actual=sample(im,bb,level)
    print("SIZEMASK",level,"bbox",bb,"actual",[f"{v:08b}" for v in actual],"expected",[[f"{v:08b}" for v in pp] for pp in patterns.values()])
    assert actual in (tuple(v) for v in patterns.values()), ("inverted or wrong sprite",level)

for face in ("Right","Left"):
    found=set()
    for path in sorted(Path("build").glob(f"face_{face}_*.png")):
        im,bb=bitmap(path)
        bits=sample(im,bb,1)
        for pose in ("A","B"):
            if bits==tuple(patterns[face,pose]):
                found.add(pose)
    assert found=={"A","B"}, (face,found,"Actual Stella frames did not show both poses")
    print("FRAME PASS", face, "poses A/B upright, arm and leg bitmasks")

directions={"R":(1,0),"L":(-1,0),"U":(0,-1),"D":(0,1),
            "UR":(1,-1),"UL":(-1,-1),"DR":(1,1),"DL":(-1,1)}
for name,(sx,sy) in directions.items():
    _,a=bitmap(f"build/move_{name}_before.png")
    _,b=bitmap(f"build/move_{name}_after.png")
    dx=(b[0]+b[2])-(a[0]+a[2])
    dy=(b[1]+b[3])-(a[1]+a[3])
    assert (dx>0)-(dx<0)==sx and (dy>0)-(dy<0)==sy, (name,dx,dy)
    print("MOVE PASS",name,"screenshot center delta",dx,dy)
print("A: Stella real-frame sprite/8-way diagnostic PASS (developer self-test)")
