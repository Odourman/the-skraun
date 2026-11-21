#!/usr/bin/env python3
"""RESEARCH II N6-C bounded source-only replay. Python 3 stdlib, NO ROM.
Replays R3 diagnostic sprite source-row lit-bit windows and next-line P1
main-copy RESP preposition conflicts. NEVER interpret as full TIA feasibility.
Original R3 Git blob: 3c9ed79078eee6a0c63100614a593f92e240b5e8.
Optional command-line argument: path to unmodified R3 original ASM, checked
against exact git SHA1 blob and original 24 EnemyArt bytes.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

R3_SHA='3c9ed79078eee6a0c63100614a593f92e240b5e8'
K={'K1':[0x18,0x3c,0x7e,0xdb,0x5a,0x24,0x66,0x42],
   'K2':[0x24,0x7e,0x5a,0xdb,0x7e,0x3c,0x66,0x81],
   'R':[0x18,0x3c,0x7e,0x5a,0x7e,0x18,0x24,0x42]}
SCENE={'S1':[('K1',32),('K2',101),('R',147)],
       'S2-permuted':[('K2',40),('R',80),('K1',120)],
       'S2-close':[('K1',67),('K2',83),('R',101)],
       'S3':[('K1',105),('K2',124),('R',147)]}
COLOR={'K1':'BLUE','K2':'BLUE','R':'WORLD_CAMO'}
def lit(b):
    return [i for i in range(8) if b & (128>>i)]
def csv_write(path,data):
    with open(path,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]))
        w.writeheader();w.writerows(data)

def verify_r3(path):
    data=Path(path).read_bytes()
    sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert sha==R3_SHA, ('R3 blob mismatch',sha,R3_SHA)
    s=data.decode('utf-8')
    for i,name in enumerate(('K1','K2','R')):
        m=re.search(r'(?m)^EnemyArt'+str(i)+r':\s*\n\s*dc\.b\s+([^\n]+)',s)
        assert m, ('source label missing',i)
        vals=[int(x.strip().replace('$','0x'),16) for x in m.group(1).split(',')]
        assert vals==K[name],(name,vals,K[name])

if len(sys.argv)>1: verify_r3(sys.argv[1])
strict=[]
for scene,actors in SCENE.items():
    for y in range(8):
        for (a,ax),(b,bx) in zip(actors,actors[1:]):
            av=K[a][y];bv=K[b][y]
            al=ax+max(lit(av))
            bf=bx+min(lit(bv))
            gap=bf-al-1
            stores=int(av!=bv)+int(COLOR[a]!=COLOR[b])
            # 3 CPU cycles = 9 TIA clocks per TIA zero-page STA/STX/STY.
            # FULL-INSTRUCTION naive requires both starts and ends in gap.
            naive=gap>=9*stores
            # OPTIMISTIC phase model: store opcode may start while previous
            # pixels draw, but writes only LATCH at completion after last lit.
            # Completions assumed at multiples of 3 clock relative to WSYNC.
            completions=[t for t in range(68+al+1,68+bf) if t%3==0]
            optimistic=(stores==0) or bool(completions and completions[0]+9*(stores-1)<=completions[-1])
            strict.append({'scene':scene,'row':y,'from':a,'to':b,'last_lit_x':al,
                           'next_first_lit_x':bf,'blank_clocks':gap,
                           'GRP1_stores':int(av!=bv),
                           'COLUP1_stores':int(COLOR[a]!=COLOR[b]),
                           'naive_whole_instructions_fit':naive,
                           'preloaded_write_completions_fit':optimistic})
position=[]
for scene in ('S1','S2-close','S3'):
    actors=SCENE[scene]
    for y in range(16):
        a,x=actors[y%3];b,nx=actors[(y+1)%3]
        # Main copy appears one scanline after its RESP reset and ~5 clocks
        # offset. This is approximate for actual TIA phase and a model of
        # one regular P1 main copy per row (NOT close NUSIZ copies).
        reset_clock=68+nx-5
        earliest_old=68+x+min(lit(K[a][y//2]))
        position.append({'scene':scene,'enemy_band_physical_y':y,
                         'source_row':y//2,'outgoing':a,'outgoing_x':x,
                         'next':b,'next_x':nx,
                         'next_RESP1_absolute_TIA_clock':reset_clock,
                         'outgoing_first_lit_absolute_TIA_clock':earliest_old,
                         'reset_before_old_main_draw':reset_clock<earliest_old})
csv_write('P1_R3_ROW_COLOR_BITMAP_BOUNDS.csv',strict)
csv_write('P1_NEXT_LINE_MAIN_RESP_CONFLICT.csv',position)
res={'R3_git_blob':R3_SHA,'source_only':True,
     'not_TIA_emulated':True,'new_N7_ROM_authorized':False,
     'scene_store_gaps':{n:{'naive_fail':sum(x['scene']==n and not x['naive_whole_instructions_fit'] for x in strict),
                          'optimistic_preloaded_fail':sum(x['scene']==n and not x['preloaded_write_completions_fit'] for x in strict)}
                         for n in SCENE},
     'F2_main_preposition_conflicts':{n:sum(x['scene']==n and x['reset_before_old_main_draw'] for x in position)
                                      for n in ('S1','S2-close','S3')},
     'disposition':{'F1_P0_only':'COUNTEREXAMPLE S1/S3 16 of 16 P0 occupied (MAIN source)',
                    'F2_regular_main_only':'COUNTEREXAMPLE 5 of 16 backward preposition resets',
                    'F2_NUSIZ_retrigger':'NOT_YET_DETERMINED',
                    'full_engine':'NOT_YET_DETERMINED'}}
assert res['scene_store_gaps']['S2-close']=={'naive_fail':7,'optimistic_preloaded_fail':0}
assert res['scene_store_gaps']['S3']=={'naive_fail':3,'optimistic_preloaded_fail':0}
assert res['F2_main_preposition_conflicts']=={'S1':5,'S2-close':5,'S3':5}
Path('N6C_SOURCE_COUNTEREXAMPLES.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(json.dumps(res,indent=2,sort_keys=True))
