#!/usr/bin/env python3
"""Corrected HEALTH-1 ownership gate: SOURCE_ONLY, no beam/gameplay proof."""
from pathlib import Path
import hashlib,re,json
R=Path(__file__).resolve().parents[1]
P=R/"experiments/fullgame1_arrow_halo_20261125"
a=[(P/f"bank{i}.asm").read_text() for i in range(4)]
checks={}
checks["TIA_002_correct"] = bool(re.search(r"HaloBLWidths:\s*\n\s*dc.b \$00,\$10,\$20,\$30",a[2]))
checks["no_HEALTH_002_inversion"] = not bool(re.search(r"HaloBLWidths:\s*\n\s*dc.b \$00,\$20,\$10,\$30",a[2]))
checks["odd_even_REF"] = "lda Stage\n        and #1\n        ora HaloBLWidths,x\n        sta CTRLPF" in a[2]
checks["no_select_audio_alias"] = "PrevSelect" not in a[3] and "SoundReq1 = $85" in a[1] and "ora #$80" in a[3]
checks["phase_masks"] = "and #$03\n        cmp #3" in a[3] and "and #$03\n        cmp #2" in a[3]
tracer=a[3].split("HaloTracerPrepare:",1)[1].split("TracerBudgetCheck:",1)[0]
checks["no_tracer_HUD_EB"] = "sta $96" in tracer and "sta $EB" not in tracer
checks["render_height_dead_87"] = "sta $87" in a[1] and "sbc $87" in a[3]
for stage in range(1,9):
 for level in (1,2,3):
  reg=(level<<4)|(stage&1)
  assert (reg&1)==(stage&1) and (1<<((reg>>4)&3))==(1<<level)
OUT=R/"build/arrow_halo_romdev4"
rom=(OUT/"THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin").read_bytes()
sha=hashlib.sha256(rom).hexdigest()
checks["actual_ROM_SHA"] = len(rom)==16384 and sha=="83f35c6d1c24be9391a845d377b4d24ee9d2b20647ca5f993d3cb54e646acbfa"
result={"classification":"SOURCE_ONLY_WITH_REAL_DASM_MANIFEST","checks":checks,"pass":all(checks.values()),"SHA256":sha}
(OUT/"MAINV_HEALTH_CORRECTED_TESTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
if not result["pass"]:raise SystemExit("HEALTH_MAINV_TEST_FAIL")
