#!/usr/bin/env bash
# H1/H2 genuine Stella same/near-Y and separated-Y P1 LIMIT PROBES.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay3/hyp_physical "$HOME/.config/stella"
n=0
for bin in build/gameplay3/hypotheses/*.bin; do
  case "$bin" in *.bank1.bin) continue;; esac
  n=$((n+1))
  name="$(basename "$bin" .bin)"
  out="$PWD/build/gameplay3/hyp_physical/$name"
  mkdir -p "$out"
  export DISPLAY=":$((155+n))"
  Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
  xpid=$!
  sleep 1
  {
    echo 'base dec'
    echo 'frame #12'
    echo 'print _scanEnd'
    echo 'print _sCycles'
    echo 'print *$AF'
    echo "saveSes $out/SESSION.txt"
  } > "$HOME/.config/stella/autoexec.script"
  cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
  stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/$bin" > "$out/STELLA.log" 2>&1 &
  pid=$!
  win=""
  for i in $(seq 1 20); do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
    [ -n "$win" ] && break
    kill -0 "$pid" 2>/dev/null || break
    sleep 1
  done
  if [ -z "$win" ];then echo "NO_STELLA_WINDOW $name";cat "$out/STELLA.log";exit 1;fi
  sleep 0.5
  scrot -z "$out/DEBUGGER_DESKTOP.png"
  xdotool windowfocus "$win" || true
  xdotool mousemove 150 618 click 1 || true
  xdotool type --clearmodifiers --delay 4 'print _scanEnd'
  xdotool key Return
  sleep 0.2
  scrot -z "$out/SCANLINE_DEBUGGER.png"
  xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt"
  xdotool key Return
  sleep 0.2
  kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
  kill "$xpid" 2>/dev/null || true;wait "$xpid" 2>/dev/null || true
done
