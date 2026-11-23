#!/usr/bin/env bash
# FULLGAME-1 authentic emulator AUDIO SAMPLE, not subjective listening review.
set -euo pipefail
export SDL_AUDIODRIVER=disk SDL_VIDEODRIVER=x11 SDL_RENDER_DRIVER=software
export SDL_DISKAUDIOFILE="$PWD/build/fullgame1/audio/STELLA_REAL_AUDIO_FLOAT32.raw"
out="$PWD/build/fullgame1/audio"
mkdir -p "$out"
export DISPLAY=:298
Xvfb "$DISPLAY" -screen 0 1400x900x24 > "$out/XVFB_AUDIO.log" 2>&1 &
xvpid=$!
trap 'kill "$xvpid" 2>/dev/null || true' EXIT
sleep 1
# Non-debug real-time Stella. timeout exit 124 is expected when capturing.
set +e
timeout 7 stella -audio.enabled 1 -audio.volume 80 -threads 0 -vsync 0 -video software -fullscreen 0 "$PWD/build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin" > "$out/STELLA_AUDIO.log" 2>&1
result=$?
set -e
if [[ "$result" != 124 && "$result" != 0 ]]; then
  echo "REAL_STELLA_AUDIO_FAILED_EXIT $result"
  exit "$result"
fi
python3 scripts/fullgame1_audio_to_wav.py
