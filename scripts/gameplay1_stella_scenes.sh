#!/usr/bin/env bash
# Real Stella debugger joystick / console SELECT / FIRE only, never direct RAM injections.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay1/moving "$HOME/.config/stella"
scene_num=0
for scene in baseline L1_on pickup_L2_off L3_select L3_select_right8 sword_warning sword_hit stage_progress; do
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
        echo 'joy0Fire #0'; echo 'frame #2'; echo 'joy0Fire #1'
        ;;
      pickup_L2_off)
        echo 'joy0Right #0'; echo 'frame #16'; echo 'joy0Right #1'
        echo 'joy0Down #0'; echo 'frame #24'; echo 'joy0Down #1'
        ;;
      L3_select|L3_select_right8)
        # Two genuine console SELECT edges, performed while x80 y88 is clear.
        echo 'swchb $FD'; echo 'frame #1'; echo 'swchb $FF'; echo 'frame #1'
        echo 'swchb $FD'; echo 'frame #1'; echo 'swchb $FF'; echo 'frame #1'
        if [ "$scene" = L3_select_right8 ]; then
          echo 'joy0Right #0'; echo 'frame #8'; echo 'joy0Right #1'
        fi
        ;;
      sword_warning|sword_hit)
        # Approach blue P1 without FIRE. Sword warning is real game logic.
        echo 'joy0Right #0'; echo 'frame #25'; echo 'joy0Right #1'
        if [ "$scene" = sword_warning ]; then
          echo 'frame #10'
        else
          echo 'frame #37'
        fi
        ;;
      stage_progress)
        # Three sequential diagnostic kills may advance stage; test not canon-clear.
        echo 'joy0Right #0'; echo 'frame #32'; echo 'joy0Right #1'
        echo 'joy0Fire #0'; echo 'frame #270'; echo 'joy0Fire #1'
        ;;
    esac
    echo 'cls'
    echo 'print _scanEnd'
    echo 'print _fCount'
    echo 'print *$80'
    echo 'print *$81'
    echo 'print *$82'
    echo 'print *$AA'
    echo 'print *$AC'
    echo 'print *$AD'
    echo 'print *$AE'
    echo 'print *$AF'
    echo 'print *$B0'
    echo 'print *$B1'
    echo 'print *$B4'
    echo 'saveSes'
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
  if [ -z "$win" ]; then
    echo "FAIL NO STELLA WINDOW $scene"
    cat "$out/STELLA.log"
    exit 1
  fi
  sleep 1
  xdotool windowfocus "$win" || true
  scrot -z "$out/DEBUGGER_DESKTOP.png"
  # saveSes writes a timestamped session file in Stella's data directory.
  find "$HOME/.config/stella" -type f -name '*.txt' -newermt '1 minute ago' -exec cp '{}' "$out/" \; || true
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  kill "$xpid" 2>/dev/null || true
  wait "$xpid" 2>/dev/null || true
done
