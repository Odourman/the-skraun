#!/usr/bin/env bash
# H3: two materially distinct P1 owner experiments; independent K1/K2/R1
# X/Y in real game bank, no RAM injection. Source/color timing in bank1.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay5/h3/scenes "$HOME/.config/stella"
n=0
for mode in same sep;do
 for scene in start L2;do
   n=$((n+1));export DISPLAY=":$((370+n))"
   out="$PWD/build/gameplay5/h3/scenes/${mode}_${scene}"
   mkdir -p "$out"
   Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
   xv=$!;sleep 1
   {
    echo 'base dec';echo 'frame #3'
    if [ "$scene" = L2 ];then
     echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
     echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
     echo 'frame #4'
    fi
    for key in _scanEnd _scan _sCycles _cClocks _fWsyncCycles _fTimReadCycles _bank _pc _sp _fCount '*$89' '*$A3' '*$A4' '*$B8' '*$B9' '*$AF' '*$82';do echo "print $key";done
    echo "saveSes $out/SESSION.txt"
   } > "$HOME/.config/stella/autoexec.script"
   cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
   stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/gameplay5/h3/${mode}/f8.bin" > "$out/STELLA.log" 2>&1 &
   pid=$!; win=""
   for k in $(seq 1 25);do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
    [ -n "$win" ] && break
    kill -0 "$pid" 2>/dev/null||break
    sleep 1
   done
   if [ -z "$win" ];then cat "$out/STELLA.log";exit 1;fi
   sleep 0.4; scrot -z "$out/DEBUGGER_DESKTOP.png"
   xdotool windowfocus "$win" || true
   xdotool mousemove 150 618 click 1 || true
   xdotool type --clearmodifiers --delay 4 'print _scanEnd' || true
   xdotool key Return || true
   sleep 0.2;scrot -z "$out/SCANLINES_DEBUGGER.png"
   xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true
   xdotool key Return || true
   sleep 0.2
   kill "$pid" 2>/dev/null||true;wait "$pid" 2>/dev/null||true
   kill "$xv" 2>/dev/null||true;wait "$xv" 2>/dev/null||true
 done
done
