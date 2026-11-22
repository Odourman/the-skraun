#!/usr/bin/env bash
# ROM DEVELOPMENT instrumentation-only. Does not alter ROM instructions.
# Shows the actual physical Stella debugger PC/scanline/cycle/colorclock
# around RESP1 and neighboring GRP1/COLUP1 writes on 2 adjacent band rows.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/n7/trace "$HOME/.config/stella"
cat > "$HOME/.config/stella/autoexec.script" <<'SCRIPT'
base dec
frame #10
print _scanEnd
print _fCount
SCRIPT
xvfb-run -a -s "-screen 0 1400x1000x24" bash -c '
 set -eu
 out="$PWD/build/n7/trace"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/n7/n7-f2b-ntsc.bin" > "$out/STELLA.log" 2>&1 &
 pid=$!
 win=""
 for i in $(seq 1 30); do
   win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
   if [ -n "$win" ]; then break; fi
   if ! kill -0 "$pid" 2>/dev/null; then break; fi
   sleep 1
 done
 test -n "$win" || { cat "$out/STELLA.log"; exit 1; }
 xdotool windowfocus "$win" || true
 sleep 2
 i=0
 for cmd in \
 "runToPc \$f0b5" "runToPc \$f0c5" "runToPc \$f0c9" \
 "step #1" "runToPc \$f0cb" "runToPc \$f0cf" \
 "runToPc \$f0d3" "runToPc \$f0b5" "runToPc \$f0c5" \
 "runToPc \$f0c9" "step #1" "runToPc \$f0cb" "runToPc \$f0cf"
 do
   i=$((i+1))
   echo "$i $cmd" >> "$out/TRACE_COMMANDS.txt"
   xdotool type --window "$win" --clearmodifiers --delay 20 "$cmd"
   xdotool key --window "$win" Return
   sleep 0.5
   scrot -z "$(printf "%s/TRACE_%02d.png" "$out" "$i")"
 done
 kill "$pid" || true
 wait "$pid" || true
'
