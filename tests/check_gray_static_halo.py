"""Real Stella pixel checks for gray Skraun inside fixed playfield ring.

This is a bounded diagnostic and cannot approve a moving halo or finished game.
"""
from PIL import Image
from pathlib import Path

def box(points):
    assert len(points)>20,"not enough matching pixels"
    xs,ys=zip(*points)
    return min(xs),min(ys),max(xs)+1,max(ys)+1

last_ring=0
for lv,(w,h) in enumerate(((16,12),(32,24),(64,36)),1):
    img=Image.open(Path(f"build/gray_halo_level{lv}.png")).convert("RGB")
    gray=[];gold=[]
    for y in range(img.height):
        for x in range(img.width):
            r,g,b=img.getpixel((x,y))
            if min(r,g,b)>110 and max(r,g,b)-min(r,g,b)<25: gray.append((x,y))
            if r>175 and g>130 and 40<b<145 and r>g>b: gold.append((x,y))
    player=box(gray)
    ring=box(gold)
    pw,ph=player[2]-player[0],player[3]-player[1]
    rw,rh=ring[2]-ring[0],ring[3]-ring[1]
    print(f"Level {lv}: gray={player} size {pw}x{ph}, gold={ring} size {rw}x{rh}")
    assert (pw,ph)==(w,h), "wrong gray sprite size"
    assert ring[0]<player[0] and ring[1]<player[1] and ring[2]>player[2] and ring[3]>player[3], "ring fails to surround troll"
    assert rw>last_ring, "level should enlarge ring"
    last_ring=rw
print("PASS: actual Stella images show light-gray three-level Skraun inside three golden rings")

# Regression: catch exactly the historic upside-down sprite-data bug.
# The visible kernel does DEX and loads TrollPtr[X] for X=191..0.
# Thus tables MUST store bottom scanline at low addresses.
from pathlib import Path
import re

source = Path("experiments/p02_gray_static_halo.asm").read_text()
expected_top = (
    "00100100",  # short top horns/ears
    "01111110", "01111110", "01011010",
    "01111110", "11111101", "10011101", "00111100",
    "01111110", "01100100", "01000110",
    "11000010",  # lower feet
)
def is_gray(rgb):
    r,g,b = rgb
    return min(r,g,b)>110 and max(r,g,b)-min(r,g,b)<25

for lv in (1,2,3):
    mt = re.search(r"^Troll" + str(lv) + r":\s*\n((?:\s*dc\.b [^\n]+\n)+)",source,re.M)
    assert mt, f"Troll{lv} table not found"
    entries = [int(n,16) for n in re.findall(r"\$([0-9A-Fa-f]{2})",mt.group(1))]
    assert len(entries)==192,f"Level {lv}: expected 192 ROM scanline bytes, got {len(entries)}"
    visible_rows=[format(entries[idx],"08b") for idx in range(191,-1,-1) if entries[idx]!=0]
    expected_rows=[row for row in expected_top for _ in range(lv)]
    assert visible_rows==expected_rows, (
       f"Level {lv}: sprite row orientation inverted or art mismatched. "
       f"Expected top {expected_rows[0]}, bottom {expected_rows[-1]}, "
       f"got top {visible_rows[0]}, bottom {visible_rows[-1]}"
    )
    im=Image.open(f"build/gray_halo_level{lv}.png").convert("RGB")
    positions=[(x,y) for y in range(im.height) for x in range(im.width) if is_gray(im.getpixel((x,y)))]
    x0,y0,x1,y1=box(positions)
    sx=2*(1 if lv==1 else 2 if lv==2 else 4)
    for pixel_row in range(12*lv):
        for col in range(8):
            px=x0 + sx*col + sx//2
            py=y0+pixel_row
            actual=is_gray(im.getpixel((px,py)))
            expected=expected_top[pixel_row//lv][col]=="1"
            if actual != expected:
                raise AssertionError(f"Stella level {lv} orientation mismatch at logical ({col},{pixel_row}): "
                  f"expected {expected}, got {actual}")
    print(f"UPRIGHT PASS: Level {lv} top/bottom byte order and actual Stella pixels match reference")

