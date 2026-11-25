#!/usr/bin/env python3
"""Fail CI when a named natural scenario misses its asserted state or is unproven."""
from pathlib import Path
import json,sys
p=(Path(sys.argv[1])/'HEALTH2_SCENE_STATES.json') if len(sys.argv)>1 else Path('build/fullgame1/HEALTH2_SCENE_STATES.json')
r=json.loads(p.read_text()); checks=r['scenario_checks']
failed={k:v for k,v in checks.items() if v['status']!='PASS'}
print(f"SCENARIO_ASSERTIONS pass={sum(v['status']=='PASS' for v in checks.values())} fail={sum(v['status']=='FAIL' for v in checks.values())} unproven={sum(v['status']=='UNPROVEN' for v in checks.values())}")
if failed:
 for n,v in failed.items():print('SCENARIO_NOT_PASS',n,v.get('status'),v.get('reason',v.get('actual',{})))
 raise SystemExit(1)
print('ALL_NATURAL_SCENARIO_ASSERTIONS_PASS')
