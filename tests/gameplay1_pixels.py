#!/usr/bin/env python3
"""Bounded developer image oracle over real Stella 6.7.1 screenshots.
No gameplay-memory injection. Does NOT certify 262 lines, enemy count, or L3.
"""
from pathlib import Path
from PIL import Image
import hashlib
import json
import numpy as np

root = Path("build/gameplay1/moving")
names = (
    "baseline", "L1_on", "pickup_L2_off", "L3_select",
    "L3_select_right8", "sword_warning", "sword_hit", "stage_progress",
)
report = {}

def bounds(mask):
    y, x = np.where(mask)
    return [int(x.min()), int(y.min()), int(x.max()) + 1, int(y.max()) + 1] if len(x) else None

for name in names:
    pic = root / name / "DEBUGGER_DESKTOP.png"
    assert pic.exists(), f"MISSING_REAL_STELLA_SCREENSHOT: {pic}"
    img = Image.open(pic).convert("RGB").crop((121, 115, 441, 343))
    img.save(root / name / "ACTUAL_STELLA_TIA.png")
    a = np.asarray(img)
    def rgb(v):
        return np.all(a == v, axis=2)
    gray = rgb((210, 210, 209))
    blue = rgb((121, 194, 251))
    gold = rgb((234, 194, 84))
    rep = {
        "P0_gray_bbox": bounds(gray), "gray_pixels": int(gray.sum()),
        "P1_blue_bbox": bounds(blue), "blue_pixels": int(blue.sum()),
        "gold_pixels": int(gold.sum()),
        "rgb_sha256": hashlib.sha256(a.tobytes()).hexdigest(),
    }
    report[name] = rep
    print(name, json.dumps(rep))
    assert rep["P0_gray_bbox"] is not None, name

def dim(v):
    b = report[v]["P0_gray_bbox"]
    return (b[2] - b[0], b[3] - b[1])

assert dim("baseline") == (16, 12), ("baseline U1 source size", dim("baseline"))
assert report["baseline"]["gray_pixels"] == 98, "baseline U1 pixel count"
assert report["baseline"]["blue_pixels"] == 120, "baseline P1 source-count"
assert report["baseline"]["gold_pixels"] == 0
assert dim("L1_on") == (16, 12)
assert report["L1_on"]["blue_pixels"] == 120, "P1 corrupt under FIRE"
assert report["L1_on"]["gold_pixels"] > 0, "missing gold PF"
assert dim("pickup_L2_off") == (32, 24), "L2 physical sprite not 32x24"
assert report["pickup_L2_off"]["gold_pixels"] == 0
assert report["pickup_L2_off"]["blue_pixels"] == 120, "P1 corrupt under orb pickup"
assert dim("sword_warning") == (16, 12)
assert report["sword_warning"]["blue_pixels"] == 0, "P1 blue remained during warning"
assert report["sword_warning"]["gold_pixels"] >= 120, "P1 warning not physically visible"
assert dim("sword_hit") == (16, 12)
assert report["sword_hit"]["blue_pixels"] == 120
# SELECT source command in two L3-named inputs did not effect a physical
# L3 upgrade in earlier runs. Fail closed: never claim L3 test PASS.
if dim("L3_select") != (64, 36) or dim("L3_select_right8") != (64, 36):
    print("L3_SELECT_NOT_VERIFIED: physical SELECT inputs did not reach L3; scope remains OPEN")
else:
    print("L3_SELECT_PHYSICAL_SIZE_MEASURED: check pose and navigation separately")
print("GAMEPLAY1_BOUNDED_DEVELOPER_OBSERVED: real Stella P0 L1/L2, P1, FIRE and sword warning; no complete gameplay PASS")
(root / "GAMEPLAY1_TIA_PIXEL_AUDIT.json").write_text(json.dumps(report, indent=2))
