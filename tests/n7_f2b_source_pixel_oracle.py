#!/usr/bin/env python3
"""Bounded R3 source-to-authentic-Stella TIA pixel oracle for N7/F2b S2 close.
Input: real Stella debugger 320x228 TIA_001..TIA_012.png captured from
actual compiled 4KiB ROM; no synthetic/paper sprite counts accepted as PASS.

python3 tests/n7_f2b_source_pixel_oracle.py build/n7/stella-s2-12

The crop's observed S2 first source row is screenshot Y109 under Stella 6.7.1.
The palette RGB comes from authentic NTSC TIA captures (not final game canon).
"""
import sys, json, hashlib
from pathlib import Path
from PIL import Image

root=Path(sys.argv[1])
rows={
  'K1': [0x18,0x3C,0x7E,0xDB,0x5A,0x24,0x66,0x42],
  'K2': [0x24,0x7E,0x5A,0xDB,0x7E,0x3C,0x66,0x81],
  'Ranger': [0x18,0x3C,0x7E,0x5A,0x7E,0x18,0x24,0x42],
}
color={
 'K1': (121,194,251), 'K2': (121,194,251),
 'Ranger': (61,151,60)
}
screenx={'K1':67,'K2':83,'Ranger':101}
first_y=109
paths=[root/f'TIA_{i:03}.png' for i in range(1,13)]
assert all(p.is_file() for p in paths),('need 12 authentic consecutive TIA screenshots',[str(x) for x in paths if not x.is_file()])

expected={}
for actor,mask in rows.items():
    points=set()
    for i,b in enumerate(mask):
        for duplicate in (0,1):
            y=first_y+i*2+duplicate
            for pixel in range(8):
                if b&(0x80>>pixel):
                    x=2*(screenx[actor]+pixel)
                    points.add((x,y,color[actor]))
                    points.add((x+1,y,color[actor]))
    expected[actor]=points

reports=[]
for path in paths:
    im=Image.open(path).convert('RGB')
    assert im.size==(320,228),(path,im.size)
    actual={(x,y,im.getpixel((x,y))) for y in range(first_y,first_y+17)
                                     for x in range(320)
                                     if im.getpixel((x,y)) in set(color.values())}
    match={}
    for actor,required in expected.items():
        m=len(required&actual)
        first_bad=next((y for y in range(first_y,first_y+16)
                    if any(q not in actual for q in required if q[1]==y)), None)
        match[actor]={'required_pixels':len(required),'correct_pixels':m,
                      'correct_percent':round(m/len(required)*100,2),
                      'all_source_pixels_in_correct_color_at_correct_x':m==len(required),
                      'first_failed_screenshot_row':first_bad}
    reports.append({'capture':path.name,
                   'visible_color_pixels_after_16rows':sum(y==first_y+16 for x,y,c in actual),
                   'actors':match,
                   'sha256_of_actual_rgb':hashlib.sha256(im.tobytes()).hexdigest()})

summary={actor:sum(x['actors'][actor]['all_source_pixels_in_correct_color_at_correct_x']
                   for x in reports) for actor in rows}
verdict=('F2b_PASS_ONLY_FOR_TESTED_SCENE' if all(n==12 for n in summary.values())
         else 'F2b_FAIL_FOR_TESTED_SCENE')
result={
  'classification': 'ROM DEVELOPMENT developer self-test, NOT independent Verification',
  'fixture':'S2 close, x67/83/101, all original R3 8-row data each doubled to 16 source rows',
  'first_failed_screenshot_row':min(x['actors'][a]['first_failed_screenshot_row']
       for x in reports for a in rows if x['actors'][a]['first_failed_screenshot_row'] is not None),
  'full_correct_frames_by_actor_out_of_12':summary,
  'verdict':verdict,
  'frames':reports
}
(root.parent/'N7_F2B_TRUE_PIXEL_SOURCE_ORACLE.json').write_text(json.dumps(result,indent=2))
print('Source-exact bitmap+X+color verdict:',verdict)
print('Full exact frames/12:',summary)
print('First physical source-pixel mismatch: screenshot row',result['first_failed_screenshot_row'])
for a in rows: print(a, reports[0]['actors'][a])
