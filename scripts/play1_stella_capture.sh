#!/usr/bin/env bash
set -euo pipefail
mkdir -p build/play1 "$HOME/.config/stella"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
cat > "$HOME/.config/stella/autoexec.script" <<'SCRIPT'
base dec
frame #10
print _scanEnd
print _fCount
SCRIPT
xvfb-run -a -s "-screen 0 1400x1000x24" bash -c '
 set -eu
 out="$PWD/build/play1"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$out/play1.bin" > "$out/STELLA_DEBUGGER.log" 2>&1 &
 pid=$!
 win=""
 for n in $(seq 1 30); do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
    [ -n "$win" ] && break
    kill -0 "$pid" 2>/dev/null || break
    sleep 1
 done
 if [ -z "$win" ]; then echo "FAIL: Stella window absent"; cat "$out/STELLA_DEBUGGER.log"; exit 1; fi
 xdotool windowfocus "$win" || true
 sleep 2
 scrot -z "$out/PLAY1_FRAME_000.png"
 # Use debugger commands to read internal hardware/ROM state; real 6507 not model.
 i=1
 while [ "$i" -le 12 ]; do
   xdotool type --window "$win" --clearmodifiers --delay 15 "frame #1" || true
   xdotool key --window "$win" Return || true
   sleep 0.25
   scrot -z "$(printf "%s/PLAY1_FRAME_%03d.png" "$out" "$i")"
   i=$((i+1))
 done
 xwininfo -root -tree > "$out/XWINDOWS.txt" || true
 kill "$pid" || true
 wait "$pid" || true
'
