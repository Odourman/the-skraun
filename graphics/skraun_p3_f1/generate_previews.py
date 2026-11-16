#!/usr/bin/env python3
"""Purely illustrative, deterministic pixel art: never loads the owner's private drawing or runs Stella."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,random
R=Path(__file__).resolve().parent
s=json.loads((R/'P3_F1_SOURCE_BITMAPS.json').read_text(encoding='utf-8'))
items=[('U1',s['frozen_control']['U1_frozen']),('D1',s['new_candidates']['D1_face_ear_permanent']),('D2',s['new_candidates']['D2_shoulder_arm_permanent'])]
G=tuple(s['preview']['color_gray_rgb']); BLACK=tuple(s['preview']['off_rgb']); FOREST=tuple(s['preview']['forest_bg_rgb']); NIGHT=tuple(s['preview']['night_bg_rgb']); FG=(238,241,245);DIM=(155,175,189);PANEL=(27,39,52);BORDER=(63,88,109);GOLD=(224,178,111)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(pt,b=False):return ImageFont.truetype(B if b else F,pt)
def say(im,xy,v,size=15,fill=FG,b=False):ImageDraw.Draw(im).text(xy,v,font=font(size,b),fill=fill)
def mask(rows,xrep=1,yrep=1,fg=G,bg=BLACK):
 im=Image.new('RGB',(len(rows[0])*xrep,len(rows)*yrep),bg);d=ImageDraw.Draw(im)
 for y,row in enumerate(rows):
  for x,c in enumerate(row):
   if c=='1':d.rectangle((x*xrep,y*yrep,(x+1)*xrep-1,(y+1)*yrep-1),fill=fg)
 return im
def get(v,pose,facing):return v[pose] if facing=='RIGHT' else v[pose+'_left']
def native(rows,level=1,bg=FOREST):
 q=s['conceptual_levels'][str(level)];glyph=mask(rows,q['x_repeat'],q['y_repeat'],G,bg);im=Image.new('RGB',(160,192),bg);im.paste(glyph,((160-glyph.width)//2,(192-glyph.height)//2));return im
def tv(rows,level=1,bg=FOREST):return native(rows,level,bg).resize((640,480),Image.Resampling.NEAREST)
def crop(rows,level=1,bg=FOREST):return tv(rows,level,bg).crop((200,158,440,322)) # no zoom: 240 x 164

def sheet(cards,columns,cell_size,title,footer,card_header=48,head=80):
 cw,ch=cell_size;gap=16;rows=(len(cards)+columns-1)//columns
 im=Image.new('RGB',(gap+columns*(cw+gap),head+rows*(ch+card_header+gap)+48),BLACK);draw=ImageDraw.Draw(im)
 title_size=23
 while ImageDraw.Draw(im).textbbox((0,0),title,font=font(title_size,True))[2]>im.width-gap*2 and title_size>14:title_size-=1
 say(im,(gap,18),title,title_size,b=True)
 for i,(source,name,sub) in enumerate(cards):
  c=i%columns;row=i//columns;x=gap+c*(cw+gap);y=head+row*(ch+card_header+gap)
  assert source.size==(cw,ch),(source.size,(cw,ch),name)
  draw.rectangle((x-1,y-1,x+cw+1,y+card_header+ch+1),fill=PANEL,outline=BORDER,width=1)
  say(im,(x+8,y+5),name,15,b=True)
  say(im,(x+8,y+27),sub,11,fill=DIM)
  im.paste(source,(x,y+card_header))
 say(im,(gap,im.height-34),footer,12,fill=DIM)
 return im

# 12 authentic 8x12 source glyphs, raw tiny; named by candidate, pose, and facing
for name,v in items:
 for pose in 'AB':
  for facing in ('RIGHT','LEFT'):
   mask(get(v,pose,facing)).save(R/f'NATIVE_8x12_{name}_{pose}_{facing}.png')

# BLIND FIRST (randomized samples, no face/pose/family labels on page), original TV-size crop only
blind=[(name,pose,facing,v) for name,v in items for pose in 'AB' for facing in ('RIGHT','LEFT')]
random.Random(s['preview']['blind_seed']).shuffle(blind)
bl=[];answers=[]
for i,(name,pose,facing,v) in enumerate(blind,1):
 bl.append((crop(get(v,pose,facing)),f'PROV {i:02d}','240x164 TV-utsnitt / ingen extra zoom'))
 answers.append(f'| {i:02d} | {name} | {pose} | {facing} |')
sheet(bl,3,(240,164),'00  |  BLIND L1: KAN DU SE VILKET HALL FIGUREN AR VAND?',
      'Alla 12 ar designbilder i samma storlek. Svar i 01_BLIND_ANSWER_KEY.md. INTE STELLA.',head=90).save(R/'00_BLIND_L1_UNLABELED.png')
(R/'01_BLIND_ANSWER_KEY.md').write_text('# P3-F1: BLIND SVARSNYCKEL\n\nVisas separat fran den omarkta forhandsgranskningen. Inga verkliga testpersoner har utvarderat bilden.\n\n| Prov | Familj | Gangpose | Riktning |\n|---:|---|:---:|---|\n'+'\n'.join(answers)+'\n\nSvarskontroll ger inte perceptuell PASS utan anvandarens egen bedomning.\n',encoding='utf-8')

# Labeled exact-scale crop for comparison
cards=[(crop(get(v,pose,facing)),f'{name} / {pose} / {"HOGER" if facing=="RIGHT" else "VANSTER"}','Ozoomat, samma TV-skala') for name,v in items for pose in 'AB' for facing in ('RIGHT','LEFT')]
sheet(cards,4,(240,164),'02  |  NIVÅ 1: SAMMA 12 BILDER MED FACIT','Granskning, inga extra pixlar. DESIGN, INTE STELLA.',head=84).save(R/'02_L1_LABELED_SAME_SCALE.png')
# Unscaled native screen (the glyph remains 8x12)
raw=[(native(get(v,p,f)),f'{n} {p}-{f[0]}','Riktig 160x192-rasterarea') for n,v in items for p in 'AB' for f in ('RIGHT','LEFT')]
sheet(raw,4,(160,192),'03  |  NIVÅ 1: OFÖRSTORADE 160x192 BILDRUTOR','Glyfen ar enbart 8x12 color clocks/scanlines. DESIGN, INTE STELLA.',head=78).save(R/'03_L1_NATIVE_160x192.png')
# Full TV screen 4:3 one pose each candidate (full image included)
full=[(tv(v['A']),f'{n} / A / HOGER','640x480, hel spelplan, NN') for n,v in items]
sheet(full,3,(640,480),'04  |  HEL SPELSKARM 4:3, NIVA 1','Samma 8x12 kallar. 160x192 --> 640x480 nearest-neighbor. INTE STELLA.',head=82).save(R/'04_L1_FULL_4_3_SCREEN.png')
# Binary source grids with exact row bits ALL 12 states
boards=[]
for n,v in items:
 for p in 'AB':
  for facing in ('RIGHT','LEFT'):
   rows=get(v,p,facing);panel=Image.new('RGB',(350,354),PANEL);d=ImageDraw.Draw(panel)
   for y,r in enumerate(rows):
    for x,b in enumerate(r):
     left=13+x*25;top=12+y*27
     d.rectangle((left,top,left+23,top+25),fill=G if b=='1' else BLACK,outline=BORDER)
    say(panel,(228,top+5),r,12,fill=DIM)
   boards.append((panel,f'{n} / {p} / {facing}','FORSTORAT for bitkontroll'))
sheet(boards,4,(350,354),'05  |  EXAKTA 8x12 PIXELMATRISER + R/L','ENDAS FORSTORAT FOR GRANSKNING. Bitmap bit7 till vanster. INTE STELLA.',head=85).save(R/'05_EXACT_8x12_GRIDS_ALL_STATES.png')
# Black white silhouette without color cues
bw=[]
for n,v in items:
 for p in 'AB':
  for facing in ('RIGHT','LEFT'):
   rr=get(v,p,facing)
   bw.append((mask(rr,25,25,(8,8,8),(255,255,255)),f'{n} {p} {facing}','25x for audit, INTE spelstorlek'))
sheet(bw,4,(200,300),'06  |  SVARTVITA KALLSILHUETTER','Enbart omvand grafik. Originalstorlek skall bedomas i 00/03/04. DESIGN.',head=80).save(R/'06_BLACK_WHITE_SILHOUETTES_ZOOMED.png')
# All three design-level sizes for each family in same TV scale
lv=[]
for lev in (1,2,3):
 for n,v in items:
  inf=s['conceptual_levels'][str(lev)];lv.append((crop(v['A'],lev,NIGHT),f'{n} / L{lev}',f'{inf["width_color_clocks"]} cc x {inf["scanline_height"]} linjer'))
sheet(lv,3,(240,164),'07  |  TRE HISTORISKA STORLEKAR, SAMMA KALLBITAR','L2/L3 ENDAST SKALNINGSILLUSTRATION. ART1 L3-fel #19 EJ ATGARDAT. INTE STELLA.',head=80).save(R/'07_L1_L2_L3_CONCEPTUAL.png')
# Pose changes overlay source difference (not sprite colors)
walk=[]
for n,v in items:
 im=Image.new('RGB',(584,342),PANEL);dr=ImageDraw.Draw(im)
 for j,p in enumerate('AB'):
  for y,row in enumerate(v[p]):
   for x,b in enumerate(row):
    diff=v['A'][y][x]!=v['B'][y][x];x0=11+j*291+x*27;y0=9+y*27
    dr.rectangle((x0,y0,x0+25,y0+25),fill=GOLD if diff else (G if b=='1' else BLACK),outline=BORDER)
  say(im,(239+j*291,40),'POSE '+p,15)
 walk.append((im,n,f'{v["A_B_changes"]} olika kallspriteceller'))
sheet(walk,1,(584,342),'08  |  A/B-POSER, BITAR SOM BYTER TILLSTAND','Guld = annotation, INTE en ny spritefarg. Face/shoulder stable across gait.',head=80).save(R/'08_GAIT_HIGHLIGHTS_SOURCE_ONLY.png')
# Stability + direction head/shoulder audit, large grid but explicitly design
stable=[]
for n,v in items:
 top=Image.new('RGB',(600,333),PANEL);dr=ImageDraw.Draw(top)
 for j,f in enumerate(('RIGHT','LEFT')):
  rows=get(v,'A',f)
  for y,row in enumerate(rows):
   for x,b in enumerate(row):
    x0=17+j*292+x*25;y0=14+y*25
    changed=get(v,'B',f)[y][x]!=b
    border=GOLD if changed else BORDER
    dr.rectangle((x0,y0,x0+23,y0+23),fill=(G if b=='1' else BLACK),outline=border,width=1)
  say(top,(216+j*292,34),f[:1],16)
 stable.append((top,n,'Guld ram visar enbart gangposeandring'))
sheet(stable,1,(600,333),'09  |  FASTE FACINGSIGNALER VS RORLIGA CELLER','Riktningssignal bedoms bara nar de rorliga bitarna INTE forklarar skillnaden. DESIGN.',head=82).save(R/'09_STABLE_FACING_CUES.png')
# forest/night contrast no PF claims
background=[]
for bg,world in [(FOREST,'SKOG'),(NIGHT,'NATT')]:
 for n,v in items:
  background.append((crop(v['A'],1,bg),f'{n} / {world}','Enfargad bakgrund, ingen PF'))
sheet(background,3,(240,164),'10  |  L1 KONTRAST, TVA ENFARGADE BAKGRUNDER','Inga arkitekturantaganden om TIA PF eller halo. DESIGN, INTE STELLA.',head=82).save(R/'10_FOREST_NIGHT_FLAT_CONTEXT.png')
# all 6 two-frame animations fixed location, no movement added
for n,v in items:
 for facing in ('RIGHT','LEFT'):
  ff=[crop(get(v,p,facing)) for p in 'AB']
  ff[0].save(R/f'GIF_{n}_{facing}_A_B.gif',save_all=True,append_images=ff[1:],duration=[140,140],loop=0,disposal=2,optimize=False)
print('Created exact source previews',len(list(R.glob('*.png'))),'PNGs,',len(list(R.glob('*.gif'))),'GIFs')
