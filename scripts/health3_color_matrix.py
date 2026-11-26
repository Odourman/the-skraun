"""Expand PR61 and fixed-PF ownership hypothesis across relevant scene flags."""
from itertools import product
from pathlib import Path
import csv

palette = (0xC6, 0xC8, 0x36, 0x38, 0x56, 0x58, 0x06, 0x08)
f = Path("h3/delivery/COLOR_COST_MATRIX.csv")
with f.open("w", newline="") as dest:
    writer = csv.writer(dest)
    writer.writerow(["world","stage","level","halo","orb","arrow","P1 occupant",
        "Ranger threat","overlap","invulnerable","zone","PR61 COLUPF","fixed PF COLUPF",
        "COLUP0 P0+M0","COLUP1 P1+M1","BL width","BL owner","limitation"])
    for stage,lev,halo,orb,arrow,occupant,threat,overlap,invuln,zone in product(
        range(1,9),range(1,4),range(2),range(2),range(2),
        ("K1","K2","R"),range(2),("separate","same-Y","edge"),range(2),("arena","HUD","clear")):
        world=palette[stage-1]
        source1=world if occupant=="R" and not (arrow or threat) else 0x9E
        writer.writerow([("Skog","Berg","Dröm","Natt")[(stage-1)//2],stage,lev,halo,orb,arrow,occupant,
            threat,overlap,invuln,zone,f"{0x2e if halo else world:02X}",f"{world:02X}",
            f"{0x2e if halo else 0x0e:02X}",f"{source1:02X} or K tint 2E/46",
            (2,4,8)[lev-1],"phased orb/rim" if orb and halo else ("orb" if orb else ("rim" if halo else "none")),
            "SOURCE_ONLY owner envelope; HUD inherits PF; clear uses separately retained latch; row/beam phase can occlude"])
