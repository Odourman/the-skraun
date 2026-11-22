#!/usr/bin/env bash
# Instrumented ROM stack highwater; no debugger RAM edits, authentic Stella.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay3/stack_physical "$HOME/.config/stella"
n=0
for scene in start combat after_stage_transition; do
 n=$((n+1))
 export DISPLAY=":$((177+n))"
 out="$PWD/build/gameplay3/stack_physical/$scene"
 mkdir -p "$out"
 Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
 xv=$!
 sleep 1
 {
  echo 'base hex'
  echo 'frame #12'
  case "$scene" in
   combat)
    echo 'joy0Right #0';echo 'frame #25';echo 'joy0Right #1';echo 'frame #60';;
   after_stage_transition)
    echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
    echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
    echo 'joy0Fire #0';echo 'joy0Up #0';echo 'frame #40'
    echo 'joy0Up #1';echo 'joy0Right #0';echo 'frame #14'
    echo 'joy0Right #1';echo 'frame #420';;
  esac
  echo 'print _scanEnd'
  echo 'print _bank'
  for start in 240 244 248 252;do
    for i in $(seq $start $((start+3)));do
      printf 'print *$%02X\n' "$i"
    done
    printf 'saveSes %s/STACK_%02X.txt\n' "$out" "$start"
  done
 } > "$HOME/.config/stella/autoexec.script"
 cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/gameplay3/stack_sentinel_f8.bin" > "$out/STELLA.log" 2>&1 &
 pid=$!
 win=""
 for k in $(seq 1 20);do
  win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
  [ -n "$win" ] && break
  kill -0 "$pid" 2>/dev/null || break
  sleep 1
 done
 if [ -z "$win" ];then echo "NO_STACK_STELLA $scene";cat "$out/STELLA.log";exit 1;fi
 sleep 0.5
 scrot -z "$out/DEBUGGER_RIOT.png"
 kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
 kill "$xv" 2>/dev/null || true;wait "$xv" 2>/dev/null || true
done
