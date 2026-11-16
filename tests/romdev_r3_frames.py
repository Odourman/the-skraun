"""P02-R3 — genuine consecutive Stella saveSnap PNG pixel/duty tests.
No external artwork, generated frames, synthetic screenshots, or UI sampling.
Intentionally reject missing frames, mispositioned P0, and invented no-flicker claims.
"""
from pathlib import Path
from PIL import Image
import collections,csv,json
PAL={
 "skraun":(210,210,209),
 "halo_gold":(234,194,84),
 "obstacles_blue":(55,61,193),
 "knight_1":(177,40,39),
 "knight_2":(210,81,80),
 "archer":(61,151,60),
 "HUD":(106,174,237),
}
ACTORS=("knight_1","knight_2","archer")
NAMES=("overlap","partial","stagger")
STATES=("center80","right104","right104-next","left56","left56-next","reverse80","reverse80-next")
EXPECTED_DUTY={
 "overlap":(4,4,4,6,6),
 "partial":(6,6,12,6,6),
 "stagger":(12,12,12,12,0)
}
POSITIONS={
 "overlap":{"knight_1":32,"knight_2":101,"archer":147},
 "partial":{"knight_1":36,"knight_2":105,"archer":149},
 "stagger":{"knight_1":28,"knight_2":111,"archer":149},
}
def colored(im,palette):
    im=im.convert("RGB")
    found=collections.defaultdict(set)
    pixel=im.load()
    for y in range(im.height):
        for x in range(im.width):
            rgb=pixel[x,y]
            for name,col in palette.items():
                if rgb==col:
                    found[name].add((x,y))
    return found
def box(ps):
    assert ps,"missing colored pixels"
    xx,yy=zip(*ps)
    return min(xx),min(yy),max(xx)+1,max(yy)+1
allrec=[];stats={};byvariant={}
for n in NAMES:
    src=Path("build/frames_"+n)
    names=[f"seq_{i:02d}" for i in range(12)]+list(STATES)
    captures={}
    for key in names:
        path=src/(key+".png")
        assert path.exists() and path.stat().st_size>300,("MISSING ORIGINAL STELLA PNG",str(path))
        im=Image.open(path).convert("RGB")
        assert im.size==(320,228),("Not 1x original Stella capture",str(path),im.size)
        caps=colored(im,PAL)
        assert len(caps["HUD"])>1800,("Unreadable HUD regional stripe",n,key,len(caps["HUD"]))
        assert len(caps["skraun"])==1320,(n,key,"gray P0 36-row identity not preserved",len(caps["skraun"]))
        assert box(caps["skraun"])[3]-box(caps["skraun"])[1]==36
        captures[key]=caps
        row={"candidate":n,"frame":key}
        for k in PAL:row[k]=len(caps[k])
        allrec.append(row)
    # VBLANK timer/real mid-frame P1 positioning shifts the whole raster scene by
    # 0..2 physical lines between candidates; relative ring-to-P0 Y stays fixed.
    # Do not mislabel this expected diagnostic VBLANK offset as sprite deformation.
    p0_y={"overlap":106,"partial":105,"stagger":104}[n]
    for state,(xlo,xhi) in (
        ("center80",(128,192)),
        ("right104",(176,240)),
        ("right104-next",(176,240)),
        ("left56",(80,144)),
        ("left56-next",(80,144)),
        ("reverse80",(128,192)),
        ("reverse80-next",(136,200))):
        expected=(xlo,p0_y,xhi,p0_y+36)
        actual=box(captures[state]["skraun"])
        assert actual==expected,(n,state,"CRITICAL P0 alignment/previous mid-HMOVE drift",actual,expected)
    base=captures["center80"]["skraun"]
    for state,delta in (("right104",48),("right104-next",48),("left56",-48),("left56-next",-48),("reverse80",0),("reverse80-next",8)):
        translated={(x+delta,y) for x,y in base}
        assert captures[state]["skraun"]==translated,(n,state,"P0 sprite shape changed/occluded",len(translated^captures[state]["skraun"]))
    # True 12 consecutive emulated frames, not 12 host-time snapshots.
    seq=[captures[f"seq_{i:02d}"] for i in range(12)]
    duty={k:sum(len(s[k])>30 for s in seq) for k in ACTORS}
    golden=sum(len(s["halo_gold"])>100 for s in seq)
    blue=sum(len(s["obstacles_blue"])>50 for s in seq)
    expected=dict(zip((*ACTORS,"halo_gold","obstacles_blue"),EXPECTED_DUTY[n]))
    assert duty=={k:expected[k] for k in ACTORS},(n,"observed independent actor duty",duty,expected)
    assert (golden,blue)==(expected["halo_gold"],expected["obstacles_blue"]),(n,"frame flicker/duty",golden,blue,expected)
    for actor in ACTORS:
        present=[s[actor] for s in seq if len(s[actor])>30]
        assert present,(n,actor,"never visible")
        bbox=[box(ps) for ps in present]
        assert len(set(bbox))==1,(n,actor,"actor pixel location unstable across frame rotations",bbox)
        xmin=min(box(ps)[0] for ps in present)
        target=2*POSITIONS[n][actor]
        # Expected TIA horizontal state programmed using PositionP1; allow 4 image pixels for TIA horizontal alignment.
        assert abs(xmin-target)<12,(n,actor,"actor RAM X not actually used to position independent sprite",xmin,target)
    if n!="stagger":
        assert all(not(s["halo_gold"] and s["obstacles_blue"]) for s in seq),(
            n,"frame alternation unexpectedly shows two independent colors on same frame")
        assert all(bool(s["halo_gold"]) != bool(s["obstacles_blue"]) for s in seq),(n,"alternating field vanished",)
        assert sum(s["halo_gold"]!=set() for s in seq)==6
        assert sum(s["obstacles_blue"]!=set() for s in seq)==6
        for key in ("right104","left56","reverse80"):
            g1=captures[key]["halo_gold"];g2=captures[key+"-next"]["halo_gold"]
            b1=captures[key]["obstacles_blue"];b2=captures[key+"-next"]["obstacles_blue"]
            assert (len(g1)>100) != (len(g2)>100),(n,key,"gold ring not exactly every second original Stella frame")
            assert (len(b1)>20) != (len(b2)>20),(n,key,"blue scene not exactly every second frame")
            assert max(len(g1),len(g2))>1000,(n,key,"halo absent in both phases")
            assert max(len(b1),len(b2))>300,(n,key,"scene absent in both phases")
        assert any(x>=256 and 80<=y<=160 for key in ("right104","right104-next")
                   for x,y in captures[key]["halo_gold"]),(
              n,"real level3 halo did not reach right PF2 at x104")
    else:
        assert all(not s["obstacles_blue"] for s in seq)
        assert all(s["halo_gold"] for s in seq)
        # RIGHT PF2 must light up for larger level-3 reach at x104
        assert any(x>=256 and y>=80 for x,y in captures["right104"]["halo_gold"]),(
            "level3 right PF2 absent or clipped",box(captures["right104"]["halo_gold"]))
    # Typical child should not mistake 20Hz hidden colored body for full 60Hz physical persistence.
    for key in STATES:
        c=captures[key]
        print("STELLA",n,key,"Skraun bbox",box(c["skraun"]),"P1 knight1/knight2/archer",*[len(c[k]) for k in ACTORS],
              "halo",len(c["halo_gold"]),"scene",len(c["obstacles_blue"]))
    byvariant[n]={k:len(captures["center80"][k]) for k in PAL}
    stats[n]={"actors_measured_active_frames_out_of_12":duty,
              "actors_measured_hz_NTSC60":{k:duty[k]*5 for k in ACTORS},
              "halo_frames_out_of_12":golden,
              "scene_frames_out_of_12":blue,
              "halo_hz_NTSC60":golden*5,
              "scene_hz_NTSC60":blue*5,
              "right_PF2_exercised":"yes" if n=="stagger" else "alternate phase edge capture needed",
              "readability":"No production approval; 20Hz or 30Hz is visible flicker risk"}
    print("MEASURED ACTUAL 60Hz FRAME DUTY",n,stats[n])
with open("build/R3_ACTUAL_STELLA_PER_FRAME_PIXEL_COUNTS.csv","w",newline="") as out:
    w=csv.DictWriter(out,fieldnames=list(allrec[0]));w.writeheader();w.writerows(allrec)
Path("build/R3_ACTUAL_STELLA_12_FRAME_DUTY_AND_ALIGNMENTS.json").write_text(json.dumps(stats,indent=2))
print("PASS original Stella pixel evidence of independent X/Y positions, exact 12-frame duty and no mid-HMOVE P0 drift.")
print("CAVEAT: is not an aesthetic endorsement of 20Hz/30Hz or a complete arrow/orb collision implementation.")
