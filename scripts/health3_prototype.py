"""Generate isolated PR61 variants, preserving the baseline source checkout."""
from pathlib import Path
import argparse
import difflib
import re
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
parser.add_argument("variant", choices=("baseline", "color", "combined", "locked", "single"))
args = parser.parse_args()
shutil.copytree(args.source, args.destination, dirs_exist_ok=True)
b = [(args.destination / f"bank{n}.asm").read_text() for n in range(4)]
original = b.copy()

def change(bank, old, new):
    if b[bank].count(old) != 1:
        raise ValueError(f"Expected one occurrence in bank {bank}: {old!r}")
    b[bank] = b[bank].replace(old, new)

if args.variant != "baseline":
    # Bank 2 owns the persistent world color. Preserve both existing writes
    # and phase timing when halo is off; simply avoid overriding it in bank 3.
    change(2, "        bne ColorHaloActive\n", "        nop\n        nop\n")
    left = b[3].index("AttackColor:\n")
    right = b[3].index("AttackRadius:\n", left)
    b[3] = b[3][:left] + "AttackColor:\n" + b[3][right:]

if args.variant in ("combined", "locked", "single"):
    # PF table runs backwards on screen. Move each motif by 56 pairs without reversing its rows.
    start = b[3].index("PlayPF1:\n")
    end = b[3].index("; End at $FD00", start)
    area = b[3][start:end]
    values = [int(v, 16) for v in re.findall(r"\$([0-9A-F]{2})", area)]
    assert len(values) == 768
    for stage in (2, 4, 6, 8):
        n = (stage - 1) * 96
        tile = values[n:n+96]
        swapped = [0] * 96
        for i, value in enumerate(tile):
            if not value:
                continue
            dest = i + 56 if i < 48 else i - 56
            assert 0 <= dest < 96 and not swapped[dest], (stage, i, dest)
            swapped[dest] = value
        values[n:n+96] = swapped
    b[3] = b[3][:start] + "PlayPF1:\n" + "".join(
        "        dc.b " + ",".join(f"${v:02X}" for v in values[n:n+16]) + "\n"
        for n in range(0, len(values), 16)
    ) + b[3][end:]
    # Rects are top-left/top-right/bottom-left/bottom-right and use internal Y.
    for stage in (2, 4, 6, 8):
        pattern = rf"(?m)^        dc.b (.+) ; Revision 3 stage {stage},.*$"
        old = re.search(pattern, b[0])[0]
        rect = [int(v, 16) for v in re.findall(r"\$([0-9A-F]{2})", old)]
        assert len(rect) == 16
        for y in (2, 3, 6, 7):
            rect[y] += 112
        for y in (10, 11, 14, 15):
            rect[y] -= 112
        rect = rect[8:] + rect[:8]
        assert all(0 <= v < 256 for v in rect)
        change(0, old, "        dc.b " + ",".join(f"${v:02X}" for v in rect)
               + f" ; HEALTH-3 swapped stage {stage} motif rectangles")
    change(2, "        lda #$42\n        sta COLUBK", "        lda #0\n        sta COLUBK")
    start = b[2].index("        lda INPT4\n        bpl GameOverFire")
    end = b[2].index("RestartGame:\n", start)
    b[2] = b[2][:start] + "        jmp GameOverStay\n" + b[2][end:]
    start = b[3].index("GateDispatch:\n")
    end = b[3].index("GateAlive:\n", start)
    b[3] = b[3][:start] + """GateDispatch:
        lda Lives
        bne GateAlive
        lda #0
        sta $95
        sta COLUBK
        sta CTRLPF
        sta GRP0
        sta GRP1
        sta ENAM0
        sta ENAM1
        sta ENABL
        lda #$0E
        sta COLUPF
        jsr HudDraw
        ldx #187
DeadScreenLine:
        sta WSYNC
        dex
        bne DeadScreenLine
        jmp VisibleDone
""" + b[3][end:]
    start = b[3].index("GameOverMap:\n")
    end = b[3].index("HaloTracerPrepare:\n", start)
    b[3] = b[3][:start] + b[3][end:]

if args.variant == "single":
    start = b[3].index("GateDispatch:\n")
    end = b[3].index("GateAlive:\n", start)
    dead = b[3][start:end].replace("sta $95", "sta $0D").replace("jsr HudDraw", "jsr DeadHudDraw")
    b[3] = b[3][:start] + dead + b[3][end:]
    change(3, "        ORG $FF01\n", """DeadHudDraw:
        ldx #0
DeadHudRow:
        sta WSYNC
        lda $90,x
        sta PF1
        cpx #3
        bcs DeadHudTail
        lda $E9,x
        jmp DeadHudPF2
DeadHudTail:
        lda $97,x
DeadHudPF2:
        sta PF2
        lda #0
        ldy #4
DeadHudDelay:
        dey
        bne DeadHudDelay
        sta PF1
        nop
        nop
        sta PF2
        inx
        cpx #5
        bne DeadHudRow
        sta WSYNC
        rts
        ORG $FF01
""")

if args.variant == "locked":
    change(3, "        jsr MoveX\n        jsr MoveY\n", "        jsr HealthMove\n        nop\n        nop\n        nop\n")
    change(3, "HaloTracerPrepare:\n", """HealthMove:
        lda HaloFrames
        bne HealthMoveDone
        jsr MoveX
        jmp MoveY
HealthMoveDone:
        rts
HaloTracerPrepare:
""")

patch = []
for n, (old, new) in enumerate(zip(original, b)):
    (args.destination / f"bank{n}.asm").write_text(new)
    patch.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                 f"a/bank{n}.asm", f"b/bank{n}.asm"))
(args.destination / "PATCH.diff").write_text("".join(patch))
if args.variant != "baseline":
    build = args.destination / "build.py"
    build.write_text(re.sub(r'^EXPECTED = ".*"$', 'EXPECTED = ""', build.read_text(), flags=re.M))
