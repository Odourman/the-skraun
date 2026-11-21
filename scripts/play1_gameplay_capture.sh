#!/usr/bin/env bash
# Original Stella 6.7.1, genuine joystick commands, no direct RAM injection.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software DISPLAY=:99
mkdir -p build/play1/gameplay "$HOME/.config/stella"
Xvfb :99 -screen 0 1400x1000x24 > build/play1/gameplay/XVFB.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
for scene in baseline movement_pickup level3_after_respawn halo_fire_target; do
  out="$PWD/build/play1/gameplay/$scene"
  mkdir -p "$out"
  {
    echo 'base dec'
    echo 'frame #10'
    if [ "$scene" != baseline ]; then
      echo 'joy0Right #0'
      echo 'frame #16'
      echo 'joy0Right #1'
      echo 'joy0Down #0'
      echo 'frame #24'
      echo 'joy0Down #1'
    fi
    if [ "$scene" = level3_after_respawn ] || [ "$scene" = halo_fire_target ]; then
      echo 'frame #100'
    fi
    if [ "$scene" = halo_fire_target ]; then
      echo 'joy0Fire #0'
      echo 'frame #2'
      echo 'joy0Fire #1'
    fi
    echo 'print *$80'
    echo 'print *$81'
    echo 'print *$82'
    echo 'print *$9C'
    echo 'print *$9D'
    echo 'print *$9E'
    echo 'print *$A1'
    echo 'print _scanEnd'
    echo 'print _fCount'
  } > "$HOME/.config/stella/autoexec.script"
  cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
  stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/play1/play1.bin" > "$out/STELLA.log" 2>&1 &
  pid=$!
  win=""
  for i in $(seq 1 30); do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
    [ -n "$win" ] && break
    kill -0 "$pid" 2>/dev/null || break
    sleep 1
  done
  if [ -z "$win" ]; then echo "FAIL NO STELLA WINDOW $scene"; cat "$out/STELLA.log"; exit 1; fi
  sleep 2
  xdotool windowfocus "$win" || true
  scrot -z "$out/DEBUGGER_DESKTOP.png"
  kill "$pid" || true
  wait "$pid" || true
done
