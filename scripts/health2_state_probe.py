#!/usr/bin/env python3
"""Collect raw Stella RAM dumps per legacy named scenario; probe only, no PASS claims."""
from pathlib import Path
import json, re, sys
root=Path('build/fullgame1/regression/scenes')
scenes=sorted(p.parent for p in root.glob('*/SESSION_TYPED.txt'))
result={}
for d in scenes:
    raw=(d/'SESSION_TYPED.txt').read_text(errors='replace')
    scan=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',raw)
    # Keep the real zero-page RAM view; print *$xx may resolve mirrored TIA
    # addresses and must never be used as a substitute for this dump.
    marker=raw.rfind('> ram')
    end=raw.find('> saveSes',marker) if marker>=0 else -1
    dump=raw[marker:end if end>=0 else None] if marker>=0 else ''
    if not scan or not dump:
        raise SystemExit(f'HEALTH2_PROBE_INCOMPLETE scene={d.name} scan={bool(scan)} ram={bool(dump)}')
    result[d.name]={"scanEnd":int(scan[-1]),"ram_dump":dump[:12000],"state_assertion":"NOT_YET_ASSERTED","evidence_class":"HEALTH_OBSERVED_PROBE_ONLY"}
    print(f'HEALTH2_STATE_PROBE scene={d.name} scanEnd={scan[-1]} ram_bytes={len(dump)}')
Path('build/fullgame1/HEALTH2_RAW_STATE_PROBE.json').write_text(json.dumps(result,indent=2)+'\n')
print('HEALTH2_PROBE_ONLY: state values captured; no gameplay scenario PASS is asserted')
