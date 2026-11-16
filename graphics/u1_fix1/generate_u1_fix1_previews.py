#!/usr/bin/env python3
"""Rebuild source-driven design images. NO Stella, emulator, TIA, ROM or private sketch."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,random
R=Path(__file__).resolve().parent
S=json.loads((R/'U1_FIX1_BITMAPS.json').read_text('utf8'))
sets=[('U1 FROZEN',S['frozen_U1']),('U1 FIX1',S['single_corrected_U1_FIX1'])]
GRAY=tuple(S['rules']['palette_gray']);FG=(232,239,247);BG=(14,25,37);PANEL=(27,39,54);EDGE=(63,86,105);FOREST=tuple(S['rules']['forest']);NIGHT=tuple(S['rules']['night'])
FF='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(sz,b=False):return ImageFont.truetype(FB if b else FF,sz)
def txt(im,xy,s,sz=14,color=FG,b=False):ImageDraw.Draw(im).text(xy,s,font=font(sz,b),fill=color)
def rows(v,p,f):return v[p] if f=='RIGHT' else v[p+'_left']
def glyph(bits,xr=1,yr=1,bg=FOREST):
    im=Image.new('RGB',(8*xr,12*yr),bg);d=ImageDraw.Draw(im)
    for y,row in enumerate(bits):
        for x,v in enumerate(row):
            if v=='1':d.rectangle((x*xr,y*yr,(x+1)*xr-1,(y+1)*yr-1),fill=GRAY)
    return im
def native(bits,bg=FOREST):
    im=Image.new('RGB',(160,192),bg);g=glyph(bits,1,1,bg);im.paste(g,((160-g.width)//2,(192-g.height)//2));return im
def tv(bits,bg=FOREST):return native(bits,bg).resize((640,480),Image.Resampling.NEAREST)
def crop(bits,bg=FOREST):return tv(bits,bg).crop((200,158,440,322))
def board(name,cards,cols,cell,title,foot='DESIGNFORHANDSVISNING - INTE STELLA',top=88):
    w,h=cell;space=14;ch=48;nr=(len(cards)+cols-1)//cols;out=Image.new('RGB',(space+cols*(w+space),top+nr*(h+ch+space)+48),BG);dr=ImageDraw.Draw(out)
    sz=21
    while dr.textbbox((0,0),title,font=font(sz,True))[2]>out.width-30 and sz>11:sz-=1
    txt(out,(14,18),title,sz,b=True)
    for j,(pic,heading,info) in enumerate(cards):
        x=space+(j%cols)*(w+space);y=top+(j//cols)*(h+ch+space)
        assert pic.size==(w,h)
        dr.rectangle((x-1,y-1,x+w+1,y+h+ch+1),fill=PANEL,outline=EDGE,width=1)
        txt(out,(x+7,y+4),heading,15,b=True);txt(out,(x+7,y+26),info,11,color=(152,175,195))
        out.paste(pic,(x,y+ch))
    txt(out,(14,out.height-32),foot,12,color=(152,175,195))
    out.save(R/name)
# Exact native source PNG: only one corrected U1 family
v=S['single_corrected_U1_FIX1']
for p in 'AB':
    for f in ('RIGHT','LEFT'):
        glyph(rows(v,p,f),bg=tuple(S['rules']['night'])).save(R/f'U1_FIX1_NATIVE_8x12_{p}_{f}.png')
# First unlabelled, not a fabricated blind perception result
states=[(p,f) for p in 'AB' for f in ('RIGHT','LEFT')];random.Random(2026111622).shuffle(states)
board('00_L1_BLIND_FACING.png',[(crop(rows(v,p,f)),f'PROV {i:02}', '240x164 i TV-skala, ingen extra zoom') for i,(p,f) in enumerate(states,1)],2,(240,164),'U1-FIX1: VILKET HALL GAR FIGUREN? (Utan facit)',foot='Endast fyra nya tillstand. Ingen person har testats. DESIGN, INTE STELLA.')
(R/'00_L1_BLIND_ANSWER_KEY.md').write_text('# U1-FIX1 - separat facit\n\nDetta ar en omarkt granskningspanel, inte ett genomfort anvandartest.\n\n| Prov | Pose | Riktning |\n|---:|:---:|---|\n'+'\n'.join(f'| {i:02} | {p} | {f} |' for i,(p,f) in enumerate(states,1))+'\n',encoding='utf8')
# Same-scale before/after 8 cases
cards=[(crop(rows(obj,p,f)),nm+' / '+p+' / '+f, 'Samma L1-skala, 4:3 TV') for nm,obj in sets for p in 'AB' for f in ('RIGHT','LEFT')]
board('01_L1_BEFORE_AFTER_SAME_SCALE.png',cards,4,(240,164),'U1: FORE VS EFTER - 8x12 L1. Samma TV-storlek.')
# Source native 160x192 full screen without enlargement
cards=[(native(rows(obj,p,f)),nm+'/'+p+'/'+f,'160x192, originalraster') for nm,obj in sets for p in 'AB' for f in ('RIGHT','LEFT')]
board('02_L1_NATIVE_160x192.png',cards,4,(160,192),'U1-FIX1: OFORSTORAT 160x192 - 8x12 SPRITE')
# True-size side-by-side full screen (native 160x192 upscaled once for 4:3, no added sprite pixels)
board('03_L1_FULL_TV_4x3.png',[(tv(obj['A']),nm+' / A / RIGHT','640x480 4:3, närmaste granne') for nm,obj in sets],2,(640,480),'SMA SPRITES I HELSPELSKARM 4:3','Kalltillstand 8x12; ingen CRT-filter eller Stella-kernel.')
# Exact matrix before & after 8 cases
pics=[]
for nm,obj in sets:
 for p in 'AB':
  for f in ('RIGHT','LEFT'):
   bit=rows(obj,p,f);im=Image.new('RGB',(320,315),PANEL);d=ImageDraw.Draw(im)
   for y,line in enumerate(bit):
    for x,b in enumerate(line):
     x0=9+x*24;y0=8+y*25
     d.rectangle((x0,y0,x0+22,y0+23),fill=GRAY if b=='1' else BG,outline=EDGE)
    txt(im,(207,11+y*25),line,10,color=(159,183,202))
   pics.append((im,nm+'/'+p+'/'+f,'Enbart for bitgranskning'))
board('04_EXACT_8x12_BITMAPS.png',pics,4,(320,315),'8x12 BITMATRISER - FROZEN U1 MOT U1-FIX1')
# Change annotations (red: removed; cyan: added). Focus row3 x7 extra head pixel, mirrored x0.
pics=[]
for p in 'AB':
 for f in ('RIGHT','LEFT'):
  old=rows(S['frozen_U1'],p,f);new=rows(v,p,f)
  im=Image.new('RGB',(448,356),PANEL);d=ImageDraw.Draw(im)
  for y,(a,b) in enumerate(zip(old,new)):
   for x,(ov,nv) in enumerate(zip(a,b)):
    x0=26+x*32;y0=12+y*28
    color=(229,98,99) if ov=='1' and nv=='0' else (73,211,221) if ov=='0' and nv=='1' else GRAY if nv=='1' else BG
    d.rectangle((x0,y0,x0+30,y0+26),fill=color,outline=EDGE)
   txt(im,(297,15+y*28),b,12,color=(170,195,211))
  pics.append((im,p+' / '+f,'Rod=slackt; cyan=tillagt'))
board('05_CHANGED_PIXELS_AUDIT.png',pics,2,(448,356),'EXAKTA ANDRINGAR I U1-FIX1',foot='Huvud: en borttagen speglad pixel per pose. Resten ar arm/fotkorrigeringar.')
# No direction motion injected into GIFs, otherwise masking artwork ambiguity
for facing in ('RIGHT','LEFT'):
    frames=[crop(rows(v,p,facing)) for p in 'AB']
    frames[0].save(R/f'GIF_U1_FIX1_{facing}_A_B.gif',save_all=True,append_images=frames[1:],duration=[180,180],loop=0,disposal=2,optimize=False)
print('Created exact design previews, 4 source PNGs, 2 GIFs')
