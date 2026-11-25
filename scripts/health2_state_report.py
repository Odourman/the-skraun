#!/usr/bin/env python3
"""Decode Stella `ram` dumps and evaluate intended natural-scene states.
No RAM/PC injection is used for these joystick scenes.
"""
from pathlib import Path
import re,json,sys
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path('build/fullgame1')
scenedir=base/'regression/scenes'
addresses={'PlayerX':0x80,'PlayerY':0x81,'Level':0x82,'HaloFrames':0x9e,'HaloRadius':0xa0,'OrbMask':0x9c,'ArrowDX':0xa3,'ArrowDY':0xa4,'Stage':0xaa,'Lives':0xac,'ScoreLo':0xad,'ScoreHi':0xae,'StageKills':0xb4,'KillsNeed':0xb5,'SwordWarn':0xb0,'SwordStrike':0xb1,'SwordRest':0xb2,'ArrowX':0xb8,'ArrowY':0xb9,'K1X':0xd0,'K1Y':0xd1,'K1Warn':0xd2,'K1Strike':0xd3,'K1Rest':0xd4,'K1Alive':0xd5,'K2X':0xd7,'K2Y':0xd8,'K2Warn':0xd9,'K2Strike':0xda,'K2Rest':0xdb,'K2Alive':0xdc,'RX':0xde,'RY':0xdf,'RDraw':0xe0,'RRelease':0xe1,'RCool':0xe2,'RAlive':0xe3,'Reserves':0xe5}
expected_scenes={'start','knight_warning','knight_strike','knight_rest','ranger_phase4','ranger_phase12','ranger_phase22','ranger_phase29','ranger_phase35','ranger_draw','ranger_release','arrow_first','arrow_mid','arrow_later','stage2_L3','gameover_restart'}
checks={
 'start':('stage1_level1_lives3',lambda s:s['Stage']==1 and s['Level']==1 and s['Lives']==3),
 'knight_warning':('a_knight_warning_timer_is_active',lambda s:s['K1Warn']>0 or s['K2Warn']>0),
 'knight_strike':('a_knight_strike_timer_is_active',lambda s:s['K1Strike']>0 or s['K2Strike']>0),
 'knight_rest':('a_knight_rest_timer_is_active',lambda s:s['K1Rest']>0 or s['K2Rest']>0),
 'ranger_draw':('RDraw>0_and_no_arrow_yet',lambda s:s['RDraw']>0 and s['ArrowDX']==0),
 'ranger_release':('RRelease>0_and_arrow_active',lambda s:s['RRelease']>0 and s['ArrowDX']!=0),
 'arrow_first':('arrow_active',lambda s:s['ArrowDX']!=0),
 'arrow_mid':('arrow_active',lambda s:s['ArrowDX']!=0),
 'arrow_later':('arrow_active',lambda s:s['ArrowDX']!=0),
 'stage2_L3':('stage2_and_level3',lambda s:s['Stage']>=2 and s['Level']==3),
}
results={}
for session in sorted(scenedir.glob('*/SESSION_TYPED.txt')):
 raw=session.read_text(errors='replace'); name=session.parent.name
 if name=='stress_120': continue
 marker=raw.rfind('> ram'); end=raw.find('> saveSes',marker)
 if marker<0 or end<0: raise SystemExit(f'RAM_DUMP_MISSING {name}')
 ram={}
 for line in raw[marker:end].splitlines():
  m=re.match(r'^([0-9a-fA-F]{2}):\s+(.+)$',line)
  if m:
   vals=re.findall(r'\b[0-9a-fA-F]{2}\b',m.group(2))
   for i,v in enumerate(vals[:16]):ram[int(m.group(1),16)+i]=int(v,16)
 if len(ram)!=128:raise SystemExit(f'RAM_DUMP_NOT_128_BYTES {name} got={len(ram)}')
 s={k:ram[a] for k,a in addresses.items()}
 scan=re.findall(r'> print _scanEnd\s*\n[^\n]*?#(\d+)',raw)
 s.update(scene=name,scanEnd=int(scan[-1]) if scan else None,evidence_class='HEALTH_OBSERVED_NATURAL_JOYSTICK_STATE')
 results[name]=s
if set(results)!=expected_scenes:
 raise SystemExit(f'SCENE_SET_MISMATCH missing={sorted(expected_scenes-set(results))} extra={sorted(set(results)-expected_scenes)}')
scene_checks={}
for name,(intent,fn) in checks.items():
 s=results[name]; ok=bool(fn(s)) and s['scanEnd']==262
 scene_checks[name]={'intent':intent,'status':'PASS' if ok else 'FAIL','actual':{k:s[k] for k in ('Stage','Level','PlayerX','PlayerY','K1Warn','K1Strike','K1Rest','K2Warn','K2Strike','K2Rest','RDraw','RRelease','RCool','RAlive','ArrowDX','ArrowX','ArrowY','Lives','ScoreLo','ScoreHi','scanEnd')}}
# These sampled phases must contain a live Ranger and an active arrow, with
# distinct arrow coordinates proving the script did not merely rename one frame.
phase_names=['ranger_phase4','ranger_phase12','ranger_phase22','ranger_phase29','ranger_phase35']
phase_coords={(results[n]['ArrowX'],results[n]['ArrowY']) for n in phase_names}
phase_ok=all(results[n]['RAlive'] and results[n]['ArrowDX'] for n in phase_names) and len(phase_coords)==len(phase_names) and all(results[n]['scanEnd']==262 for n in phase_names)
scene_checks['ranger_phase_samples']={'intent':'five_distinct_live_arrow_positions','status':'PASS' if phase_ok else 'FAIL','coordinates':{n:[results[n]['ArrowX'],results[n]['ArrowY']] for n in phase_names}}
# Final-state-only observation cannot prove that GameOver happened before restart.
scene_checks['stage2_transition']={'intent':'reach_stage2_after_stage1_clear','status':'PASS' if results['stage2_L3']['Stage']==2 and results['stage2_L3']['scanEnd']==262 else 'FAIL','actual':{'Stage':results['stage2_L3']['Stage'],'Level':results['stage2_L3']['Level'],'StageKills':results['stage2_L3']['StageKills'],'KillsNeed':results['stage2_L3']['KillsNeed'],'scanEnd':results['stage2_L3']['scanEnd']}}
scene_checks['gameover_restart']={'intent':'observe_game_over_and_subsequent_restart','status':'UNPROVEN','reason':'The frozen scenario saves only the final RAM state; it has no checkpoint at GameOver. End state is not evidence that GameOver occurred.'}
report={'evidence_class':'HEALTH_OBSERVED','rom_sha256':'bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5','scene_states':results,'scenario_checks':scene_checks,'note':'Natural joystick sessions; 128-byte Stella RIOT RAM command dump parsed by address. No debugger RAM/PC writes.'}
out=base/'HEALTH2_SCENE_STATES.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(f'SCENE_STATE_REPORT scenes={len(results)} scenarios={len(scene_checks)}')
for name,c in scene_checks.items():print(f"SCENE_ASSERT {name} {c['status']} {c['intent']}")
