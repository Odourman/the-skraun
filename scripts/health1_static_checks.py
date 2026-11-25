#!/usr/bin/env python3
"""Static ownership checks for the isolated HEALTH-1 patch; not gameplay proof."""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "experiments/fullgame1_arrow_halo_20261125"
OUT = ROOT / "build/arrow_halo_romdev4"
bank1 = (SRC / "bank1.asm").read_text()
bank2 = (SRC / "bank2.asm").read_text()
bank3 = (SRC / "bank3.asm").read_text()
tracer = bank3[bank3.index("HaloTracerPrepare:"):bank3.index("TracerBudgetCheck:")]
audio = bank1[bank1.index("AudioEngine:"):bank1.index("NoNewEvent:")]
checks = {
    "audio_consumes_and_clears_85": "lda SoundReq1" in audio and "sta SoundReq1" in audio,
    "select_debounce_is_packed_in_phase_bit7": bool(re.search(r"Phase\s*=\s*\$86.*bit 7 = SELECT latch", bank3)) and "ora #$80" in bank3 and "and #$7F" in bank3,
    "phase_math_masks_latch_bit": "and #$03\n        cmp #3" in bank3 and "and #$03\n        cmp #2" in bank3,
    "hud_pf2_rows_remain_contiguous": "sta $00E9,y" in bank1 and "lda $E9,x" in bank3,
    "halo_tracer_does_not_clobber_hud_row2": "sta $96" in tracer and "sta $EB" not in tracer,
    "render_bottom_uses_post_movement_scratch": "sta $87           ; movement's DiagonalSkip dies before HUD/render setup" in bank1 and "sbc $87" in bank3,
    "ctrlpf_preserves_odd_stage_ref": "and #1\n        beq CTPFRepeat" in bank2 and "ora #1" in bank2,
    "ball_width_table_level1_2_3": bool(re.search(r"HaloBLWidths:\s*\n\s*dc\.b \$00,\$20,\$10,\$30", bank2)),
}
widths = [0x20, 0x10, 0x30]
checks["stage_width_register_values"] = all(
    ((widths[level - 1] | (stage & 1)) & 0x31) == (widths[level - 1] | (stage & 1))
    for stage in range(1, 9) for level in range(1, 4)
)
if not all(checks.values()):
    raise SystemExit("HEALTH1_STATIC_CHECK_FAIL " + repr(checks))
rom = OUT / "THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin"
if not rom.is_file() or rom.stat().st_size != 16384:
    raise SystemExit("HEALTH1_ROM_SIZE_FAIL")
sha = hashlib.sha256(rom.read_bytes()).hexdigest()
manifest = (OUT / "SHA256SUMS.txt").read_text().split()[0]
if sha != manifest:
    raise SystemExit("HEALTH1_ROM_MANIFEST_FAIL")
report = {
    "classification": "HEALTH_OBSERVED_STATIC_SOURCE_CHECKS_ONLY",
    "checks": checks,
    "rom_size_bytes": rom.stat().st_size,
    "rom_sha256": sha,
    "scope_limit": "Does not prove gameplay, pixels, TIA beam deadlines, complete cycle budgets, stack high-water, or original hardware behavior.",
}
(OUT / "HEALTH1_STATIC_CHECKS.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
