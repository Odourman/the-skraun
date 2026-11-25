#!/usr/bin/env bash
# HEALTH-2 natural joystick scenarios. RAM is read interactively via Stella;
# no test writes RAM or PC. The broken empty-file stress_120 case is replaced
# by the separate individually measured 120-frame test.
set -euo pipefail
runner=scripts/fullgame1_stella_regression.sh
test -f "$runner"
python3 - "$runner" scripts/health2_stella_regression_instrumented.sh <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()
checks=[
  (' stress_120;do',';do'),
  ("if [ \"$scene\" = knight_strike ];then echo 'frame #30';fi",
   "if [ \"$scene\" = knight_strike ];then echo 'frame #23';fi"),
]
for old,new in checks:
  assert src.count(old)==1, f"frozen runner structure changed for {old!r}"
  src=src.replace(old,new)
needle=' xdotool type --clearmodifiers --delay 4 "saveSes $out/SESSION_TYPED.txt" || true'
insert=' xdotool type --clearmodifiers --delay 4 "ram" || true\n xdotool key Return || true\n sleep 0.2\n'+needle
assert src.count(needle)==1, "frozen saveSes command changed"
src=src.replace(needle,insert)
Path(sys.argv[2]).write_text(src)
PY
bash scripts/health2_stella_regression_instrumented.sh
