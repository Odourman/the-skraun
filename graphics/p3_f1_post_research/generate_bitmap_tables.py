#!/usr/bin/env python3
"""Produce pure art-only dc.b records (NOT ROM/CPU/kernel code)."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
S=json.loads((R/'SOURCE_8x12.json').read_text('utf8'))
items={'U1_FROZEN':S['baseline']['U1_frozen'],'D1_NEW':S['new_candidates']['D1_head_expression'],'D2_NEW':S['new_candidates']['D2_swaying_arms']}
lines=['; SKRAUN P3-F1 POST RESEARCH - GRAPHICS-ONLY TABLES, NO EXECUTABLE CODE',
       '; 8x12 P0 source bitmaps. TOP_FIRST top of sprite -> bottom. BOTTOM_FIRST reversed row order.',
       '; LEFT = bit-exact 8-bit reversal per row. DO NOT assume these are integrated in any kernel.',
       '; NO M0, NO NUSIZ changes, NO extra color channels, NO UP/DOWN sprite.', '']
for name,v in items.items():
 for pose in 'AB':
  for facing in ('RIGHT','LEFT'):
   rr=v[pose] if facing=='RIGHT' else v[pose+'_left']
   for order in ('TOP_FIRST','BOTTOM_FIRST'):
    label=f'SkraunP3F1_Post_{name}_{pose}_{facing}_{order}:'
    lines.append(label)
    lines.extend('dc.b %'+q for q in (rr if order=='TOP_FIRST' else rr[::-1]))
    lines.append('')
(R/'PIXEL_DATA_ONLY.inc').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Generated art-only data labels',len(items)*2*2*2)
