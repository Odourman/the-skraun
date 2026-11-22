#!/usr/bin/env bash
# GAMEPLAY-5 true same-script frozen vs candidate differential, no debug state injection.
# Source-only typed joystick/frame commands; NO debugger RAM/PC modification.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
ROM="${1:?pass actual verified F8 ROM path}"
TAG="${2:?pass trace prefix (e.g. frozen or candidate)}"
mkdir -p "build/gameplay5/scenes/$TAG" "$HOME/.config/stella"
i=0
for phase in 18 21 24 27 30;do
 i=$((i+1))
 export DISPLAY=":$((230+i+(${#TAG}*5)))"
 out="$PWD/build/gameplay5/scenes/$TAG/ranger_$phase"
 mkdir -p "$out"
 Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
 xv=$!;sleep 1
 {
  echo 'base dec'
  echo 'frame #10'
  echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
  echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
  echo 'joy0Fire #0'
  echo 'joy0Up #0';echo 'frame #40';echo 'joy0Up #1'
  echo 'joy0Right #0';echo 'frame #14';echo 'joy0Right #1'
  # 200 pts / final Ranger slot in normal stage; suppress new halo recast.
  echo 'joy0Fire #1'
  echo 'joy0Left #0';echo "frame #$phase";echo 'joy0Left #1'
  for key in _scanEnd _scan _sCycles _cClocks _fWsyncCycles _fTimReadCycles _bank _pc _sp _fCount '*$80' '*$81' '*$82' '*$9E' '*$A1' '*$A2' '*$AA' '*$AC' '*$AD' '*$AE' '*$AF' '*$B0' '*$B1' '*$B2' '*$B3' '*$B4';do
   echo "print $key"
  done
  echo "saveSes $out/SESSION.txt"
 } > "$HOME/.config/stella/autoexec.script"
 cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/$ROM" > "$out/STELLA.log" 2>&1 &
 pid=$!;win=""
 for k in $(seq 1 25);do
  win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
  [ -n "$win" ] && break
  kill -0 "$pid" 2>/dev/null||break
  sleep 1
 done
 if [ -z "$win" ];then echo "STELLA_WINDOW_FAIL safe_$phase";cat "$out/STELLA.log";exit 1;fi
 sleep 0.4
 scrot -z "$out/DEBUGGER_DESKTOP.png"
 xdotool windowfocus "$win" || true
 xdotool mousemove 150 618 click 1 || true
 xdotool type --clearmodifiers --delay 4 'print _scanEnd'
 xdotool key Return
 sleep 0.2;scrot -z "$out/SCANLINES_DEBUGGER.png"
 xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true
 xdotool key Return
 sleep 0.2
 kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
 kill "$xv" 2>/dev/null || true;wait "$xv" 2>/dev/null || true
done
