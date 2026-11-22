#!/usr/bin/python3
"""GAMEPLAY-2 authentic Stella 6.7.1 pixel audit; status closed on unsupported events."""
from pathlib import Path
from PIL import Image
import numpy as np
import hashlib, json, re
root=Path('build/gameplay2/scenes')
names=('start','orb_L2','fight_stage1','stage2_L3','sword_warning','sword_hit','gameover_restart')
reports={}
def box(mask):
    y,x=np.where(mask)
    if not len(x): return None
    return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
for name in names:
    pic=root/name/'DEBUGGER_DESKTOP.png'
    assert pic.exists(),f'NO REAL STELLA screenshot {pic}'
    img=Image.open(pic).convert('RGB').crop((121,115,441,343))
    assert img.size==(320,228)
    img.save(root/name/'ACTUAL_TIA.png')
    a=np.asarray(img)
    gray=np.all(a==[210,210,209],axis=2)
    blue=np.all(a==[121,194,251],axis=2)
    gold=np.all(a==[234,194,84],axis=2)
    sess=root/name/'SESSION.txt'
    sess_data=sess.read_text(errors='replace') if sess.exists() else ''
    formats=[x.strip() for x in (root/name/'STELLA.log').read_text(errors='replace').splitlines() if 'Display Format:' in x]
    reports[name]={'P0_bbox':box(gray),'P0_gray_pixels':int(gray.sum()),
        'P1_blue_pixels':int(blue.sum()),'gold_pixels':int(gold.sum()),
        'rgb_sha256':hashlib.sha256(a.tobytes()).hexdigest(),
        'format_logs':formats[:2],'session_exists':bool(sess_data),
        'session_tail':sess_data[-1800:]}
    print('PHYSICAL_TIA',name,json.dumps({k:v for k,v in reports[name].items() if k!='session_tail'}))
def dim(k):
    b=reports[k]['P0_bbox']
    return None if b is None else (b[2]-b[0],b[3]-b[1])
assert dim('start')==(16,12),('start P0 physical U1 source',dim('start'))
assert reports['start']['P0_gray_pixels']==98, 'U1-LEG1 exact baseline source pixels not visible'
assert reports['start']['P1_blue_pixels']==120, 'P1 source sprite corrupted'
assert dim('orb_L2')==(32,24),('orb did not physically upgrade 1->2',dim('orb_L2'))
assert reports['start']['gold_pixels']==0,'gold attack leaked off state'
assert reports['sword_warning']['P1_blue_pixels']==0,'P1 warning still original blue'
reportfile=Path('build/gameplay2/PHYSICAL_AUDIT.json')
reportfile.write_text(json.dumps(reports,indent=2))
print('PASS: bounded authentic Stella base sprite, 1->2 orb sprite, knight and warning')
for name in ('fight_stage1','stage2_L3'):
    print('NOT VERIFIED UNLESS SESSION SHOWS EXPECTED RAM:',name,'P0_DIM',dim(name),
          'SESSION',reports[name]['session_exists'])
print('PHYSICAL 262-SCANLINE: NOT VERIFIED without readable _scanEnd frame trace.')
