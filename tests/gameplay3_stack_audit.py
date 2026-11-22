#!/usr/bin/env python3
"""Developer-observed RIOT stack canary readback, not independent Verification."""
from pathlib import Path
import json,re
root=Path("build/gameplay3/stack_physical")
report={}
for scene in ("start","combat","after_stage_transition"):
 p=root/scene; data={}
 for start in (240,244,248,252):
  f=p/(f"STACK_{start:02X}.txt")
  if not f.exists():continue
  src=f.read_text(errors="replace")
  for m in re.finditer(r'> print \*\$([0-9a-fA-F]{2})\s*\n([^\n]+)',src):
   adr=int(m.group(1),16)
   v=re.search(r'\$([0-9a-fA-F]{2})\s',m.group(2))
   if v:data[adr]=int(v.group(1),16)
 touched=[a for a,v in data.items() if 0xF0<=a<=0xFF and v!=(0xA5^(a-0xF0))]
 if len(data)!=16:
  print('NOT_VERIFIED_FULL_STACK_CANARY_READBACK',scene,'addresses',sorted(hex(x) for x in data))
  info={'status':'NOT_VERIFIED','read_count':len(data)}
 else:
  depth=0x100-min(touched) if touched else 0
  info={'status':'DEVELOPER_OBSERVED_CANARY','stack_addresses_written':[hex(a) for a in sorted(touched)],
        'measured_max_stack_bytes':depth,'read_count':len(data),
        'all_16_stack_bytes_examined':True,'overflow_into_collision_not_ruled_out_by_canary_alone':True}
  if depth>16:print('HARD_OVERFLOW',scene)
 print('STACK_RIOT',scene,json.dumps(info))
 report[scene]=info
(root/"GAMEPLAY3_STACK_READBACK.json").write_text(json.dumps(report,indent=2))
