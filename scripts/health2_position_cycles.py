#!/usr/bin/env python3
"""Exact source-path instruction cycle model for frozen and double-step positioners.
WSYNC beam wait is measured separately by Stella and is not folded into CPU cycles.
"""
from pathlib import Path
import csv,json
out=Path('build/health2_position_cycle_model');out.mkdir(parents=True,exist_ok=True)
rows=[]
for x in range(160):
 old_n=x//15+1; new_n=x//30+1; rem=x%30
 old=5*old_n+26
 new=40+5*new_n+(3 if rem>=15 else 2)+(0 if rem>=15 else 4)
 rows.append({'x':x,'baseline_iterations':old_n,'candidate_iterations':new_n,'baseline_instruction_cycles_including_wsync_write':old,'candidate_instruction_cycles_including_wsync_write':new,'candidate_delta_cycles':new-old,'beam_wait_included':False})
with (out/'cycles_by_x.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
d=[r['candidate_delta_cycles'] for r in rows]
summary={'evidence_class':'SOURCE_ONLY','coordinate_domain':'0..159 screen X','baseline_sha256':'bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5','candidate_sha256':'cc65326332c1b53578e957420454e5efd711a481d99c17d8681d42b8cb32fa63','baseline_mean_cycles':sum(r['baseline_instruction_cycles_including_wsync_write'] for r in rows)/160,'candidate_mean_cycles':sum(r['candidate_instruction_cycles_including_wsync_write'] for r in rows)/160,'candidate_mean_delta_cycles':sum(d)/160,'candidate_slower_positions':sum(x>0 for x in d),'equal_positions':sum(x==0 for x in d),'faster_positions':sum(x<0 for x in d),'worst_regression_cycles':max(d),'best_saving_cycles':min(d),'selected_x':{str(x):{'baseline':rows[x]['baseline_instruction_cycles_including_wsync_write'],'candidate':rows[x]['candidate_instruction_cycles_including_wsync_write'],'delta':rows[x]['candidate_delta_cycles']} for x in (0,33,40,64,80,107,120,159)},'method':'65C02/6507 instruction path count from emitted source structure. Branches are page-local; branch taken/not-taken and loop counts are modeled exactly. Includes STA WSYNC instruction but excludes its raster-dependent wait; not a Stella measurement.'}
(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(f"SOURCE_ONLY position cycles mean baseline={summary['baseline_mean_cycles']:.2f} candidate={summary['candidate_mean_cycles']:.2f} delta={summary['candidate_mean_delta_cycles']:+.2f}; slower={summary['candidate_slower_positions']}/160 faster={summary['faster_positions']}/160 range={summary['best_saving_cycles']}..+{summary['worst_regression_cycles']}")
