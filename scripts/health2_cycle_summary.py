#!/usr/bin/env python3
"""Summarize Stella's native per-frame counters from natural joystick sessions.

DEVELOPER_OBSERVED session fields are read from each SESSION_TYPED.txt.
These counters rank total frame workload; they do NOT prove every raster line
met the 76-cycle/TIA beam deadline.
"""
from pathlib import Path
import csv, json, re, sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("build/fullgame1/regression/scenes")
out=Path(sys.argv[2]) if len(sys.argv)>2 else Path("build/fullgame1/HEALTH2_DYNAMIC_CYCLE_SUMMARY.json")
rows=[]
keys=("_scanEnd","_fCycles","_fWsyncCycles","_fTimReadCycles","_sp","_bank","_pc")
for session in sorted(root.glob("*/SESSION_TYPED.txt")):
    text=session.read_text(errors="replace")
    row={"scene":session.parent.name,"source":"SESSION_TYPED.txt","input_class":"natural_joystick"}
    for key in keys:
        match=re.search(r"> print "+re.escape(key)+r"\s*\n[^\n]*?#(\d+)",text)
        row[key]=int(match.group(1)) if match else None
    missing=[key for key in keys[:4] if row[key] is None]
    if missing:
        raise SystemExit(f"COUNTER_MISSING scene={row['scene']} missing={','.join(missing)}")
    row["evidence_class"]="DEVELOPER_OBSERVED_NATURAL_JOYSTICK_SESSION"
    rows.append(row)
if not rows:
    raise SystemExit(f"NO_TYPED_STELLA_SESSIONS root={root}")
summary={
    "evidence_class":"DEVELOPER_OBSERVED",
    "input_class":"natural_joystick",
    "rom_sha256":"bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5",
    "counter_semantics":{
        "_fCycles":"CPU cycles executed in this frame since VSYNC clear, per Stella debugger",
        "_fWsyncCycles":"cycles skipped by WSYNC in this frame, per Stella debugger",
        "_fTimReadCycles":"approximate cycles spent in timer-read loops, per Stella debugger",
        "_scanEnd":"physical scanline count at capture",
        "_sp":"point-in-time stack pointer only; not stack high-water",
    },
    "limits":[
        "Frame totals rank measured input paths; they are not a worst-case proof of every untested branch.",
        "No total-cycle field establishes the per-scanline 76-cycle limit or TIA write beam deadlines.",
        "SP is a final debugger sample, not a dynamic high-water measurement.",
        "Sessions must be captured from the SHA-pinned 16 KiB ROM and matching bank symbols.",
    ],
    "session_count":len(rows),
    "max_fCycles":max(r["_fCycles"] for r in rows),
    "min_fCycles":min(r["_fCycles"] for r in rows),
    "max_fWsyncCycles":max(r["_fWsyncCycles"] for r in rows),
    "max_fTimReadCycles":max(r["_fTimReadCycles"] for r in rows),
    "scenes":rows,
}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(summary,indent=2)+"\n")
csv_path=out.with_suffix(".csv")
with csv_path.open("w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=["scene","_scanEnd","_fCycles","_fWsyncCycles","_fTimReadCycles","_sp","_bank","_pc","input_class","evidence_class"])
    writer.writeheader()
    writer.writerows(rows)
slow=sorted(rows,key=lambda r:r["_fCycles"],reverse=True)[:5]
print(f"DYNAMIC_FRAME_CYCLES sessions={len(rows)} max={summary['max_fCycles']} min={summary['min_fCycles']} max_wsync={summary['max_fWsyncCycles']} max_timer={summary['max_fTimReadCycles']}")
for r in slow:
    print(f"FRAME_CYCLE_RANK scene={r['scene']} fCycles={r['_fCycles']} wsync={r['_fWsyncCycles']} timer={r['_fTimReadCycles']} scanEnd={r['_scanEnd']} sp_sample={r['_sp']}")
