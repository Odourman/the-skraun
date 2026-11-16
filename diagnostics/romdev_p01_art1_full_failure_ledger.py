#!/usr/bin/env python3
"""P01-ART1 bounded FINAL diagnostic of all native, original Stella screenshots.
Continues across technical failures, unlike strict tests/romdev_p01_art1_stella.py.
Consumes existing untouched A/B/Q1 source JSON and original 320x228 PNGs.
A result with any pixel mismatches is TECHNICAL FAIL, never forced green.
"""
import csv,json,hashlib,pathlib,collections
from PIL import Image
B=pathlib.Path("build")
p1=json.loads(pathlib.Path("experiments/romdev_p01_art1_exact_P1_masks.json").read_text())
q=json.loads(pathlib.Path("experiments/romdev_p01_art1_exact_Q1_v03.json").read_text())
names=("A_rounded_back","B_low_long_back","Q1_splayed_quad")
colors=(210,210,209)
data=[]
walk=[]
for n in names:
    o=p1["baseline_Q1"] if n=="Q1_splayed_quad" else p1["candidates"][n]
    if n=="Q1_splayed_quad":
        for pose in "AB":
            for side in ("right","left"):
                oldkey=pose if side=="right" else pose+"_left"
                qkey=pose if side=="right" else "left_"+pose
                assert o[oldkey]==q["new_attempts"]["Q1_splayed_quad"][qkey]
    for stage in range(6):
        lev=stage//2+1;facing="left" if stage%2 else "right"
        rep=[1,2,3][lev-1];scale=[1,2,4][lev-1]
        x0={1:146,2:140,3:124}[lev]
        y0={1:106,2:100,3:94}[lev]
        for pose in "AB":
            key=pose if facing=="right" else (pose+"_left" if n=="Q1_splayed_quad" else "left_"+pose)
            src=o[key]
            assert len(src)==12 and all(len(r)==8 for r in src)
            imgpath=B/f"frames_{n}"/f"state_{stage}_{pose}.png"
            im=Image.open(imgpath).convert("RGB")
            assert im.size==(320,228)
            actual={(x,y) for y in range(228) for x in range(320) if im.getpixel((x,y))==colors}
            expected={(x0+bit*2*scale+dx,y0+row*rep+dy)
                      for row,word in enumerate(src)
                      for bit,c in enumerate(word) if c=="1"
                      for dy in range(rep) for dx in range(scale*2)}
            extra=actual-expected; missing=expected-actual
            # Reconstruct original native image rows; do not infer from data only.
            reconstructed=[]
            for row in range(12):
                bits=""
                for bit in range(8):
                    count=sum((x0+bit*2*scale+dx,y0+row*rep+dy) in actual
                              for dy in range(rep) for dx in range(scale*2))
                    bits+="1" if count>0 else "0"
                reconstructed.append(bits)
            diffrows=sorted({y for x,y in extra|missing})
            record={"candidate":n,"level":lev,"pose":pose,"facing":facing,"state":f"state_{stage}_{pose}",
                    "expected_exact":len(expected),"observed_gray":len(actual),
                    "extra_pixels":len(extra),"missing_pixels":len(missing),
                    "pixel_diff_total":len(extra)+len(missing),"different_scanline_y":",".join(map(str,diffrows)),
                    "top_first_expected":src[0],"top_first_observed":reconstructed[0],
                    "bottom_last_expected":src[-1],"bottom_last_observed":reconstructed[-1],
                    "status":"PASS" if not (extra or missing) else "FAIL",
                    "png_sha256":hashlib.sha256(imgpath.read_bytes()).hexdigest()}
            data.append(record)
    # 24 consecutive original emulator frames, 14 A and 10 B, every 8 frame cadence
    for k in range(24):
        src=o["A" if ((2+k)//8)%2==0 else "B"]
        path=B/f"frames_{n}"/f"walk_{k:02d}.png"
        im=Image.open(path).convert("RGB")
        actual={(x,y) for y in range(228) for x in range(320) if im.getpixel((x,y))==colors}
        exp={(146+bit*2+dx,106+row) for row,word in enumerate(src) for bit,c in enumerate(word) if c=="1" for dx in range(2)}
        walk.append({"candidate":n,"frame":k,"pose_expected":"A" if ((2+k)//8)%2==0 else "B","exact_raster_match":actual==exp,"actual_png":str(path)})
assert len(data)==36 and len(walk)==72
assert sum(s["status"]=="PASS" for s in data)==24
assert sum(s["status"]=="FAIL" for s in data)==12
assert all(s["status"]=="FAIL" for s in data if s["level"]==3)
assert all(s["status"]=="PASS" for s in data if s["level"]<3)
assert all(w["exact_raster_match"] for w in walk)
assert {int(s["different_scanline_y"].split(",")[0]) for s in data if s["status"]=="FAIL"}=={94}
assert all(len(s["different_scanline_y"].split(","))==1 for s in data if s["status"]=="FAIL")
assert all(s["missing_pixels"]==0 for s in data if s["status"]=="FAIL")
assert sorted([s["extra_pixels"] for s in data if s["status"]=="FAIL"])==[48]*8+[64]*4
assert all(s["top_first_observed"]=="11111111" for s in data if s["status"]=="FAIL")
assert all(s["top_first_observed"]==s["top_first_expected"] for s in data if s["level"]<3)
neg=p1["candidates"]["A_rounded_back"]["A"]
assert sum(a!=b for a,b in zip("".join(neg),"".join(neg[::-1])))==4
with open(B/"P01_ART1_ALL_36_GENUINE_STELLA_PIXEL_STATUS.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
with open(B/"P01_ART1_72_GENUINE_STELLA_GAIT_FRAMES.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(walk[0]));w.writeheader();w.writerows(walk)
summary={
  "test_type":"genuine Stella 6.7.1 320x228 PNG pixel data, NOT source-only",
  "exact_p0_states_passed":24,"states_failed":12,"states_total":36,
  "all_level3_states_fail":"one 64 native pixel wide spurious fully lit top scanline",
  "failure_y_original_png":94,
  "total_extra_gray_pixels_level3":{"A_rounded_back":48,"B_low_long_back":64,"Q1_splayed_quad":48},
  "other_level3_scanlines_match_all_original_bitmaps":True,
  "sequential_walk_frames_passed":72,
  "primary_A_pose_A_vertical_inversion_diff_cells":4,
  "strict_test_verdict":"TECHNICAL FAIL, not waived",
  "art_identity":"NOT ACCEPTED; user/MAIN must decide",
  "full_scene_architecture":"R3 NO-GO unchanged"}
(B/"P01_ART1_FINAL_DIAGNOSTIC_SUMMARY.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
print("Complete 36-row ledger produced; hardware rendering FAIL persists in level3. No source art altered.")
