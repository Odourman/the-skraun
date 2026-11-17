#!/usr/bin/env python3
"""SOURCE model / frozen approved art audit for THE SKRAUN P01-COL1.

Analytical only. Real ROM & TIA need independent executable runtime tests.
The diagnostic map is 4 mirrored bars, NOT one of eight final maps.
"""
import re, json, hashlib
from pathlib import Path
from collections import deque

SRC=Path(__file__).resolve().parents[1]/'experiments/p01_col1_single_arena.asm'
S=SRC.read_text()
ART_TOP_RIGHT=[
    '00100100','01111110','01011010','01100110','00111110','01111111',
    '10111100','00111100','00111100','00100110','00100011','01100000']
ART_TOP_RIGHT_B=[
    '00100100','01111110','01011010','01100110','00111110','01111111',
    '01111101','00111100','00111100','01100100','11000100','00000110']
def flip(rows):return [x[::-1] for x in rows]
def get_bytes(label):
    m=re.search(r'^'+re.escape(label)+r':\s*\n((?:\s+dc\.b\s+[^\n]+\n)+)',S,re.M)
    assert m, label
    return [int(bits,2) for bits in re.findall(r'%([01]{8})',m.group(1))]
expected={
  'A_VISUAL_RIGHT':list(reversed(flip(ART_TOP_RIGHT))),
  'B_VISUAL_RIGHT':list(reversed(flip(ART_TOP_RIGHT_B))),
  'A_VISUAL_LEFT':list(reversed(ART_TOP_RIGHT)),
  'B_VISUAL_LEFT':list(reversed(ART_TOP_RIGHT_B)),
}
for name,rows in expected.items():
    e=[int(v,2) for v in rows]
    got=get_bytes(name)
    assert len(got)==12 and got==e,(name,got,e)
print('ART PASS: bit-exact old-LEFT->new-RIGHT and old-RIGHT->new-LEFT, A+B, 4×12 source rows')

obs=[(12,24,16,24),(132,24,16,24),(24,136,20,16),(116,136,20,16)]
size={1:(8,12),2:(16,24),3:(32,36)}
rects={}
for lv,(w,h) in size.items():
    expected=[]
    for ox,oy,ow,oh in obs:
        expected.extend([max(0,ox-w//2-4+1),min(160,ox+ow+w//2+4),max(0,oy-h//2-4+1),min(176,oy+oh+h//2+4)])
    m=re.search(r'^F01Diag_L'+str(lv)+r':\s*\n((?:\s+dc\.b\s+[^\n]+\n)+)',S,re.M)
    assert m
    embedded=[int(v) for v in re.findall(r'\d+',m.group(1))]
    assert len(embedded)==16 and embedded==expected,(lv,embedded,expected)
    rects[lv]=[tuple(embedded[i:i+4]) for i in range(0,16,4)]
print('COLLISION TABLES PASS: 48 embedded ROM bytes exactly match 4 original-shaped mirrored obstacles × 3 sizes')

def legal(pos,lv,rects=rects):
    x,y=pos;w,h=size[lv];rx=w//2+4;ry=h//2+4
    return rx<=x<=160-rx and ry<=y<=176-ry and not any(x0<=x<x1 and y0<=y<y1 for x0,x1,y0,y1 in rects[lv])

def collision_move(pos,dx,dy,lv):
    x,y=pos
    # THIS is the assembly's X-first, Y-second one-unit axis policy.
    base=x
    xa=(x+dx,y)
    if dx and legal(xa,lv):x+=dx
    ya=(base,y+dy) if dx else (x,y+dy)
    if dy and legal(ya,lv) and legal((x,y+dy),lv):y+=dy
    return x,y

def strict_reference(pos,dx,dy,lv):
    x,y=pos
    xa=(x+dx,y);ya=(x,y+dy);di=(x+dx,y+dy)
    if dx and dy:
        if legal(xa,lv) and legal(ya,lv) and legal(di,lv):return di
        if legal(xa,lv):return xa
        if legal(ya,lv):return ya
        return pos
    return di if legal(di,lv) else pos

counts={};first_mismatch=[];safe=0
for lv in (1,2,3):
    valid={(x,y) for x in range(160) for y in range(176) if legal((x,y),lv)}
    assert (80,88) in valid
    for x,y in valid:
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if not (dx or dy):continue
                dest=collision_move((x,y),dx,dy,lv)
                assert dest in valid
                strict=strict_reference((x,y),dx,dy,lv)
                if strict!=dest and len(first_mismatch)<5:first_mismatch.append((lv,x,y,dx,dy,strict,dest))
                safe+=1
    counts[str(lv)]=len(valid)
assert not first_mismatch,('UNEXPECTED MISMATCH with K0 corner oracle',first_mismatch)
print('STEP PASS:',safe,'8-way moves == strict K0 1-unit source oracle at every legal centre at all three sizes',counts)

# Full-scene geometry model, ONLY a source-level connectivity reference.
for lv in (1,2,3):
    start=(80,88);seen={start};stack=[start]
    while stack:
        x,y=stack.pop()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            d=collision_move((x,y),dx,dy,lv)
            if d not in seen:seen.add(d);stack.append(d)
    assert len(seen)==counts[str(lv)],(lv,len(seen),counts[str(lv)])
print('NAVIGATION PASS: full accessible centre-position graph connected at L1/L2/L3 under the diagnostic geometry')

# Reproduce known original F01 K0 1-unit and 4-unit corner bugs, which are
# from a DIFFERENT ORIGINAL 3-block layout, not our new mirrored 4-block map.
old_obs=[(12,24,16,24),(132,32,16,24),(24,136,20,16)]
legacy={3:[]}
for ox,oy,ow,oh in old_obs:
    w,h=size[3];legacy[3].append((max(0,ox-w//2-4+1),min(160,ox+ow+w//2+4),max(0,oy-h//2-4+1),min(176,oy+oh+h//2+4)))
assert legal((48,69),3,legacy) and legal((47,70),3,legacy)
assert not legal((47,69),3,legacy) # K0 1-clock diagonal endpoint falsely accepted despite corner blocking
assert legal((48,66),3,legacy) and legal((44,70),3,legacy)
# Same old F01 4-clock candidate endpoint, but some intermediate centres blocked.
assert any(not legal((48-i,66+i),3,legacy) for i in range(1,4))
print('NEGATIVE CONTROLS PASS: old F01 one-unit (48,69)->(47,70) corner cut, old four-unit (48,66)->(44,70) tunnel')

# Growth contact locations are from the representative diagnostic map, not real orb pickups.
for x,y in [(80,56),(80,120)]:
    assert legal((x,y),1) and legal((x,y),2) and legal((x,y),3)
assert legal((80,88),3)
# Locate one true Level2-only place where the L2->L3 SELECT must FAIL.
trap=next((p for p in [(x,y) for x in range(160) for y in range(176)] if legal(p,2) and not legal(p,3)),None)
assert trap and not legal(trap,3)
print('GROWTH PASS: central and orb-like positions safe; blocked growth test centre',trap)
print('SOURCE ONLY PASS. Actual assembler, hardware scanlines, joystick/game feel and runtime grow-block are NOT proved here.')
