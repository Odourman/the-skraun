"""Verify optimized R1-PF 4K ROM reproduces all 52 original obstruction masks.
DASM aliases must resolve to EXACT 33-byte assets, not just array lengths.
"""
from pathlib import Path
import re
p=Path("experiments/romdev_b3b_obstacles.asm").read_text()
opt=Path("experiments/romdev_r1_optimized_pf.asm").read_text()
pattern=re.compile(r'^((?:L1|L2|R0|R1)_\d+):\n((?:[ \t]*dc\.b [^\n]+\n)+)',re.M)
expected={}
for name,rows in pattern.findall(p):
    x=bytes(int(y,16) for y in re.findall(r'\$([0-9A-Fa-f]{2})',rows))
    assert len(x)==33
    expected[name]=x
assert len(expected)==52
sym={}
for row in Path("build/romdev-r1-opt.sym").read_text().splitlines():
    m=re.match(r'^([A-Za-z][A-Za-z_0-9]*)\s+([0-9A-Fa-f]{4})\s+',row)
    if m:sym[m[1]]=int(m[2],16)
rom=Path("build/romdev-r1-opt.bin").read_bytes()
assert len(rom)==4096
used=set()
for name,dat in expected.items():
    assert name in sym,("DASM alias missing",name)
    adr=sym[name]-0xf000
    actual=rom[adr:adr+33]
    assert actual==dat,("optimized mask differs from original",name,adr,actual.hex(),dat.hex())
    used.add(adr)
assert len(used)==36,("expected exactly 36 unique physical masks",len(used))
print("PASS: exact ROM bytes for 52 original PF masks; only 36 physical 33-byte copies.")
print("ROM savings", (52-len(used))*33, "bytes (528); no runtime compositing added.")
print("WARNING: same-color obstacle+ring overlap persists, independent scenes still cost storage.")
