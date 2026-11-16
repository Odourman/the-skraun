#!/usr/bin/env python3
"""Pixel-source distance audit only: never a perceptual correctness claim."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
S=json.loads((R/'SOURCE_8x12.json').read_text('utf8'))
F={'U1':S['baseline']['U1_frozen'],'D1':S['new_candidates']['D1_head_expression'],'D2':S['new_candidates']['D2_swaying_arms']}
def h(a,b):return sum(x!=y for r,s in zip(a,b) for x,y in zip(r,s))
log={}
for name,v in F.items():
 names=['A_RIGHT','A_LEFT','B_RIGHT','B_LEFT']
 obj=[v['A'],v['A_left'],v['B'],v['B_left']]
 log[name]={'states':names,'pairwise_hamming_96_cells':[[h(x,y) for y in obj] for x in obj],
   'A_R_vs_A_L':h(obj[0],obj[1]),'B_R_vs_B_L':h(obj[2],obj[3]),
   'A_R_vs_B_L':h(obj[0],obj[3]),'A_R_vs_B_R':h(obj[0],obj[2]),
   'head_only_A_R_vs_A_L':h(obj[0][:6],obj[1][:6]),
   'head_only_A_vs_B':h(obj[0][:6],obj[2][:6])}
result={'warning':'SOURCE HAMMING ONLY, NOT HUMAN FACING/IDENTITY PROOF','method':'number of differing cells out of 96; head-only rows 0-5','families':log}
(R/'SOURCE_DISTANCE_AUDIT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
for name,v in log.items():print(name,'A R/L',v['A_R_vs_A_L'],'B R/L',v['B_R_vs_B_L'],'Cross A-R/B-L',v['A_R_vs_B_L'],'Pose',v['A_R_vs_B_R'])
