#!/usr/bin/env bash
# HEALTH-2 probe: frozen natural joystick scenarios, with real Stella RIOT RAM
# command typed interactively so saveSes captures the result in SESSION_TYPED.
set -euo pipefail
runner=scripts/fullgame1_stella_regression.sh
test -f "$runner"
python3 - "$runner" scripts/health2_stella_regression_instrumented.sh <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()
needle='  xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true'
insert='  xdotool type --clearmodifiers --delay 4 "ram" || true\n  xdotool key Return || true\n  sleep 0.2\n'+needle
assert src.count(needle)==1, "frozen runner structure changed; refusing silent patch"
src=src.replace(needle,insert)
Path(sys.argv[2]).write_text(src)
PY
bash scripts/health2_stella_regression_instrumented.sh
