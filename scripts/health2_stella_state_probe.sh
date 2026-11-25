#!/usr/bin/env bash
# HEALTH-2 probe: rerun the frozen natural joystick scenarios and append a real
# Stella RIOT RAM dump to every debugger session. It does not inject RAM/PC.
set -euo pipefail
runner=scripts/fullgame1_stella_regression.sh
test -f "$runner"
python3 - "$runner" scripts/health2_stella_regression_instrumented.sh <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()
needle='   echo "saveSes $out/SESSION.txt"'
assert src.count(needle)==1, "frozen runner structure changed; refusing silent patch"
src=src.replace(needle, "   echo 'ram'\n"+needle)
Path(sys.argv[2]).write_text(src)
PY
bash scripts/health2_stella_regression_instrumented.sh
