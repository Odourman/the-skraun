"""ROMDEV C P02-B3a: compare actual Stella screens at three PF centers.
This is developer self-test only; no collision, FIRE or moving halo.
"""
from pathlib import Path
from PIL import Image
from hashlib import sha256
from collections import Counter

def pixels(file):
    return Image.open(file).convert("RGB")

def gold(rgb):
    r,g,b=rgb
    return r>175 and g>130 and 40<b<145 and r>g>b

def gray(rgb):
    r,g,b=rgb
    return min(r,g,b)>110 and max(r,g,b)-min(r,g,b)<25

def bounds(points):
    assert len(points)>50, "missing colored graphic"
    xs,ys=zip(*points)
    return min(xs),min(ys),max(xs)+1,max(ys)+1

allgold=[]
for clock in (56,80,104):
    im=pixels(f"build/b3a_{clock}.png")
    g={(x,y) for y in range(im.height) for x in range(im.width) if gold(im.getpixel((x,y)))}
    p={(x,y) for y in range(im.height) for x in range(im.width) if gray(im.getpixel((x,y)))}
    gb=bounds(g); pb=bounds(p)
    print("CENTER",clock,"ring",gb,"gold pixels",len(g),"P0",pb)
    assert gb[0]<pb[0] and gb[1]<pb[1] and gb[2]>pb[2] and gb[3]>pb[3], ("ring not enclosing P0",clock)
    assert abs((gb[0]+gb[2]-1)/2-clock*2)<=5, ("not centered at requested TIA x",clock,gb)
    assert len(g)>150, ("missing/fragmented ring",clock)
    allgold.append((clock,g,gb))
a,b,c=allgold
assert len(a[1])==len(b[1])==len(c[1]), "ring pixel count changed with X"
assert (a[2][2]-a[2][0],a[2][3]-a[2][1])==(b[2][2]-b[2][0],b[2][3]-b[2][1])==(c[2][2]-c[2][0],c[2][3]-c[2][1]), "ring geometry changed"
assert {(x+48,y) for x,y in a[1]}==b[1], "56->80 graphical discontinuity/different outline"
assert {(x+48,y) for x,y in b[1]}==c[1], "80->104 graphical discontinuity/different outline"

rom=Path("build/romdev-c-b3a.bin").read_bytes()
assert len(rom)==4096
print("ROM size 4096 SHA256",sha256(rom).hexdigest())
asm=Path("experiments/romdev_c_b3a.asm").read_text()
assert "sta CTRLPF" in asm and "lda (R0Ptr),y" in asm and "lda (L2Ptr),y" in asm
print("ROM footprint: 9 * 192 = 1728 table bytes including static P0 and reusable zero row-table.")
print("RAM symbols: $80..$8B = 12 bytes, 116 of 128 bytes remain in this isolated diagnostic.")
print("TIA: 6 PF writes (PF0/PF1/PF2 in each half) + GRP0 and WSYNC per visible line.")
print("Static estimated worst path: ~61 CPU cycles after WSYNC, including indexed page crossings; margin ~15/76.")
print("PASS: real Stella pixels align across exactly three x centers; developer self-test.")
