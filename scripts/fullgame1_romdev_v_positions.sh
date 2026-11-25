#!/usr/bin/env bash
# Synthetic gate checks, NOT a gameplay or pixel oracle. Guard M1 position.
set -euo pipefail
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
root="$PWD/build/arrow_halo_romdev4/ROMDEV_V_POSITIONS"
mkdir -p "$root" "$HOME/.config/stella"
rom="$PWD/build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin"
test "$(sha256sum "$rom" | cut -d' ' -f1)" = "bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5"
for phase in 0 2; do
  export DISPLAY=":$((250+phase))"
  out="$root/phase_$phase"
  mkdir -p "$out"
  Xvfb "$DISPLAY" -screen 0 1400x1000x24 > "$out/xvfb.log" 2>&1 &
  xv=$!
  pid=""
  trap '[ -z "$pid" ] || kill "$pid" 2>/dev/null || true; kill "$xv" 2>/dev/null || true' EXIT
  sleep 1
  printf 'base hex\nframe #10\n' > "$HOME/.config/stella/autoexec.script"
  stella -debug -logtoconsole 1 -audio.enabled 0 -threads 0 -vsync 0 -video software -fullscreen 0 "$rom" > "$out/stella.log" 2>&1 &
  pid=$!
  win=""
  for k in $(seq 1 30); do
    win=$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)
    [ -n "$win" ] && break
    sleep .5
  done
  test -n "$win"
  sleep .4
  xdotool windowfocus "$win"
  xdotool mousemove 155 650 click 1
  send() { xdotool type --clearmodifiers --delay 2 "$1"; xdotool key Return; sleep .1; }
  {
    printf '%s\n' 'base hex' 'ram 80 50 58 03' "ram 8d 0$phase" 'ram 9c 02' 'ram 9e 1e 00 26' 'ram a3 01 00' 'ram b8 78 30' 'ram af 25 18 00 00 00' 'ram e4 00' 'ram e8 51' 'ram d0 25 58 18 00 00 01 00' 'ram d7 7b 58 18 00 00 01 08' 'ram de 82 58 00 00 30 01' 'break $f406' 'run' 'print pc' 'print _bank' 'print _scan' 'print _sCycles' 'print *$a8' 'print *$a9' 'tia'
  } > "$out/COMMANDS.txt"
  while IFS= read -r command; do send "$command"; done < "$out/COMMANDS.txt"
  send "saveSes $out/SESSION.txt"
  scrot -o "$out/desktop.png"
  python3 - "$out/SESSION.txt" "$phase" <<'PY'
import pathlib, re, sys
s=pathlib.Path(sys.argv[1]).read_text(errors="replace")
expected={0:40,2:107}[int(sys.argv[2])]
assert re.search(r"> print pc\s*\n\$f406\b",s,re.I),s
assert re.search(r"> print _bank\s*\n[^\n]*#3\b",s),s
assert re.search(r"M1:.*?pos=#122\b",s),s
assert re.search(r"BL:.*?pos=#"+str(expected)+r"\b",s),s
print("DEVELOPER_OBSERVED synthetic VisibleGate: M1=122 BL="+str(expected))
PY
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  pid=""
  kill "$xv" 2>/dev/null || true
  wait "$xv" 2>/dev/null || true
  trap - EXIT
done
