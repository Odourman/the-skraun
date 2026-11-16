#!/usr/bin/env python3
"""Recreate deterministic GRAPHICS P3-F1 design-only pixel previews. Never uses Stella or private source photo."""
from pathlib import Path
import json, random
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent
S=json.loads((R/'SOURCE_8x12.json').read_text(encoding='utf-8'))
P=S['pixels']
ART=[('U1',S['baseline']['U1_frozen']),('D1',S['new_candidates']['D1_head_expression']),('D2',S['new_candidates']['D2_swaying_arms'])]
GRAY=tuple(P['gray']);FOREST=tuple(P['background']);NIGHT=tuple(P['night']);OFF=tuple(P['off'])
INK=(240,245,249);MUTED=(168,190,201);BOARD=(25,38,50);BORDER=(77,95,111);GOLD=(227,181,86)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def write(im,pos,txt,pt=14,col=INK,bold=False):ImageDraw.Draw(im).text(pos,txt,font=font(pt,bold),fill=col)
def rows(v,p,f):return v[p] if f=='RIGHT' else v[p+'_left']
def glyph(data,xr=1,yr=1,fg=GRAY,bg=OFF):
 im=Image.new('RGB',(8*xr,12*yr),bg);dr=ImageDraw.Draw(im)
 for y,line in enumerate(data):
  for x,bit in enumerate(line):
   if bit=='1':dr.rectangle((x*xr,y*yr,(x+1)*xr-1,(y+1)*yr-1),fill=fg)
 return im
def arena(data,level=1,bg=FOREST):
 q=str(level);im=Image.new('RGB',(160,192),bg)
 sprite=glyph(data,P['level_x_repeat'][q],P['level_y_repeat'][q],GRAY,bg)
 im.paste(sprite,((160-sprite.width)//2,(192-sprite.height)//2))
 return im
def screen(data,level=1,bg=FOREST):return arena(data,level,bg).resize((640,480),Image.Resampling.NEAREST)
def crop(data,level=1,bg=FOREST):return screen(data,level,bg).crop((200,158,440,322))
def sheet(title,items,cols,cell,footer='DESIGNFÖRHANDSVISNING / INTE STELLA',head=84):
 cw,ch=cell;gap=16;cardhead=45;rowsnum=(len(items)+cols-1)//cols
 w=gap+cols*(cw+gap);h=head+rowsnum*(ch+cardhead+gap)+50
 im=Image.new('RGB',(w,h),OFF);dr=ImageDraw.Draw(im)
 pts=21
 while dr.textbbox((0,0),title,font=font(pts,True))[2]>w-30 and pts>10:pts-=1
 write(im,(16,16),title,pts,bold=True)
 for i,(pic,name,detail) in enumerate(items):
  assert pic.size==(cw,ch),(name,pic.size,(cw,ch))
  x=gap+(i%cols)*(cw+gap);y=head+(i//cols)*(ch+cardhead+gap)
  dr.rectangle((x-1,y-1,x+cw,y+cardhead+ch),fill=BOARD,outline=BORDER)
  write(im,(x+6,y+4),name,15,bold=True)
  write(im,(x+6,y+26),detail,10,col=MUTED)
  im.paste(pic,(x,y+cardhead))
 write(im,(16,h-33),footer,12,col=MUTED)
 return im
# Native 8x12 true pixels, no enlargement
for n,v in ART:
 for p in 'AB':
  for f in ('RIGHT','LEFT'):glyph(rows(v,p,f)).save(R/f'NATIVE_8x12_{n}_{p}_{f}.png')
# Blind images: numeric sample labels only, 12 source states, not fabricated user test
cases=[(n,v,p,f) for n,v in ART for p in 'AB' for f in ('RIGHT','LEFT')]
random.Random(P['blind_seed']).shuffle(cases)
blind=[];answers=[]
for i,(n,v,p,f) in enumerate(cases,1):
 blind.append((crop(rows(v,p,f)),f'PROV {i:02}','Samma verkliga nivå-1-TV-skala'))
 answers.append(f'| {i:02} | {n} | {p} | {f} |')
sheet('00 | OMARKT NIVA-1-TEST: VILKEN RIKTNING SER DU?',blind,3,(240,164),
      'Alla är samma bildskala. INGEN studie med riktiga betraktare har utförts. DESIGN, INTE STELLA.').save(R/'00_BLIND_L1_UNLABELED.png')
(R/'01_BLIND_ANSWER_KEY.md').write_text('# P3-F1 efter forskningsrelease: BLIND FACIT\n\nBilden är en objektiv, slumpad presentationsordning, **inte ett utfört mänskligt perceptuellt test**.\n\n| Prov | Familj | Pose | Visuell riktning |\n|---:|---|:---:|---|\n'+'\n'.join(answers)+'\n',encoding='utf-8')
# Labeled common-scale 12 states
labeled=[(crop(rows(v,p,f)),f'{n} / {p} / {f}','240x164 ozoomad 4:3-crop') for n,v in ART for p in 'AB' for f in ('RIGHT','LEFT')]
sheet('02 | JÄMFÖRELSE: FRYST U1, D1, D2 VID NIVA 1',labeled,4,(240,164)).save(R/'02_L1_LABELED_IDENTICAL_SCALE.png')
native=[(arena(rows(v,p,f)),f'{n}/{p}/{f}','160x192 originalraster') for n,v in ART for p in 'AB' for f in ('RIGHT','LEFT')]
sheet('03 | OFÖRSTORADE 160x192-RASTERBILDER',native,4,(160,192),
     'Varje spelarsprite = exakt 8x12 ursprungliga celler. DESIGN, INTE STELLA.').save(R/'03_L1_NATIVE_160x192.png')
full=[(screen(v['A']),n+' / A / RIGHT','640x480 NN: hel 4:3 skärm') for n,v in ART]
sheet('04 | NIVÅ-1 HELSKÄRM, TV 4:3',full,3,(640,480)).save(R/'04_L1_FULL_4_3_TV.png')
# Exact grids include all 12 source states with binary text labels
mat=[]
for n,v in ART:
 for p in 'AB':
  for f in ('RIGHT','LEFT'):
   q=rows(v,p,f);im=Image.new('RGB',(338,345),BOARD);dr=ImageDraw.Draw(im)
   for y,line in enumerate(q):
    for x,bit in enumerate(line):
     x0=12+x*23;y0=12+y*27
     dr.rectangle((x0,y0,x0+21,y0+25),fill=GRAY if bit=='1' else OFF,outline=BORDER)
    write(im,(206,16+y*27),line,11,col=MUTED)
   mat.append((im,f'{n} {p} {f}','FÖRSTORAD bitmatris - inte L1-visning'))
sheet('05 | BITMAP DATA 8x12: ALLA POSER OCH RIKTNINGAR',mat,4,(338,345)).save(R/'05_EXACT_SOURCE_MATRICES.png')
bw=[(glyph(rows(v,p,f),22,22,(8,8,8),(255,255,255)),f'{n} {p} {f}','FÖRSTORAT x22 - ENDAST silhuett') for n,v in ART for p in 'AB' for f in ('RIGHT','LEFT')]
sheet('06 | SVARTVITT - FÖRSTORADE 8x12-SILHUETTER',bw,4,(176,264)).save(R/'06_BLACK_WHITE_SILHOUETTES.png')
levels=[(crop(v['A'],level=level,bg=NIGHT),f'{n} / NIVÅ {level}',str(P['level_dimensions'][str(level)])+' rasterceller') for level in (1,2,3) for n,v in ART]
sheet('07 | NIVÅ 1, 2 OCH 3 - KONCEPTUELL FÖRSTORING',levels,3,(240,164),
      'Skalbilder, inte Stella. P01-ART1 L3 rasterfel #19 EJ reparerat.').save(R/'07_LEVELS_1_2_3_CONCEPTUAL.png')
# A/B annotated changes, no sprite color change
items=[]
for n,v in ART:
 panel=Image.new('RGB',(540,335),BOARD);dr=ImageDraw.Draw(panel)
 for k,p in enumerate('AB'):
  for y,line in enumerate(v[p]):
   for x,bit in enumerate(line):
    x0=12+k*268+x*25;y0=10+y*26
    changed=v['A'][y][x]!=v['B'][y][x]
    dr.rectangle((x0,y0,x0+23,y0+24),fill=GOLD if changed else (GRAY if bit=='1' else OFF),outline=BORDER)
  write(panel,(230+k*268,40),'POSE '+p,13)
 items.append((panel,n,'Guld = ÄNDRAD pixel, inte figurens kulör'))
sheet('08 | ARMRÖRELSE OCH STEG: BITAR SOM ÄNDRAS',items,1,(540,335)).save(R/'08_GAIT_SOURCE_DIFFS.png')
# fixed facing cue stable across gait region comparison
cue=[]
for n,v in ART:
 card=Image.new('RGB',(552,335),BOARD);dr=ImageDraw.Draw(card)
 for k,f in enumerate(('RIGHT','LEFT')):
  for y,line in enumerate(rows(v,'A',f)):
   for x,bit in enumerate(line):
    x0=12+k*265+x*25;y0=10+y*26
    stable=bit==rows(v,'B',f)[y][x]
    dr.rectangle((x0,y0,x0+23,y0+24),fill=GRAY if bit=='1' else OFF,outline=BORDER if stable else GOLD,width=1)
  write(card,(222+k*265,34),f,13)
 cue.append((card,n,'Guld kontur = gångposeändring, inte permanent cue'))
sheet('09 | PERMANENT VÄNDNING VS GÅNGPOSE',cue,1,(552,335)).save(R/'09_STABLE_FACING_SOURCE.png')
contrast=[(crop(v['A'],bg=back),f'{n} / {world}','Platt bakgrund, ingen PF-kernel') for world,back in [('SKOG',FOREST),('NATT',NIGHT)] for n,v in ART]
sheet('10 | KONTRAST I NIVÅ 1, DESIGNBAKGRUNDER',contrast,3,(240,164)).save(R/'10_L1_FOREST_NIGHT_FLAT.png')
for n,v in ART:
 for f in ('RIGHT','LEFT'):
  frames=[crop(rows(v,p,f)) for p in 'AB']
  frames[0].save(R/f'GIF_{n}_{f}_A_B.gif',save_all=True,append_images=frames[1:],duration=[140,140],loop=0,disposal=2,optimize=False)
print('Generated',len(list(R.glob('*.png'))),'PNGs,',len(list(R.glob('GIF_*.gif'))),'GIFs')
