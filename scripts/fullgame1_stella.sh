#!/usr/bin/env bash
# Frame probe of the physical 16KiB F6 ROM (not full-game validation).
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
export DISPLAY=:174
out="$PWD/build/fullgame1/stella_boot"
mkdir -p "$out" "$HOME/.config/stella"
Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
xv=$!;trap 'kill "$xv" 2>/dev/null || true' EXIT
sleep 2
{
 echo 'base dec'
 echo 'frame #20'
 echo 'joy0Right #0'
 echo 'frame #20'
 echo 'joy0Right #1'
 echo 'frame #30'
 echo 'print _scanEnd'
 echo 'print _bank'
 echo 'print _pc'
 echo 'print _sp'
 echo 'print *$80'
 echo 'print *$81'
 echo 'print *$AA'
 echo "saveSes $out/SESSION_AUTO.txt"
} > "$HOME/.config/stella/autoexec.script"
rom="$PWD/build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin"
stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$rom" > "$out/STELLA.log" 2>&1 &
pid=$!
win=""
for i in $(seq 1 30);do
 win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
 [ -n "$win" ] && break
 kill -0 "$pid" 2>/dev/null || break
 sleep 1
done
if [ -z "$win" ];then cat "$out/STELLA.log"; exit 1;fi
scrot -z "$out/DESKTOP.png"
xdotool windowfocus "$win" || true
xdotool mousemove 150 618 click 1 || true
xdotool type --clearmodifiers --delay 4 'print _scanEnd' || true
xdotool key Return || true
sleep 0.3
scrot -z "$out/SCANLINE.png"
xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true
xdotool key Return || true
sleep 0.3
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
echo 'REAL_STELLA_BOOTSTRAP_ATTEMPT_DONE (inspect scanline+bank traces)'
