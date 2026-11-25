#!/usr/bin/env python3
"""Build the current three-level runic halo and true ArrowY renderer from four readable F6 banks.
User-authorized FULLGAME-1 scope on branch from frozen adaptive PR #53.
REAL DASM required. Output reproducible, no "released" claim implied.
"""
from pathlib import Path
import hashlib, subprocess, shutil, sys, json
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "build" / "arrow_halo_romdev4"
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED = "45a6c84b01910e6021e398f71096e435ea68c750867eaa826d0ee03dc64e1dbf"
BASELINE = "d2a0a1b57ac9c78b2af14f77800f7c1ecf99aaa43f60e8c4216974f18aed2a0e"
parts = []
usage = []
for n in range(4):
    src = HERE / f"bank{n}.asm"
    binary = OUT / f"bank{n}.bin"
    cmd = ["dasm", str(src), "-f3", f"-o{binary}", f"-l{OUT/f'bank{n}.lst'}",f"-s{OUT/f'bank{n}.sym'}"]
    result = subprocess.run(cmd,capture_output=True,text=True)
    (OUT/f"DASM{n}.log").write_text("COMMAND "+" ".join(cmd)+"\n"+result.stdout+result.stderr)
    if result.returncode:
        raise RuntimeError(f"real DASM bank{n} failed: "+result.stdout+result.stderr)
    b=binary.read_bytes()
    if len(b)!=4096:raise ValueError(f"F6 bank{n} actual len {len(b)}, not 4096")
    parts.append(b)
    nonfill=sum(v!=0 for v in b)
    usage.append({"bank":n,"size":len(b),"nonzero_bytes":nonfill,"sha256":hashlib.sha256(b).hexdigest()})
rom=b"".join(parts)
sha=hashlib.sha256(rom).hexdigest()
if sha != EXPECTED:raise RuntimeError("OUTPUT ROM NOT FROZEN CHECKPOINT: "+sha)
(OUT/"THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin").write_bytes(rom)
(OUT/"SHA256SUMS.txt").write_text(sha+"  THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin\n")
(OUT/"BANK_USAGE.json").write_text(json.dumps({"mapper":"F6 (NO SC RAM)","rom_sha256":sha,"frozen_adaptive_sha256":BASELINE,"banks":usage},indent=2)+"\n")
compat = ROOT / "build" / "fullgame1"
compat.mkdir(parents=True, exist_ok=True)
shutil.copy2(OUT/"THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin",compat/"THE_SKRAUN_FULLGAME1_F6_NTSC.bin")
print(f"DEVELOPER_EXPERIMENT_NOT_RELEASE sha256={sha} bytes={len(rom)}")
