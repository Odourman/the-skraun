#!/usr/bin/env python3
"""FULLGAME-1: reproducible 16 KiB F6 bootstrap from exact frozen GAMEPLAY-5.
No graphics or combat success is implied by a larger ROM.
The original F8 game banks are F6 banks 2/3 (hotspots $1FF8/$1FF9).
"""
from pathlib import Path
import hashlib, subprocess
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "fullgame1"
OUT.mkdir(parents=True, exist_ok=True)
SRC = ROOT / "experiments"
EXPECTED = "b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca"
original = (SRC/"gameplay5_f8_ntsc.bin").read_bytes()
assert len(original) == 8192 and hashlib.sha256(original).hexdigest() == EXPECTED, "Frozen checkpoint modified"
# F6 bank 0 is reserved for future gameplay/world renderer and bank 1 for HUD/AI.
# Cold entry in either extra bank safely returns to the original graphics/reset bank.
def extra_bank(n):
    return f"""        processor 6502
        ORG $F000
F6B{n}Cold:
        lda $FFF9
        jmp $F000
        ORG $FFFC
        dc.w F6B{n}Cold
        dc.w F6B{n}Cold
"""
from fullgame1_world_renderer_patch import patch_bank0, patch_bank2 as safety_bank2, patch_bank3 as stage_render_bank3
from fullgame1_hud_patch import bank0 as hud_bank0, bank1 as hud_bank1, bank3 as hud_bank3, gameover_bank2, gameover_bank3
(OUT/"bank0.asm").write_text(hud_bank0(patch_bank0((ROOT/"scripts"/"fullgame1_actor_bank0.asm").read_text())))
(OUT/"bank1.asm").write_text(hud_bank1((ROOT/"scripts"/"fullgame1_sound_bank1.asm").read_text()))
from fullgame1_arrow_patch import patch_bank2, patch_bank3
from fullgame1_geometry_patch import cache_bank2, cache_bank3
from fullgame1_actor_patch import actors_bank2, actors_bank3
from fullgame1_world_patch import world_bank3
from fullgame1_sound_patch import sound_bank2, sound_bank3
for i, name in ((2,"gameplay5_bank0.asm"),(3,"gameplay5_bank1.asm")):
    original_source=(SRC/name).read_text()
    updated_source=(patch_bank2(original_source) if i==2 else patch_bank3(original_source))
    updated_source=(cache_bank2(updated_source) if i==2 else cache_bank3(updated_source))
    updated_source=(actors_bank2(updated_source) if i==2 else actors_bank3(updated_source))
    if i==3: updated_source=world_bank3(updated_source)
    updated_source=(sound_bank2(updated_source) if i==2 else sound_bank3(updated_source))
    updated_source=(safety_bank2(updated_source) if i==2 else stage_render_bank3(updated_source))
    if i==3: updated_source=gameover_bank3(hud_bank3(updated_source))
    else: updated_source=gameover_bank2(updated_source)
    (OUT/f"bank{i}.asm").write_text(updated_source)
parts=[]
for i in range(4):
    source=OUT/f"bank{i}.asm"
    dest=OUT/f"bank{i}.bin"
    cmd=["dasm",str(source),"-f3",f"-o{dest}",f"-l{OUT/f'bank{i}.lst'}",f"-s{OUT/f'bank{i}.sym'}"]
    p=subprocess.run(cmd,capture_output=True,text=True)
    (OUT/f"DASM{i}.log").write_text("COMMAND: "+" ".join(cmd)+"\n"+p.stdout+p.stderr)
    if p.returncode:
        raise RuntimeError(f"DASM failed bank{i}: {p.stdout} {p.stderr}")
    part=dest.read_bytes()
    if len(part)!=4096:
        raise ValueError(f"bank{i} size={len(part)}, expected 4096")
    parts.append(part)
# Original 8KiB remains frozen; derived banks2/3 intentionally differ for new M1 attempt.
assert parts[2] != original[:4096] and parts[3] != original[4096:], "Arrow experiment did not compile"
rom=b"".join(parts)
assert len(rom)==16384
(OUT/"THE_SKRAUN_FULLGAME1_F6_NTSC.bin").write_bytes(rom)
rows=[f"{hashlib.sha256(rom).hexdigest()}  THE_SKRAUN_FULLGAME1_F6_NTSC.bin"]
for i in range(4):
    for ext in ("asm","bin"):
        p=OUT/f"bank{i}.{ext}"
        rows.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}")
(OUT/"SHA256SUMS.txt").write_text("\n".join(rows)+"\n")
print("FULLGAME1_F6_M1_EXPERIMENT_NOT_A_PASS")
print("F8 frozen:",EXPECTED)
print("F6 16384:",hashlib.sha256(rom).hexdigest())
