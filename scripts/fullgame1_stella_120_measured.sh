#!/usr/bin/env bash
# FULLGAME-1 physical Stella 120 consecutive individually measured NTSC frames.
# Real joystick-only Level3 scene. Each ten-frame tranche preserves the
# typed Stella debugger output of every actual 'print _scanEnd' command.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
export DISPLAY=:241
out="$PWD/build/arrow_halo_romdev4/NTSC_120_MEASURED"
mkdir -p "$out" "$HOME/.config/stella"
rom="$PWD/build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin"
test "$(stat -c %s "$rom")" -eq 16384
Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
xv=$!
pid=""
trap '[ -z "$pid" ] || kill "$pid" 2>/dev/null || true; kill "$xv" 2>/dev/null || true' EXIT
sleep 1
cat > "$HOME/.config/stella/autoexec.script" <<'STELLA'
base dec
frame #10
joy0Right #0
frame #16
joy0Right #1
joy0Down #0
frame #24
joy0Down #1
joy0Fire #0
joy0Up #0
frame #40
joy0Up #1
joy0Right #0
frame #14
joy0Right #1
frame #420
joy0Fire #1
joy0Right #0
frame #8
joy0Right #1
joy0Down #0
frame #24
joy0Down #1
frame #65
joy0Fire #0
frame #2
joy0Right #0
joy0Up #0
frame #12
joy0Right #1
joy0Up #1
joy0Fire #1
print _scanEnd
STELLA
cp "$HOME/.config/stella/autoexec.script" "$out/INITIAL_SCENE.script"
stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$rom" > "$out/STELLA.log" 2>&1 &
pid=$!
win=""
for k in $(seq 1 35); do
  win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
  [ -n "$win" ] && break
  kill -0 "$pid" 2>/dev/null || break
  sleep 0.5
done
[ -n "$win" ] || { cat "$out/STELLA.log"; echo "FAIL_NO_STELLA_WINDOW"; exit 1; }
sleep 0.4
xdotool windowfocus "$win" || true
xdotool mousemove 150 618 click 1
for frame in $(seq 1 120); do
  xdotool type --clearmodifiers --delay 1 "frame #1"
  xdotool key Return
  sleep 0.05
  xdotool type --clearmodifiers --delay 1 "print _scanEnd"
  xdotool key Return
  sleep 0.05
  if (( frame % 10 == 0 )); then
    printf -v id "%03d" "$frame"
    xdotool type --clearmodifiers --delay 1 "saveSes $out/FRAME_$id.txt"
    xdotool key Return
    sleep 0.15
    test -s "$out/FRAME_$id.txt" || { echo "FAIL_MISSING_SESSION frame=$frame"; exit 1; }
  fi
done
xdotool type --clearmodifiers --delay 1 "print _sp"
xdotool key Return
xdotool type --clearmodifiers --delay 1 "print _fWsyncCycles"
xdotool key Return
xdotool type --clearmodifiers --delay 1 "print _fTimReadCycles"
xdotool key Return
xdotool type --clearmodifiers --delay 1 "saveSes $out/FINAL_DEBUGGER.txt"
xdotool key Return
sleep 0.3
python3 - "$out" <<'PY'
import json, pathlib, re, sys
out=pathlib.Path(sys.argv[1])
records=[]
for block in range(10,121,10):
    f=out/f"FRAME_{block:03d}.txt"
    s=f.read_text(errors="replace")
    vals=[int(x) for x in re.findall(r"> print _scanEnd\s*\n[^\n]*?#(\d+)",s)]
    if len(vals)<10:
        raise RuntimeError(f"REAL_STELLA_INDIVIDUAL_MISSING block={block} parsed={len(vals)}")
    tranche=vals[-10:]
    for i,v in enumerate(tranche):
        records.append({"frame":block-9+i,"scanEnd":v,"session":f.name})
    print(f"REAL_STELLA_10_FRAME_SCANS {block-9}..{block} {tranche}",flush=True)
if len(records)!=120 or any(r["scanEnd"]!=262 for r in records):
    raise RuntimeError("REAL_STELLA_120_NTSC_FAILURE "+str([r for r in records if r["scanEnd"]!=262]))
(out/"120_INDIVIDUAL_SCANENDS.json").write_text(json.dumps({"romSizeBytes":16384,"frames":records},indent=2)+"\n")
print("DEVELOPER_OBSERVED_120_CONSECUTIVE_INDIVIDUAL_NTSC_PASS",flush=True)
PY
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
pid=""
