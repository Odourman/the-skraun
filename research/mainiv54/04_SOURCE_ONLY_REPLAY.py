#!/usr/bin/env python3
"""RESEARCH II / MAIN IV 54-ID source-only replay, Python 3 stdlib.
Usage: python3 04_SOURCE_ONLY_REPLAY.py
Must run in research/mainiv54 directory with 01_ALL_54_ISSUES_MATRIX.csv.
Only tabular coverage and nominal arithmetic: NO ROM, emulator, TIA or Stella.
"""
import csv,collections,json,pathlib
here=pathlib.Path(__file__).resolve().parent
with (here/'01_ALL_54_ISSUES_MATRIX.csv').open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f))
ids=[int(r['ID']) for r in rows]
assert sorted(ids)==list(range(1,55)), "Expected all 54 unique issue IDs"
counts=dict(sorted(collections.Counter(r['current_status'] for r in rows).items()))
expected={
  'CONFIRMED_GAMEPLAY4A_DEFECT':4,
  'UNIMPLEMENTED_CANON':18,
  'REAL_INTEGRATION_RISK':8,
  'PARTIAL_OR_UNVERIFIED':22,
  'LEGACY_ONLY':2}
assert counts==dict(sorted(expected.items())), counts
out={
 'source_only':True,'issue_ids':ids,'count':len(rows),'classes':counts,
 'nominal_cpu_cycles_per_ntsc_line':76,
 'nominal_color_clocks_per_line':228,
 'tim64t_34_nominal_cycles':34*64,
 'tim64t_34_nominal_scanlines':round(34*64/76,6),
 'old_m1_indirect_5cy_and_store_3cy_min':8,
 'old_m1_indirect_page_cross_and_store':9,
 'preloaded_m0_enam0_store_min_cycles':3,
 'hardware_or_stella_proof':False}
print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))
