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
assert 88 <= (r-l+1) <= 124, "expected 44–62 logical pixel ring wider than 32px troll"
assert 72 <= b-t+1 <= 96, "ring should be approximately 84 scanlines high"
assert abs((l+r)/2-(w-1)/2) <= 4, "ring not centered at visible screen center"
symmetric=sum((w-1-x,y) in gold for x,y in gold)/len(gold)
print("gold horizontal reflection agreement",symmetric)
print("display aspect ratio",round((r-l+1)/(b-t+1),3))
assert (r-l+1)/(b-t+1) < 1.55,"ring looks unnaturally flattened on Stella screenshot"
assert symmetric>=0.95,"mirrored playfield is visibly asymmetric"
assert len(gold) < (r-l+1)*(b-t+1)*0.58,"expected hollow ring, not solid disk"
print("PASS: static P02-B1 mirrored ring is visible, large, centered and hollow in Stella")
