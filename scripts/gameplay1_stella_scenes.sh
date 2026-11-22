#!/usr/bin/env bash
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay1/moving "$HOME/.config/stella"
scene_num=0
for scene in baseline L1_on pickup_L2_off A_L3_on B_L3_right8; do
  scene_num=$((scene_num+1))
  export DISPLAY=":$((90+scene_num))"
  Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "build/gameplay1/XVFB_${scene}.log" 2>&1 &
  xpid=$!
  sleep 2
  out="$PWD/build/gameplay1/moving/$scene"
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
         if [ "$scene" != L2_on ] && [ "$scene" != pickup_L2_off ]; then
            echo 'frame #100'
         fi
         if [ "$scene" != pickup_L2_off ]; then
            echo 'joy0Fire #0'
            echo 'frame #2'
         fi
         if [ "$scene" = B_L3_right8 ] || [ "$scene" = C_L3_right8_up8 ] || [ "$scene" = D_L3_right8_down8 ]; then
           echo 'joy0Right #0'
           echo 'frame #8'
           echo 'joy0Right #1'
         fi
         if [ "$scene" = C_L3_right8_up8 ]; then
           echo 'joy0Up #0'
           echo 'frame #8'
           echo 'joy0Up #1'
         fi
         if [ "$scene" = D_L3_right8_down8 ]; then
           echo 'joy0Down #0'
           echo 'frame #8'
           echo 'joy0Down #1'
         fi
         if [ "$scene" != pickup_L2_off ]; then
            echo 'joy0Fire #1'
         fi
       ;;
    esac
    for addr in 80 81 82 9C 9D 9E A1 A5 A6 A7; do
      printf 'print *$%s\n' "$addr"
    done
    echo 'print _scanEnd'
    echo 'print _fCount'
  } > "$HOME/.config/stella/autoexec.script"
  cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
  stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/gameplay1/gameplay1_f8.bin" > "$out/STELLA.log" 2>&1 &
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
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  kill "$xpid" 2>/dev/null || true
  wait "$xpid" 2>/dev/null || true
done
