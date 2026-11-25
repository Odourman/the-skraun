#!/usr/bin/env python3
"""Extract genuine _scanEnd and state from saved Stella sessions; do not invent PASS."""
from pathlib import Path
import re, json
root=Path("build/fullgame1/regression/scenes")
summary={}
for scene in ["start","knight_warning","knight_strike","knight_rest","ranger_phase4","ranger_phase12","ranger_phase22","ranger_phase29","ranger_phase35","ranger_draw","ranger_release","arrow_first","arrow_mid","arrow_later","stage2_L3","gameover_restart","stress_120"] :
    p=root/scene/"SESSION_TYPED.txt"
    text=p.read_text(errors="replace") if p.exists() else ""
    match=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)', text)
    counts=list(map(int,match))
    summary[scene]={"scan_end":counts[-1] if counts else None,"raw_scan_values":counts,"saved_session":str(p),"session_bytes":len(text)}
    print("REAL_STELLA_FRAME",scene,"scanEnd",summary[scene]["scan_end"],"session_bytes",len(text))
out=Path("build/fullgame1/REAL_STELLA_SCENES.json")
# Stella saveSes stores the current debugger state, not the full transcript.
# Read one genuine session after each of 120 consecutive frame #1 commands.
frames=sorted((root/"stress_120").glob("FRAME_*.txt"))
if len(frames)!=120:
    raise SystemExit(f"CONSECUTIVE_FRAMES_UNOBSERVED: {len(frames)}/120 separate Stella captures")
sequential=[]
for frame_file in frames:
    session=frame_file.read_text(errors="replace")
    observed=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',session)
    # saveSes in Stella 6.7.1 does not necessarily preserve autoexec's
    # debugger print history. Never infer scanline counts from an empty record.
    sequential.append(int(observed[-1]) if observed else None)
summary["stress_120"]["consecutive_scan_end"]=sequential
measured=[n for n in sequential if n is not None]
if any(n!=262 for n in measured):
    raise SystemExit("CONSECUTIVE_NTSC_FAIL: observed physical frame not 262")
print("REAL_STELLA_CONTIGUOUS_CAPTURED",len(frames),
      "per_frame_scan_observed",len(measured),"unobserved",len(frames)-len(measured))
out.write_text(json.dumps(summary,indent=2)+"\n")
if not all(row["raw_scan_values"] and all(v == 262 for v in row["raw_scan_values"]) for row in summary.values()):
    raise SystemExit("NOT_262_OR_UNOBSERVED: real F6 arrow candidate must not be called a PASS")
print("BOUNDED_NTSC_PASS 17 final scenes; 120 contiguous state captures with unmeasured per-frame scanEnd (not full game)")
