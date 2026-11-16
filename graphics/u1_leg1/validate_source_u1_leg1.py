#!/usr/bin/env python3
"""GitHub-branch source-only validator. Media/GIF/ZIP validator in Drive ZIP."""
from pathlib import Path
import json
s=json.loads((Path(__file__).resolve().parent/'SOURCE_U1_LEG1.json').read_text(encoding='utf-8'))
a=s['frozen_U1_FIX1'];b=s['one_candidate_U1_LEG1']
assert s['frozen_baseline_github_blob_sha']=='811bd1f7da51d1003174423f30e6b8d0ebe77b1c'
assert set(a)==set(b)=={'A','B'}
for p in 'AB':
    assert len(a[p])==len(b[p])==12
    assert all(len(r)==8 and set(r)<=set('01') for r in b[p])
    assert a[p][:9]==b[p][:9], 'Upper nine rows were changed'
    assert a[p][9:]!=b[p][9:], 'No lower leg change'
    assert a[p][3]==b[p][3]=='01100110', 'Head correction lost'
    assert any(c1!=c2 for x,y in zip(a[p][9:],b[p][9:]) for c1,c2 in zip(x,y))
assert b['A'][9:]==['00100110','00100011','01100000']
assert b['B'][9:]==['01100100','11000100','00000110']
print('PASS: A/B 8x12, original y0..8 frozen, goat-like alternating lower y9-11, exact mirrored LEFT derived from reversed rows; no subjective acceptance')
