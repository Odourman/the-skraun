"""B1 static playfield screenshot self-test. Requires a genuine Stella PNG.
Checks a wide, symmetric, centered golden arc; NOT a full independent acceptance test.
"""
import sys
from PIL import Image

im=Image.open(sys.argv[1]).convert("RGB")
w,h=im.size
gold=set()
for y in range(h):
    for x in range(w):
        r,g,b=im.getpixel((x,y))
        if r>175 and g>130 and 40<b<145 and r>g>b:
            gold.add((x,y))
if len(gold)<150:
    raise SystemExit(f"FAIL: only {len(gold)} gold pixels")
xs=[x for x,y in gold]
ys=[y for x,y in gold]
l,r,t,b=min(xs),max(xs),min(ys),max(ys)
print("image", im.size, "gold pixels",len(gold),"bbox", (l,t,r,b))
assert (r-l+1)>=152, "ring too narrow for 32px level-3 troll"
assert 40 <= b-t+1 <= 65, "ring should be about 52 scanlines high"
assert abs((l+r)/2-(w-1)/2) <= 4, "ring not centered at visible screen center"
symmetric=sum((w-1-x,y) in gold for x,y in gold)/len(gold)
print("gold horizontal reflection agreement",symmetric)
assert symmetric>=0.95,"mirrored playfield is visibly asymmetric"
assert len(gold) < (r-l+1)*(b-t+1)*0.55,"expected hollow ring, not solid disk"
print("PASS: static P02-B1 mirrored ring is visible, large, centered and hollow in Stella")
