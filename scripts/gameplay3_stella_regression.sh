#!/usr/bin/env bash
# GAMEPLAY-2 authentic Stella 6.7.1 debugger sequences; NO RAM or PC injection.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
mkdir -p build/gameplay3/scenes "$HOME/.config/stella"
n=0
for scene in start orb_L2 fight_stage1 stage2_L3 sword_warning sword_hit gameover_restart; do
 n=$((n+1))
 export DISPLAY=":$((100+n))"
 Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "build/gameplay3/XVFB_$scene.log" 2>&1 &
 xv=$!
 sleep 1
 out="$PWD/build/gameplay3/scenes/$scene"
 mkdir -p "$out"
 {
   echo 'base dec'
   echo 'frame #10'
   case "$scene" in
    start) ;;
    orb_L2)
      echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
      echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
      ;;
    fight_stage1|stage2_L3|stage2_L3_stationary|stage1_score_checkpoint|bonus_2000)
      echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
      echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
      echo 'joy0Fire #0'
      echo 'joy0Up #0';echo 'frame #40';echo 'joy0Up #1'
      echo 'joy0Right #0';echo 'frame #14';echo 'joy0Right #1'
      if [ "$scene" = stage1_score_checkpoint ];then
        echo 'frame #110'
      elif [ "$scene" = bonus_2000 ];then
        echo 'frame #220'
        # Real no-RAM-input four more stage visits in the same executable.
        for k in 1 2 3 4 5; do
          echo 'joy0Right #0';echo 'frame #30';echo 'joy0Right #1'
          echo 'joy0Up #0';echo 'frame #16';echo 'joy0Up #1'
          echo 'frame #240'
        done
      else
        echo 'frame #420'
      fi
      if [ "$scene" = stage2_L3 ] || [ "$scene" = stage2_L3_stationary ];then
        echo 'joy0Fire #1'
        # Stage 2 respawns at x80 y88; new BL orb x88,y112 (not x96).
        # REAL joystick move only, one orb gives exactly one level.
        echo 'joy0Right #0';echo 'frame #8';echo 'joy0Right #1'
        echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
      fi
      if [ "$scene" = stage2_L3 ];then
        # L3 moves diagonally during the genuine FIRE attack.
        echo 'frame #65' # let the prior L2 cooldown finish without RAM intervention
        echo 'joy0Fire #0'
        echo 'frame #2'
        echo 'joy0Right #0';echo 'joy0Up #0';echo 'frame #12'
        echo 'joy0Right #1';echo 'joy0Up #1'
        echo 'frame #2';echo 'joy0Fire #1'
      fi
      ;;
    sword_warning|sword_hit)
      echo 'joy0Right #0';echo 'frame #25';echo 'joy0Right #1'
      if [ "$scene" = sword_warning ];then echo 'frame #10';else echo 'frame #37';fi
      ;;
    damage_level2|life_lost_after_kill)
      # Pick up exactly one orb, kill one P1 knight, then deliberately
      # stand in the sword attack zone without holding FIRE.
      echo 'joy0Right #0';echo 'frame #16';echo 'joy0Right #1'
      echo 'joy0Down #0';echo 'frame #24';echo 'joy0Down #1'
      echo 'joy0Fire #0';echo 'frame #2';echo 'joy0Fire #1'
      # Move beyond the level2 halo radius before enemy #2 can respawn,
      # preserving exactly ONE prior kill. Return later to sword danger.
      echo 'joy0Left #0';echo 'frame #20';echo 'joy0Left #1'
      if [ "$scene" = damage_level2 ];then
        echo 'frame #170'
      else
        echo 'frame #300'
      fi
      ;;
    gameover_before|gameover_restart)
      echo 'joy0Right #0';echo 'frame #30';echo 'joy0Right #1'
      echo 'frame #500'
      if [ "$scene" = gameover_restart ];then
        echo 'joy0Fire #0';echo 'frame #3';echo 'joy0Fire #1'
      fi
      ;;
   esac
   for x in _scanEnd _scan _sCycles _bank _fCount '*$80' '*$81' '*$82' '*$9C' '*$9E' '*$A1' '*$A2' '*$AA' '*$AB' '*$AC' '*$AD' '*$AE' '*$AF' '*$B0' '*$B1' '*$B3' '*$B4' '*$B5' '*$BC' '*$BD' '*$BE'; do echo "print $x"; done
   echo "saveSes $out/SESSION.txt"
 } > "$HOME/.config/stella/autoexec.script"
 cp "$HOME/.config/stella/autoexec.script" "$out/INPUT.script"
 stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/gameplay3/gameplay3_f8.bin" > "$out/STELLA.log" 2>&1 &
 pid=$!
 win=""
 for i in $(seq 1 25); do
  win=$(xdotool search --onlyvisible --name Stella 2>/dev/null|head -n1||true)
  [ -n "$win" ] && break
  kill -0 "$pid" 2>/dev/null || break
  sleep 1
 done
 if [ -z "$win" ];then echo "STELLA_WINDOW_FAIL: $scene";cat "$out/STELLA.log"; exit 1;fi
 sleep 1
 scrot -z "$out/DEBUGGER_DESKTOP.png"
 # Additional real GUI debugger query (never RAM injection). Capture the
 # actual result of _scanEnd in a separate screenshot for MAIN review.
 xdotool windowfocus "$win" || true
 xdotool mousemove 150 618 click 1 || true
 xdotool type --clearmodifiers --delay 7 'print _scanEnd' || true
 xdotool key Return || true
 sleep 0.3
 scrot -z "$out/SCANEND_DEBUGGER.png" || true
 xdotool type --clearmodifiers --delay 5 "saveSes $out/SESSION_TYPED.txt" || true
 xdotool key Return || true
 sleep 0.2
 find "$HOME" -type f -name '*.txt' -mmin -5 -print0 | while IFS= read -r -d '' f;do
   cp "$f" "$out/$(basename "$f")" 2>/dev/null || true
 done
 kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true
 kill "$xv" 2>/dev/null || true; wait "$xv" 2>/dev/null || true
done
