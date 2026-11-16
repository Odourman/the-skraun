#!/usr/bin/env python3
"""Deterministic design-only 8x12 glyph previews. Never claims Stella output. Pillow required."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

ROOT=Path(__file__).resolve().parent
S=json.loads((ROOT/'P2_SPRITES_SOURCE.json').read_text(encoding='utf8'))
NAMES=['P1 A (FRYST)','I1 HEAD SIGNATURE','I2 LIMB SIGNATURE']
KEYS=['frozen_P1_A','I1_head_signature','I2_limb_signature']
DATA=[S['frozen_P1_A'],S['new_candidates']['I1_head_signature'],S['new_candidates']['I2_limb_signature']]
GRAY=tuple(S['preview']['palette_gray_RGB'])
FOREST=tuple(S['preview']['forest_RGB']); NIGHT=tuple(S['preview']['night_RGB'])
DARK=(15,23,32); INK=(230,237,243); MUTE=(150,166,183); LINE=(54,75,92)
fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fontbold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font18=ImageFont.truetype(fontfile,18);font14=ImageFont.truetype(fontfile,14)
font22=ImageFont.truetype(fontbold,22);font16=ImageFont.truetype(fontbold,16)

def glyph(rows,fc=GRAY,bg=DARK,xrep=1,yrep=1):
    out=Image.new('RGB',(8*xrep,12*yrep),bg)
    d=ImageDraw.Draw(out)
    for yy,r in enumerate(rows):
        assert len(r)==8
        for xx,c in enumerate(r):
            if c=='1': d.rectangle((xx*xrep,yy*yrep,(xx+1)*xrep-1,(yy+1)*yrep-1),fill=fc)
    return out

def frame(rows,bg=DARK,level=1,original=True):
    info=S['levels'][str(level)]; raw=glyph(rows,GRAY,bg,info['x_repeat'],info['row_repeat'])
    fr=Image.new('RGB',(160,192),bg)
    fr.paste(raw,((160-raw.width)//2,(192-raw.height)//2))
    return fr if original else fr.resize((640,480),Image.Resampling.NEAREST)

def annotated_sheet(frames,labels,cols,cell=(640,480),footer='DESIGN PREVIEW ONLY / NOT STELLA / nearest neighbor 4:3 approximation',scale=1):
    w,h=cell;rows=(len(frames)+cols-1)//cols
    head=39;gutter=12;foot=48
    im=Image.new('RGB',(cols*(w+gutter)+gutter,rows*(h+head+gutter)+foot),DARK)
    d=ImageDraw.Draw(im)
    for idx,(f,label) in enumerate(zip(frames,labels)):
        x=gutter+(idx%cols)*(w+gutter);y=gutter+(idx//cols)*(h+head+gutter)
        d.text((x+4,y+6),label,font=font18 if w>=300 else font14,fill=INK)
        if f.size!=cell:f=f.resize(cell,Image.Resampling.NEAREST)
        im.paste(f,(x,y+head))
        d.rectangle((x-1,y+head-1,x+w,y+head+h),outline=LINE,width=1)
    d.text((gutter,im.height-35),footer,font=font14,fill=MUTE)
    return im

# Exact unenhanced native glyphs; 6 sprite source file pairs, no hidden resampling
for i,key in enumerate(['P1_A_FROZEN','I1_HEAD','I2_LIMB']):
    for pose in ('A','B'):
        glyph(DATA[i][pose]).save(ROOT/f'NATIVE_8x12_{key}_{pose}.png')

# True 160x192 native arena pixels (unscaled); montage is two rows each with raw panels.
raws=[];labs=[]
for pose in ('A','B'):
    for k,v in zip(NAMES,DATA):raws.append(frame(v[pose],FOREST,1,True));labs.append(f'{("P1 A","I1","I2")[len(labs)%3]} / {pose} - native')
annotated_sheet(raws,labs,3,cell=(160,192),footer='NATIVE 160x192 / 8x12 glyph / DESIGN / NOT Stella').save(ROOT/'01_L1_NATIVE_160x192_UNENHANCED.png')
# Same pixel positions in actual approximate 4:3 640x480 output
annotated_sheet([frame(v[p],FOREST,1,False) for p in ('A','B') for v in DATA],
               [f'{k} - L1 pose {p} (8 x 12)' for p in ('A','B') for k in NAMES],3).save(ROOT/'02_L1_TV_4x3_NATIVE_COMPARISON.png')

# B/W silhouette only, equal-sized source data sheets, do not draw additional facial details
bw=[];bl=[]
for p in ('A','B'):
 for k,v in zip(NAMES,DATA):
    tiny=glyph(v[p],(0,0,0),(255,255,255)).resize((8*28,12*28),Image.Resampling.NEAREST)
    bw.append(tiny);bl.append(f'{("P1-A","I1","I2")[len(bl)%3]} / {p} / B-W')
annotated_sheet(bw,bl,3,cell=(224,336),footer='SOURCE BLACK-WHITE SILHOUETTES, enlarged pixel blocks; NOT Stella').save(ROOT/'03_BLACK_WHITE_SOURCE_SILHOUETTES.png')

# Exact matrices and mirrored rows in four arrangements, no smoothing
boards=[];lab=[]
for i,(k,v) in enumerate(zip(NAMES,DATA)):
 for p in ('A','B'):
  for face in ('right','left'):
   rows=v[p] if face=='right' else (v[p+'_left'] if p+'_left' in v else v['left_'+p])
   # distinct matrix; black grid and labeled binary rows
   sheet=Image.new('RGB',(320,360),(19,30,41));d=ImageDraw.Draw(sheet)
   for y,r in enumerate(rows):
    for x,ch in enumerate(r):
     d.rectangle((25+x*27,18+y*27,25+(x+1)*27-2,18+(y+1)*27-2),fill=GRAY if ch=='1' else (31,43,56))
    d.text((246,19+y*27),r,font=font14,fill=MUTE)
   boards.append(sheet);lab.append(f'{("P1-A","I1","I2")[i]} / {p} / {face.upper()}')
annotated_sheet(boards,lab,3,cell=(320,360),footer='BINARY SOURCE BOARDS / exact bits / left is per-row horizontal reversal / NOT Stella').save(ROOT/'04_EXACT_BITMAPS_BOTH_FACINGS.png')

# Full TV conceptual L2 L3 comparisons on 4:3 with source-based row repetition
fr=[];labs=[]
for lev in (2,3):
 for k,v in zip(NAMES,DATA):
    fr.append(frame(v['A'],NIGHT,lev,False));labs.append(f'{k}  / L{lev} ({S["levels"][str(lev)]["width_cc"]}x{S["levels"][str(lev)]["height_scanlines"]})')
annotated_sheet(fr,labs,3,footer='CONCEPTUAL 2X/4X WIDTH + 2X/3X ROW REPEAT; L3 ART1 had a REAL bug; THESE ARE NOT STELLA').save(ROOT/'05_L2_L3_CONCEPTUAL_LEVELS.png')

# Contrast across TWO flat backgrounds, no PF claims
fr=[];labs=[]
for bg,name in [(FOREST,'FOREST'),(NIGHT,'NIGHT')]:
 for k,v in zip(NAMES,DATA):
    fr.append(frame(v['A'],bg,1,False));labs.append(f'{k} / L1 / flat {name}')
annotated_sheet(fr,labs,3,footer='FLAT BACKGROUNDS ONLY; no TIA PF renderer, no fabricated Stella').save(ROOT/'06_L1_FOREST_NIGHT_FLAT_BACKGROUND.png')

# A/B pixel changes (source-level) with a minimal overlay to demonstrate moving limb zones
changes=[];labels=[]
for k,v in zip(NAMES,DATA):
  tiny=Image.new('RGB',(650,350),DARK);d=ImageDraw.Draw(tiny)
  for idx,p in enumerate(('A','B')):
   rows=v[p]; off=12+idx*325
   for y,row in enumerate(rows):
    for x,c in enumerate(row):
     changed=(v['A'][y][x]!=v['B'][y][x])
     box=(off+x*28,10+y*28,off+x*28+26,10+y*28+26)
     d.rectangle(box,fill=(204,161,78) if changed else (GRAY if c=='1' else (32,47,62)),outline=(80,98,113))
  changes.append(tiny)
  n=sum(a!=b for a,b in zip(''.join(v['A']),''.join(v['B'])))
  labels.append(f'{k} / A  vs  B / {n} cells move')
annotated_sheet(changes,labels,1,cell=(650,350),footer='SOURCE-CHANGED PIXELS IN AMBER are only an annotation, NOT sprite pixels').save(ROOT/'07_GAIT_BITS_BOTH_POSES.png')

# No artistical claims: one technical map with overlay coordinates, including mouth issue.
feat=Image.new('RGB',(1050,640),DARK);d=ImageDraw.Draw(feat)
for i,k in enumerate(('I1 HEAD','I2 LIMBS')):
 v=DATA[i+1];ox=65+i*505;oy=80;cell=33
 d.text((ox,28),k,font=font22,fill=INK)
 for y,row in enumerate(v['A']):
  for x,b in enumerate(row):
   d.rectangle((ox+x*cell,oy+y*cell,ox+(x+1)*cell-2,oy+(y+1)*cell-2),fill=GRAY if b=='1' else (32,48,61),outline=LINE)
  d.text((ox+275,oy+y*cell+8),f'{y:02d}   {row}',font=font14,fill=MUTE)
 # colors mark geometry NOT new sprite colors
 for x,y in ([(5,4),(5,7)] if i==0 else [(6,5),(6,7)]):
  d.rectangle((ox+x*cell,oy+y*cell,ox+(x+1)*cell-2,oy+(y+1)*cell-2),outline=(92,214,224),width=3)
 if i==0:
  for x,y in [(7,5),(7,6)]:d.rectangle((ox+x*cell,oy+y*cell,ox+(x+1)*cell-2,oy+(y+1)*cell-2),outline=(255,198,113),width=3)
 d.text((ox,510),'Cyan: intended eye holes',font=font14,fill=(92,214,224))
 d.text((ox,537),'Amber: intended mouth notch' if i==0 else 'Mouth: NOT represented',font=font14,fill=(255,198,113))
d.text((50,610),'ANATOMICAL COORDINATE ANNOTATION ONLY; NO COLOR IN SOURCE ART; NOT STELLA; recognition not proven.',font=font14,fill=MUTE)
feat.save(ROOT/'08_ANATOMY_HYPOTHESIS_NOT_VISUAL_PROOF.png')

# All GIF loops deliberately equal cadence and identical source scale/flat background
for k,v,fn in zip(NAMES,DATA,('09_GIF_P1_A_FROZEN.gif','10_GIF_I1_HEAD.gif','11_GIF_I2_LIMBS.gif')):
 frames=[frame(v[p],FOREST,1,False) for p in ('A','B')]
 frames[0].save(ROOT/fn,save_all=True,append_images=frames[1:],duration=[133,133],loop=0,optimize=False,disposal=2)
print('images created: '+', '.join(p.name for p in ROOT.glob('*.png')))
