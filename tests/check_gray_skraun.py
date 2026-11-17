"""Development-only smoke checks for the gray overhead Skraun art ROM.
Check source sprite tables and genuine Stella screenshots, not full independent verification.
"""
from pathlib import Path
import re
from PIL import Image

source=Path("experiments/p01_skraun_gray_topdown.asm").read_text()
names=("GfxRightA","GfxRightB","GfxLeftA","GfxLeftB")
frames={}
for name in names:
    m=re.search(r"^"+name+r":\n((?:\s*dc\.b %\d{8}\n?){12})",source,re.M)
    assert m,name+" table missing or wrong length"
    bits=re.findall(r"dc\.b %(\d{8})",m.group(1))
    assert len(bits)==12 and all(len(row)==8 for row in bits)
    frames[name]=list(reversed(bits)) # ASM stores bottom-to-top
for pose in ("A","B"):
    assert frames["GfxLeft"+pose]==[r[::-1] for r in frames["GfxRight"+pose]], "Left is not a horizontal pixel mirror"
assert frames["GfxRightA"]!=frames["GfxRightB"], "no two-pose animation"
diff=sum(a!=b for a,b in zip(frames["GfxRightA"],frames["GfxRightB"]))
assert diff>=4, ("insufficient animated rows",diff)
assert "lda #$0C" in source, "light-gray TIA color code missing"
assert "UpdateFacing:" in source and "Facing      =" in source
print("SOURCE PASS: 2 moving poses, 2 exact mirrored directions, gray TIA player")

def bbox_gray(path):
    im=Image.open(path).convert("RGB")
    pts=[]
    for y in range(im.height):
        for x in range(im.width):
            r,g,b=im.getpixel((x,y))
            if min(r,g,b)>100 and max(r,g,b)-min(r,g,b)<26:
                pts.append((x,y))
    assert len(pts)>20,("missing visible gray troll",str(path))
    xs=[x for x,y in pts];ys=[y for x,y in pts]
    return (min(xs),min(ys),max(xs)+1,max(ys)+1)

dims=[(16,12),(32,24),(64,36)]
for level,(w,h) in enumerate(dims,1):
    bb=bbox_gray(Path(f"build/gray_level{level}.png"))
    actual=(bb[2]-bb[0],bb[3]-bb[1])
    print("LEVEL",level,"bbox",bb,"dims",actual)
    assert actual==(w,h),f"expected {w}x{h}, got {actual}"
left=bbox_gray(Path("build/gray_left_walk.png"))
right=bbox_gray(Path("build/gray_right_walk.png"))
print("Left walking",left,"Right walking",right)
assert left!=right, "horizontal joystick directions did not alter the snapshot position"
print("STELLA SMOKE PASS: gray player renders at 3 sizes; opposite joystick input changes position")
