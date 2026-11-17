"""P02-B2 visual checks of real Stella PNGs, not a complete independent review."""
from PIL import Image
from pathlib import Path

def bounds(im, kind):
    pts=[]
    for y in range(im.height):
        for x in range(im.width):
            r,g,b=im.getpixel((x,y))
            if kind=="green" and g>110 and g>r*1.5 and g>b*1.5:
                pts.append((x,y))
            if kind=="gold" and r>175 and g>130 and 40<b<145 and r>g>b:
                pts.append((x,y))
    if len(pts)<20:
        raise AssertionError("not enough "+kind+" pixels")
    x=[p[0] for p in pts];y=[p[1] for p in pts]
    return (min(x),min(y),max(x),max(y)),len(pts)

last_width=0
for level,(expected_w,expected_h) in enumerate([(16,12),(32,24),(64,36)],1):
    path=Path(f"build/p02_b2_level{level}.png")
    im=Image.open(path).convert("RGB")
    gb,np=bounds(im,"green")
    rb,nr=bounds(im,"gold")
    gw=gb[2]-gb[0]+1;gh=gb[3]-gb[1]+1
    rw=rb[2]-rb[0]+1;rh=rb[3]-rb[1]+1
    print(f"LEVEL {level} screenshot={im.size} P0 troll={gb} {gw}x{gh} gold PF halo={rb} {rw}x{rh} green={np} gold={nr}")
    assert (gw,gh)==(expected_w,expected_h),f"wrong sprite size: {gw}x{gh}"
    assert rw>gw and rh>gh, "halo must extend outside troll silhouette"
    assert rb[0]<gb[0] and rb[2]>gb[2] and rb[1]<gb[1] and rb[3]>gb[3], "ring does not surround troll envelope"
    assert abs((rb[0]+rb[2])/2-(gb[0]+gb[2])/2)<=8, "centers too far apart"
    assert rw>last_width, "halo width must increase with level"
    assert np>60 and nr>100
    last_width=rw
print("PASS P02-B2: real Stella three levels display distinct P0 troll sizes, larger enclosing rings")
