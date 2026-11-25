#!/usr/bin/env bash
# Build and compare a rejected shared /30 position-loop experiment against the
# frozen V1 ROM. Test is synthetic RAM-fixture TIA position evidence only.
set -euo pipefail
base_sha=bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5
cand_sha=cc65326332c1b53578e957420454e5efd711a481d99c17d8681d42b8cb32fa63
src=experiments/fullgame1_arrow_halo_20261125
runner=scripts/fullgame1_romdev_v_positions.sh
rom=build/arrow_halo_romdev4/THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin
compat=build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin
out=build/arrow_halo_romdev4
mkdir -p "$out"
test "$(sha256sum "$rom" | cut -d' ' -f1)" = "$base_sha"
test -f "$runner"
git diff --quiet -- "$src/bank3.asm" "$src/build.py" || { echo SOURCE_DIRTY_BEFORE_EXPERIMENT; exit 1; }
restore() {
  git checkout -- "$src/bank3.asm" "$src/build.py" || true
  cp "$out/HEALTH2_FROZEN_BASELINE.bin" "$rom" 2>/dev/null || true
  cp "$out/HEALTH2_FROZEN_BASELINE.bin" "$compat" 2>/dev/null || true
}
trap restore EXIT
cp "$rom" "$out/HEALTH2_FROZEN_BASELINE.bin"
cp -a "$out" "$out/../HEALTH2_BASELINE_BUILD"
# Instrument the same frozen two-phase physical-TIA fixture for real cycle counters.
python3 - "$runner" scripts/health2_v_positions_instrumented.sh "$base_sha" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
needle="'print _sCycles' 'print *$a8'"
replace="'print _sCycles' 'print _fCycles' 'print _fWsyncCycles' 'print _fTimReadCycles' 'print *$a8'"
assert s.count(needle)==1
s=s.replace(needle,replace)
Path(sys.argv[2]).write_text(s)
PY
rm -rf "$out/ROMDEV_V_POSITIONS"
bash scripts/health2_v_positions_instrumented.sh
cp -a "$out/ROMDEV_V_POSITIONS" "$out/../HEALTH2_POSITION_BASELINE"
# Apply candidate source patch only in this disposable Action checkout.
patch -p1 < experiments/health2_position_doublestep.patch
python3 - "$src/build.py" "$cand_sha" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();old='bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5';assert s.count(old)==1;p.write_text(s.replace(old,sys.argv[2]))
PY
python3 "$src/build.py"
test "$(sha256sum "$rom" | cut -d' ' -f1)" = "$cand_sha"
cp "$rom" "$out/HEALTH2_POSITION_CANDIDATE.bin"
cp "$rom" "$compat"
python3 - "$out/../HEALTH2_POSITION_BASELINE" "$cand_sha" <<'PY'
from pathlib import Path
import sys
p=Path('scripts/health2_v_positions_instrumented.sh');s=p.read_text();old='bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5';assert s.count(old)==1;p.write_text(s.replace(old,sys.argv[2]))
PY
rm -rf "$out/ROMDEV_V_POSITIONS"
bash scripts/health2_v_positions_instrumented.sh
cp -a "$out/ROMDEV_V_POSITIONS" "$out/../HEALTH2_POSITION_CANDIDATE"
python3 - "$out/../HEALTH2_POSITION_BASELINE" "$out/../HEALTH2_POSITION_CANDIDATE" "$out/HEALTH2_POSITION_PHYSICAL_COMPARISON.json" <<'PY'
from pathlib import Path
import re,json,sys
base,cand=map(Path,sys.argv[1:3]); result={'evidence_class':'DEVELOPER_OBSERVED','synthetic_fixture':True,'phases':{},'interpretation':'Physical position equivalence only; no gameplay or raster-wide proof.'}
for phase in ('phase_0','phase_2'):
 rec={}
 for which,folder in [('baseline',base),('candidate',cand)]:
  s=(folder/phase/'SESSION.txt').read_text(errors='replace')
  metrics={}
  for key in ('_fCycles','_fWsyncCycles','_fTimReadCycles','_scan','_sCycles'):
   m=re.search(r'> print '+re.escape(key)+r'\s*\n[^\n]*?#(\d+)',s)
   metrics[key]=int(m.group(1)) if m else None
  pos={}
  for obj in ('P0','P1','M0','M1','BL'):
   m=re.search(r'^'+obj+r':[^\n]*?pos=#(\d+)',s,re.M)
   pos[obj]=int(m.group(1)) if m else None
  rec[which]={'metrics':metrics,'positions':pos}
 b=rec['baseline']['positions'];c=rec['candidate']['positions']
 rec['same_physical_positions']=b==c and all(v is not None for v in b.values())
 rec['delta_fCycles']=None if rec['baseline']['metrics']['_fCycles'] is None or rec['candidate']['metrics']['_fCycles'] is None else rec['candidate']['metrics']['_fCycles']-rec['baseline']['metrics']['_fCycles']
 result['phases'][phase]=rec
 assert rec['same_physical_positions'],f'position drift {phase}: {b} vs {c}'
Path(sys.argv[3]).write_text(json.dumps(result,indent=2)+'\n')
print('TIA_POSITION_EQUIVALENCE PASS phases=2; physical position tuple and Stella cycle counters recorded')
for phase,v in result['phases'].items():print(phase,'positions=',v['baseline']['positions'],'candidate_fCycles_delta=',v['delta_fCycles'])
PY
