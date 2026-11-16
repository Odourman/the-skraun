#!/usr/bin/env python3
"""Objective source-bit comparison only, NEVER a human perceptual readability test."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
S=json.loads((R/'P3_F1_SOURCE_BITMAPS.json').read_text(encoding='utf-8'))
items={'U1_frozen':S['frozen_control']['U1_frozen'],**S['new_candidates']}
def hd(a,b):return sum(c!=d for x,y in zip(a,b) for c,d in zip(x,y))
def headhd(a,b):return sum(c!=d for x,y in zip(a[:5],b[:5]) for c,d in zip(x,y))
data={}
for n,v in items.items():
 ar,al,br,bl=v['A'],v['A_left'],v['B'],v['B_left']
 data[n]={
  'A_RIGHT__A_LEFT':hd(ar,al),'B_RIGHT__B_LEFT':hd(br,bl),
  'A_RIGHT__B_RIGHT':hd(ar,br),'A_LEFT__B_LEFT':hd(al,bl),
  'A_RIGHT__B_LEFT':hd(ar,bl),'A_LEFT__B_RIGHT':hd(al,br),
  'A_RIGHT__A_LEFT_HEAD_ONLY_ROWS_0_4':headhd(ar,al),
  'B_RIGHT__B_LEFT_HEAD_ONLY_ROWS_0_4':headhd(br,bl),
  'A_RIGHT__B_RIGHT_HEAD_ONLY_ROWS_0_4':headhd(ar,br),
  'four_case_pairwise_matrix_order':['A_RIGHT','A_LEFT','B_RIGHT','B_LEFT'],
  'four_case_pairwise_matrix':[[hd(a,b) for b in (ar,al,br,bl)] for a in (ar,al,br,bl)]
 }
result={'caution':'NO PERCEPTUAL PASS: Hamming only counts bit differences; family silhouette and direction at actual L1 require user review.','source_cells':96,'families':data}
(R/'HAMMING_AUDIT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for n,r in data.items():print(n,{k:v for k,v in r.items() if k.endswith('LEFT') or k.endswith('RIGHT')})
