#!/usr/bin/env python3
"""MAIN-authorized R3-VFIX: compare genuine pre-fix and post-fix Stella 6.7.1 PNGs.
Critically tests each of 12 asymmetric 8-bit head-to-feet rows on actual GRP0 pixels.
Must FAIL original and PASS corrected for all 19 frames x 3 variants.
Also proves assembled ROM delta contains *only* reversed 36 active Troll3 bytes.
R3 enemy silhouettes, synthetic obstacle columns, HUD remain unapproved placeholders.
"""
import argparse, hashlib, json, pathlib, re, sys
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument("--old", default="before")
parser.add_argument("--new", default="build")
args=parser.parse_args()
old=pathlib.Path(args.old); new=pathlib.Path(args.new)
names=("overlap","partial","stagger")
states=[f"seq_{i:02d}" for i in range(12)]+["center80","right104","right104-next",
       "left56","left56-next","reverse80","reverse80-next"]
gray=(210,210,209)
# Exact top-first logical bitmap from MAIN's authoritative
# docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md (original approved-source prototype).
topfirst=(0x24,0x7E,0x7E,0x5A,0x7E,0xFD,0x9D,0x3C,0x7E,0x64,0x46,0xC2)
# 1 P0 source bit expands to 4 TIA color clocks = 8 original Stella 320px pixels.
# 1 logical bitmap row = 3 physical 60Hz NTSC scanlines in level 3.
pixel_width=8; row_rep=3
expected_pixels=sum(v.bit_count() for v in topfirst)*pixel_width*row_rep
assert expected_pixels==1320
results={}
for name in names:
    bin_before=old/("r3-"+name+".bin")
    bin_after=new/("r3-"+name+".bin")
    b0,b1=bin_before.read_bytes(),bin_after.read_bytes()
    assert len(b0)==len(b1)==4096,(name,"wrong ROM length")
    symfile=new/("r3-"+name+".sym")
    syms=symfile.read_text()
    mm=re.search(r"^Troll3\s+([0-9a-fA-F]{4})\b",syms,re.M)
    assert mm,(name,"assembler symbol Troll3 missing")
    offset=int(mm.group(1),16)-0xF000
    assert 0<=offset<4096-177
    prior=b0[offset:offset+177]; fixed=b1[offset:offset+177]
    assert prior[:66]==fixed[:66] and prior[102:]==fixed[102:],(name,"modified out-of-scope troll rows")
    assert prior[66:102][::-1]==fixed[66:102],(name,"not exact active 36-byte row reversal")
    assert prior[99:102]==bytes((0xC2,)*3) and fixed[99:102]==bytes((0x24,)*3),(name,"head not top")
    assert prior[66:69]==bytes((0x24,)*3) and fixed[66:69]==bytes((0xC2,)*3),(name,"feet not bottom")
    delta=[j for j,(a,b) in enumerate(zip(b0,b1)) if a!=b]
    assert delta and all(offset+66<=j<offset+102 for j in delta),(name,"non-P0 ROM change",delta[:10])
    rows_p0=0
    per_variant=[]
    for state in states:
        oldpath=old/("frames_"+name)/(state+".png")
        newpath=new/("frames_"+name)/(state+".png")
        assert oldpath.is_file() and newpath.is_file(),("Missing authentic Stella capture",name,state)
        i0=Image.open(oldpath).convert("RGB")
        i1=Image.open(newpath).convert("RGB")
        assert i0.size==i1.size==(320,228),(name,state,"wrong native screenshot dimensions")
        def inspect(im):
            px=im.load()
            g={(x,y) for y in range(228) for x in range(320) if px[x,y]==gray}
            assert len(g)==1320,(name,state,"P0 pixel count changed",len(g))
            xmin=min(x for x,y in g); xmax=max(x for x,y in g)
            ymin=min(y for x,y in g); ymax=max(y for x,y in g)
            assert xmax-xmin+1==64 and ymax-ymin+1==36,(name,state,"level3 size changed")
            bitmap=[]
            # Every genuine pixel in each 8×3 expanded source cell, not only a bounding box.
            for k in range(12):
                packed=0
                for bit in range(8):
                    cell={(xmin+bit*8+dx,ymin+k*3+dy) for dx in range(8) for dy in range(3)}
                    occupied={(x,y) for x,y in cell if px[x,y]==gray}
                    assert len(occupied) in (0,24),(name,state,k,bit,"partial/tearing gray row",len(occupied))
                    if occupied:packed|=1<<(7-bit)
                bitmap.append(packed)
            return {"x":xmin,"y":ymin,"bitmap":tuple(bitmap),"gray":g}
        pre=inspect(i0); post=inspect(i1)
        # The old original ROM should ALWAYS fail the new top/head requirement.
        assert pre["bitmap"]!=topfirst,(name,state,"ORIGINAL unexpectedly passes new orientation contract")
        assert pre["bitmap"]==topfirst[::-1],(name,state,"frozen original did not show expected reversal",pre["bitmap"])
        assert post["bitmap"]==topfirst,(name,state,"FIXED genuine Stella pixels not head-first",post["bitmap"])
        assert (pre["x"],pre["y"])==(post["x"],post["y"]),(name,state,"player moved; VFIX scope exceeded")
        rows_p0+=1
        per_variant.append({"state":state,"old_top":f"{pre['bitmap'][0]:02X}",
                            "fixed_top":f"{post['bitmap'][0]:02X}",
                            "old_bottom":f"{pre['bitmap'][-1]:02X}",
                            "fixed_bottom":f"{post['bitmap'][-1]:02X}",
                            "x":post["x"],"y":post["y"]})
    # Center/right/left/reversal are explicitly covered, no single-image cherry-picking.
    assert len(per_variant)==19
    results[name]={"actual_old_stella_cases_that_fail_new_upright_contract":rows_p0,
                   "actual_fixed_stella_cases_that_pass_new_upright_contract":rows_p0,
                   "new_rom_sha256":hashlib.sha256(b1).hexdigest(),
                   "old_rom_sha256":hashlib.sha256(b0).hexdigest(),
                   "emitted_rom_byte_differences":len(delta),"troll3_offset":offset,
                   "per_frame":per_variant,
                   "enemy_images":"temporary 8-byte test silhouettes, not approved knight/archer art",
                   "obstacle_columns":"synthetic diagnostic, not actual scenery",
                   "HUD":"placeholder, not final HUD"}
    print("REAL STELLA UPRIGHT PASS",name,"old FAIL 19/19, fixed PASS 19/19",
          "Troll3 old TOP C2 fixed TOP 24 / old FOOT 24 fixed FOOT C2",
          "new ROM SHA",results[name]["new_rom_sha256"],"binary bytes changed",len(delta))
p=new/"R3_VFIX_ORIGINAL_FAIL_FIXED_PASS_PIXEL_ORIENTATION.json"
p.write_text(json.dumps(results,indent=2))
print("PASS 57/57 real old images FAIL head-above-feet; 57/57 real corrected images PASS.")
print("PASS all 3 ROMs differ in P0 active-row bytes only; unchanged location, all head and foot pixels checked.")
print("PLACEHOLDERS: enemy sprites unapproved; obstacle columns synthetic; HUD dummy; forests, mountains, dreams, night artwork NOT IMPLEMENTED.")
print("R3 original technical NO-GO remains, not upgraded by VFIX.")
