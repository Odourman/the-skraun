"""R2 genuine Stella PNG-only geometry and draw-slot assessment.
Candidate failures are faithfully recorded, never turned into a success.
"""
from PIL import Image
from pathlib import Path
import json,csv,collections
NAMES=("baseline","twoline","dual","hud","interlace")
STATES=("centre80","centre104","centre56","reverse")
def is_gray(p):
    r,g,b=p
    return min(p)>105 and max(p)-min(p)<28
def is_gold(p):
    r,g,b=p
    return r>175 and g>120 and 32<b<155 and r>g>b
def is_green(p):
    r,g,b=p
    return g>65 and g>r*1.15 and g>b*1.07
def pixels(im,pred):
    return {(x,y) for y in range(im.height) for x in range(im.width) if pred(im.getpixel((x,y)))}
def box(ps):
    if not ps:return None
    xs,ys=zip(*ps)
    return min(xs),min(ys),max(xs)+1,max(ys)+1
images={}; rec=[]
for n in NAMES:
    for state in STATES:
        p=Path("build")/(n+"-"+state+".png")
        assert p.exists() and p.stat().st_size>200,"MISSING genuine Stella screenshot: "+str(p)
        im=Image.open(p).convert("RGB")
        assert im.width==320 and im.height in (192,228),("not original x1 Stella NTSC image",n,state,im.size)
        images[n,state]=im
        gr=pixels(im,is_gray);au=pixels(im,is_gold);ge=pixels(im,is_green)
        bb=box(gr);gb=box(au)
        assert bb and len(gr)>100,("gray Skraun missing from actual frame",n,state)
        assert bb[2]-bb[0]==32 and bb[3]-bb[1]==24,("P0 visible geometry corrupted",n,state,bb)
        # True two-line P0 order does not depend on P1.
        row=[len([x for x,y in gr if y==yy]) for yy in range(bb[1],bb[3])]
        if n in ("baseline","twoline","dual","interlace","hud"):
            assert bb[1]==99,("P0 dropped or shifted",n,state,bb)
        # HUD consumes the original empty top 16 scanlines; arena sprite Y stays fixed.
        rec.append({"candidate":n,"state":state,"gray_count":len(gr),"gray_bbox":bb,"gold_count":len(au),"gold_bbox":gb,"p1_green_count":len(ge),"p1_green_bbox":box(ge),"P0_shape_each_line":row})
        print(f"GENUINE STELLA {n:8s} {state:9s}: P0{bb}, PF gold {gb} {len(au)}pix, P1 green {box(ge)} {len(ge)}pix")
# Pixel error against one-line original, ring+scene same center.
for state in STATES:
    a=images["baseline",state];b=images["twoline",state]
    ga=pixels(a,is_gray);gb=pixels(b,is_gray)
    assert ga==gb,("two-line P0 must retain ALL 24 individual physical sprite rows",state,len(ga^gb))
    ua=pixels(a,is_gold);ub=pixels(b,is_gold)
    delta=len(ua^ub);jaccard=len(ua&ub)/max(1,len(ua|ub))
    # Compare P0 exactness across both altered PF schedules, not just the first.
    gl=pixels(images["interlace",state],is_gray)
    assert ga==gl,("two-line interlace must preserve every P0 pixel row",state,len(ga^gl))
    print("TWO-LINE QUALITY",state,"gold symmetric diff",delta,"union",len(ua|ub),"IoU",round(jaccard,5))
    assert jaccard>0.70,("two-line PF ring/synthetic scene badly deformed",state,jaccard)
# R2 dualcopy: two actual green P1 copies with distinct row silhouettes.
dual_status=[]
for state in STATES:
    im=images["dual",state]
    ge=pixels(im,is_green)
    left={(x,y) for x,y in ge if 95<=x<=151}
    right={(x,y) for x,y in ge if 228<=x<=278}
    # Compare normalized bitmap shapes; do not mistake the copy's X offset
    # for two independently authored sprites.
    def local_shape(ps):
        if not ps:return set()
        x0=min(x for x,y in ps);y0=min(y for x,y in ps)
        return {(x-x0,y-y0) for x,y in ps}
    present=len(left)>25 and len(right)>25
    distinct=local_shape(left)!=local_shape(right)
    dual_status.append({"state":state,"first_green_pixels":len(left),"second_green_pixels":len(right),"both_present":present,"different_bitmaps":distinct})
    print("SAME-Y P1 DUALCOPY",state,"left",len(left),"right",len(right),"BOTH",present,"DIFFERENT",distinct)
# Interlace has intentionally sacrificed every other vertical halo/scene row.
for state in STATES:
    baseGold=pixels(images["baseline",state],is_gold)
    r2Gold=pixels(images["interlace",state],is_gold)
    assert len(r2Gold)>100,("interlaced halo disappeared",state)
    print("INTERLACE RING DUTY",state,"gold rows/pixels",len(r2Gold),"baseline",len(baseGold),"ratio",round(len(r2Gold)/len(baseGold),3))
hud=images["hud","centre80"]
# Stella 320x228 output places first active visible HUD line at y=30.
bar=[hud.getpixel((x,y)) for y in range(30,46) for x in range(0,320)]
lit=sum(max(v)>70 for v in bar)
print("SEPARATE HUD PLACEHOLDER first 16 active display rows (y30..45) nonblack pixel count",lit)
assert lit>100,("HUD region was not actually drawn",lit)
with open("build/R2_GENUINE_IMAGE_GEOMETRY.json","w") as f:
    json.dump({"stella_pngs":rec,"two_enemy_copies":dual_status,"hud_nonblack_pixels":lit},f,indent=2)
with open("build/R2_GENUINE_IMAGE_GEOMETRY.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rec[0]));w.writeheader();w.writerows(rec)
print("R2 genuine Stella image test completed. Dualcopy status is reported, not automatically accepted.")
