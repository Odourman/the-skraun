#!/usr/bin/env bash
# One original Stella Debugger session. Commands and 12 successive frame
# advances are saved; screenshots are actual native Xvfb window pixels.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/n7/stella-s2-12 "$HOME/.config/stella"
cat > "$HOME/.config/stella/autoexec.script" <<'STELLA'
base dec
frame #10
print _scanEnd
print _fCount
print _fCycles
STELLA
cp "$HOME/.config/stella/autoexec.script" build/n7/AUTOEXEC.script
xvfb-run -a -s "-screen 0 1400x1000x24" bash -c '
  set -eu
  out="$PWD/build/n7/stella-s2-12"
  stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/n7/n7-f2b-ntsc.bin" > "$out/STELLA_DEBUGGER.log" 2>&1 &
  pid=$!
  win=""
  for attempt in $(seq 1 30); do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
    if [ -n "$win" ]; then break; fi
    if ! kill -0 "$pid" 2>/dev/null; then break; fi
    sleep 1
  done
  if [ -z "$win" ]; then echo "FAIL: Stella GUI never opened"; cat "$out/STELLA_DEBUGGER.log"; exit 1; fi
  xdotool windowfocus "$win" || true
  sleep 2
  scrot -z "$out/FRAME_000.png"
  for i in $(seq 1 12); do
    xdotool type --window "$win" --clearmodifiers --delay 25 "frame #1" || true
    xdotool key --window "$win" Return || true
    sleep 0.30
    xdotool type --window "$win" --clearmodifiers --delay 25 "print _fCount" || true
    xdotool key --window "$win" Return || true
    sleep 0.25
    file=$(printf "%s/FRAME_%03d.png" "$out" "$i")
    scrot -z "$file"
  done
  xwininfo -root -tree > "$out/XWINDOWS.txt" || true
  ps -p "$pid" -o pid,stat,etime,args > "$out/STELLA_PROCESS.txt" || true
  kill "$pid" || true
  wait "$pid" || true
'
