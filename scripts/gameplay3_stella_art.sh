#!/usr/bin/env bash
# Authentic Stella 6.7.1 GUI captures, six exact masks x native/mirrored,
# no debugger writes to game RAM, no synthetic sprite montage.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay3/art "$HOME/.config/stella"
n=0
for asm in build/gameplay3/variants/*.asm; do
 name="$(basename "$asm" .asm)"
 n=$((n+1))
 export DISPLAY=":$((120+n))"
 Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "build/gameplay3/XVFB_$name.log" 2>&1 &
 xvpid=$!
 sleep 1
 out="$PWD/build/gameplay3/art/$name"
 mkdir -p "$out"
 {
   echo 'base dec'
   echo 'frame #12'
   echo 'print _scanEnd'
   echo 'print *$AF'
   echo 'print *$AA'
   echo 'print *$AC'
   echo 'print *$AD'
   echo "saveSes $out/SESSION.txt"
 } > "$HOME/.config/stella/autoexec.script"
 cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/gameplay3/variants/$name.bin" > "$out/STELLA.log" 2>&1 &
 pid=$!
 win=""
 for k in $(seq 1 20);do
  win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
  [ -n "$win" ] && break
  kill -0 "$pid" 2>/dev/null || break
  sleep 1
 done
 if [ -z "$win" ];then echo "STELLA_WINDOW_FAIL $name";cat "$out/STELLA.log";exit 1;fi
 sleep 0.5
 scrot -z "$out/DEBUGGER_DESKTOP.png"
 xdotool windowfocus "$win" || true
 xdotool mousemove 150 618 click 1 || true
 xdotool type --clearmodifiers --delay 4 'print _scanEnd' || true
 xdotool key Return || true
 sleep 0.2
 scrot -z "$out/SCANLINE_DEBUGGER.png"
 xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true
 xdotool key Return || true
 sleep 0.2
 kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
 kill "$xvpid" 2>/dev/null || true;wait "$xvpid" 2>/dev/null || true
done
