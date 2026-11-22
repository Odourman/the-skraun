#!/usr/bin/env bash
# GAMEPLAY-4 CHECKPOINT A genuine Stella runtime evidence: joystick and FIRE only, no RAM/PC writes.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay4/checkpoint_A/scenes "$HOME/.config/stella"
i=0
for scene in start knight_warning knight_strike knight_rest ranger_phase4 ranger_phase12 ranger_phase22 ranger_phase29 ranger_phase35 ranger_draw ranger_release stage2_L3 gameover_restart;do
 i=$((i+1));export DISPLAY=":$((200+i))"
 out="$PWD/build/gameplay4/checkpoint_A/scenes/$scene";mkdir -p "$out"
 Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/XVFB.log" 2>&1 &
 xv=$!;sleep 1
 {
   echo 'base dec'
   echo 'frame #10'
   case "$scene" in
    start) ;;
    knight_warning|knight_strike|knight_rest)
      echo 'joy0Right #0';echo 'frame #25';echo 'joy0Right #1'
      if [ "$scene" = knight_warning ];then echo 'frame #9';fi
      if [ "$scene" = knight_strike ];then echo 'frame #30';fi
      if [ "$scene" = knight_rest ];then echo 'frame #44';fi
      ;;
    ranger_phase4|ranger_phase12|ranger_phase22|ranger_phase29|ranger_phase35|ranger_draw|ranger_release|arrow_first|arrow_mid|arrow_later|stage2_L3)
      echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
      echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
      echo 'joy0Fire #0'
      echo 'joy0Up #0';echo 'frame #40';echo 'joy0Up #1'
      echo 'joy0Right #0';echo 'frame #14';echo 'joy0Right #1'
      case "$scene" in
        ranger_phase4) echo 'frame #4';;
        ranger_phase12) echo 'frame #12';;
        ranger_phase22) echo 'frame #22';;
        ranger_phase29) echo 'frame #29';;
        ranger_phase35) echo 'frame #35';;
        ranger_draw)
          # After second knight, leave L2 halo radius before Ranger respawns
          echo 'joy0Fire #1'
          echo 'joy0Left #0';echo 'frame #25';echo 'joy0Left #1'
          echo 'frame #12'
          ;;
        ranger_release)
          echo 'joy0Fire #1'
          echo 'joy0Left #0';echo 'frame #25';echo 'joy0Left #1'
          echo 'frame #39'
          ;;
        arrow_first) echo 'frame #59';;
        arrow_mid) echo 'frame #75';;
        arrow_later) echo 'frame #90';;
        stage2_L3)
          echo 'frame #420';echo 'joy0Fire #1'
          echo 'joy0Right #0';echo 'frame #8';echo 'joy0Right #1'
          echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
          echo 'frame #65';echo 'joy0Fire #0'
          echo 'frame #2';echo 'joy0Right #0';echo 'joy0Up #0';echo 'frame #12'
          echo 'joy0Right #1';echo 'joy0Up #1'
          echo 'joy0Fire #1';;
      esac
      ;;
    gameover_restart)
      echo 'joy0Right #0';echo 'frame #30';echo 'joy0Right #1'
      echo 'frame #500';echo 'joy0Fire #0';echo 'frame #3';echo 'joy0Fire #1';;
   esac
   for k in _scanEnd _scan _sCycles _bank _fCount '*$80' '*$81' '*$82' '*$9D' '*$9E' '*$A1' '*$A3' '*$A4' '*$A5' '*$AA' '*$AC' '*$AD' '*$AE' '*$AF' '*$B0' '*$B1' '*$B2' '*$B3' '*$B4' '*$B5' '*$B8' '*$B9';do
     echo "print $k"
   done
   echo "saveSes $out/SESSION.txt"
 } > "$HOME/.config/stella/autoexec.script"
 cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/gameplay4/checkpoint_A/gameplay4a_f8.bin" > "$out/STELLA.log" 2>&1 &
 pid=$!; win=""
 for k in $(seq 1 25);do
  win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
  [ -n "$win" ] && break
  kill -0 "$pid" 2>/dev/null||break
  sleep 1
 done
 if [ -z "$win" ];then echo "NO_REAL_STELLA_WINDOW $scene";cat "$out/STELLA.log";exit 1;fi
 sleep 0.5
 scrot -z "$out/DEBUGGER_DESKTOP.png"
 xdotool windowfocus "$win" || true
 xdotool mousemove 150 618 click 1 || true
 xdotool type --clearmodifiers --delay 4 'print _scanEnd' || true
 xdotool key Return || true
 sleep 0.2;scrot -z "$out/SCANLINES_DEBUGGER.png"
 xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true
 xdotool key Return || true
 sleep 0.3
 kill "$pid" 2>/dev/null||true;wait "$pid" 2>/dev/null||true
 kill "$xv" 2>/dev/null||true;wait "$xv" 2>/dev/null||true
done
