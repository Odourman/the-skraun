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
