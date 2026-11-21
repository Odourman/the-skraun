#!/usr/bin/env bash
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software DISPLAY=:99
mkdir -p build/play1h/moving "$HOME/.config/stella"
Xvfb :99 -screen 0 1400x1000x24 > build/play1h/XVFB.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
for scene in baseline A_L3_on B_L3_right8 C_L3_right8_down8 L1_on L2_on; do
  out="$PWD/build/play1h/moving/$scene"
  mkdir -p "$out"
  {
    echo 'base dec'
    echo 'frame #10'
    case "$scene" in
       baseline) ;;
       L1_on)
         echo 'joy0Fire #0'
         echo 'frame #2'
         echo 'joy0Fire #1'
         ;;
       *)
         echo 'joy0Right #0'
         echo 'frame #16'
         echo 'joy0Right #1'
         echo 'joy0Down #0'
         echo 'frame #24'
         echo 'joy0Down #1'
         if [ "$scene" != L2_on ]; then
            echo 'frame #100'
         fi
         echo 'joy0Fire #0'
         echo 'frame #2'
         if [ "$scene" = B_L3_right8 ] || [ "$scene" = C_L3_right8_down8 ]; then
           echo 'joy0Right #0'
           echo 'frame #8'
           echo 'joy0Right #1'
         fi
         if [ "$scene" = C_L3_right8_down8 ]; then
           echo 'joy0Down #0'
           echo 'frame #8'
           echo 'joy0Down #1'
         fi
         echo 'joy0Fire #1'
       ;;
    esac
    for addr in 80 81 82 9C 9D 9E A1 A5 A6 A7; do
      printf 'print *$%s\n' "$addr"
    done
    echo 'print _scanEnd'
    echo 'print _fCount'
  } > "$HOME/.config/stella/autoexec.script"
  cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
  stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/play1h/play1h.bin" > "$out/STELLA.log" 2>&1 &
  pid=$!
  win=""
  for i in $(seq 1 30); do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
    [ -n "$win" ] && break
    kill -0 "$pid" 2>/dev/null || break
    sleep 1
  done
  if [ -z "$win" ]; then echo "FAIL NO STELLA WINDOW $scene"; cat "$out/STELLA.log"; exit 1; fi
  sleep 1
  xdotool windowfocus "$win" || true
  scrot -z "$out/DEBUGGER_DESKTOP.png"
  kill "$pid" || true
  wait "$pid" || true
done
