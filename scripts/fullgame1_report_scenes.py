#!/usr/bin/env python3
"""Extract genuine _scanEnd and state from saved Stella sessions; do not invent PASS."""
from pathlib import Path
import re, json
root=Path("build/fullgame1/regression/scenes")
summary={}
for scene in ["start","knight_warning","knight_strike","knight_rest","ranger_phase4","ranger_phase12","ranger_phase22","ranger_phase29","ranger_phase35","ranger_draw","ranger_release","arrow_first","arrow_mid","arrow_later","stage2_L3","gameover_restart"] :
    p=root/scene/"SESSION_TYPED.txt"
    text=p.read_text(errors="replace") if p.exists() else ""
    match=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)', text)
    counts=list(map(int,match))
    summary[scene]={"scan_end":counts[-1] if counts else None,"raw_scan_values":counts,"saved_session":str(p),"session_bytes":len(text)}
    print("REAL_STELLA_FRAME",scene,"scanEnd",summary[scene]["scan_end"],"session_bytes",len(text))
out=Path("build/fullgame1/REAL_STELLA_SCENES.json")
out.write_text(json.dumps(summary,indent=2)+"\n")
if not all(row["scan_end"] == 262 for row in summary.values()):
    raise SystemExit("NOT_262_OR_UNOBSERVED: real F6 arrow candidate must not be called a PASS")
print("BOUNDED_NTSC_PASS 16 sampled scenarios (not entire game, not worst-case beam deadlines)")
