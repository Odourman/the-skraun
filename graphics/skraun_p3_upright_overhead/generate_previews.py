#!/usr/bin/env python3
"""Reproduce P3 exact pixel-based artwork. NO Stella, emulator, ROM, or code generation.
All enlargement is nearest-neighbor. Native 8x12 glyphs and 160x192 arena are supplied.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
ROOT=Path(__file__).resolve().parent
S=json.loads((ROOT/'P3_SOURCE_BITMAPS.json').read_text(encoding='utf-8'))
D=[('Q1_UPRIGHT_REFERENCE',S['controls']['Q1_prior_best_upright']),('P1_A_PRONE_NEGATIVE',S['controls']['P1_A_negative_prone']),('U1_FACE',S['new_candidates']['U1_upright_face_priority']),('U2_BODY',S['new_candidates']['U2_upright_body_priority'])]
GRAY=tuple(S['preview']['color_gray_RGB']);FOREST=tuple(S['preview']['contrast_forest_RGB']);NIGHT=tuple(S['preview']['contrast_night_RGB']);INK=(237,243,248);MUTED=(157,177,194);DARK=(17,25,35);PANEL=(27,40,54);BORDER=(73,94,113);YELLOW=(239,192,91)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def writing(im,x,y,t,size=16,color=INK,bold=False):ImageDraw.Draw(im).text((x,y),t,font=font(size,bold),fill=color)
def mask(rows,color=GRAY,bg=DARK,xrep=1,yrep=1):
 im=Image.new('RGB',(8*xrep,12*yrep),bg);d=ImageDraw.Draw(im)
 for y,r in enumerate(rows):
  for x,c in enumerate(r):
   if c=='1':d.rectangle((x*xrep,y*yrep,(x+1)*xrep-1,(y+1)*yrep-1),fill=color)
 return im
def arena(rows,level=1,bg=FOREST,tv=False):
 info=S['conceptual_sizes'][str(level)];g=mask(rows,GRAY,bg,info['x_width_multiplier'],info['row_repeat'])
 im=Image.new('RGB',(160,192),bg);im.paste(g,((160-g.width)//2,(192-g.height)//2))
 return im.resize((640,480),Image.Resampling.NEAREST) if tv else im
def crop_tv(rows,level=1,bg=FOREST,w=240,h=164):
 fr=arena(rows,level,bg,True);return fr.crop((320-w//2,240-h//2,320+w//2,240+h//2))
def panel_sheet(items,cols,cell_w,cell_h,heading,footer='DESIGN PREVIEW - NOT STELLA',header=75):
 gap=18;rows=(len(items)+cols-1)//cols;out=Image.new('RGB',(cols*(cell_w+gap)+gap,rows*(cell_h+58+gap)+header+40),DARK);d=ImageDraw.Draw(out)
 writing(out,20,14,heading,24,INK,True)
 for i,(im,title,sub) in enumerate(items):
  x=gap+(i%cols)*(cell_w+gap);y=header+(i//cols)*(cell_h+58+gap)
  d.rectangle((x,y,x+cell_w+1,y+cell_h+57),fill=PANEL,outline=BORDER,width=1)
  writing(out,x+8,y+5,title,15,INK,True)
  writing(out,x+8,y+28,sub,11,MUTED)
  if im.size!=(cell_w,cell_h):raise AssertionError((title,im.size,(cell_w,cell_h)))
  out.paste(im,(x,y+56))
 writing(out,20,out.height-30,footer,13,MUTED)
 return out
# Single-source raw 8x12 RGB pixel files; both poses and horizontal directions for new 2 + control 2
for k,v in D:
 for pose in 'AB':
  for side in ('RIGHT','LEFT'):
   rows=v[pose] if side=='RIGHT' else v[pose+'_left']
   mask(rows).save(ROOT/f'NATIVE_8x12_{k}_{pose}_{side}.png')
# Level 1 native, true 160x192 color clocks, no scaling inside the panels
raw=[]
for pose in 'AB':
 for k,v in D:raw.append((arena(v[pose]),k+'  '+pose,'160x192 arena; 8x12 glyph'))
panel_sheet(raw,4,160,192,'01 | NIVA 1: OBEHANDLADE 160x192-KLOCKPIXELSKARMAR',footer='1 bitmapcell = 1 color clock och 1 scanline vid L1. INGEN forstoring. DESIGN, INTE STELLA.',header=78).save(ROOT/'01_L1_NATIVE_160x192.png')
# Full 4:3 TV 640x480 each, identical output geometric assumptions
full=[]
for pose in 'AB':
 for k,v in D:full.append((arena(v[pose],tv=True),k+' / '+pose,'8x12 original, 640x480 NN'))
panel_sheet(full,4,640,480,'02 | NIVA 1: FULLSKARM 4:3 NTSC-APPROXIMATION',footer='640x480 nearest-neighbor fran 160x192. Glyphen ar fortfarande bara 8x12. DESIGN, INTE STELLA.',header=76).save(ROOT/'02_L1_TV_4x3_FULL_A_B.png')
# honest surrounding crops: 4:3 resampled BEFORE crop, no zoom further
small=[]
for k,v in D:small.append((crop_tv(v['A']),k,'240x164 crop at unchanged 640x480 scale'))
panel_sheet(small,4,240,164,'03 | NIVA 1: CENTRALA BESKARNINGAR (INGEN EXTRA ZOOM)',footer='Beskarning av 640x480 bild. Skraun ar lika liten som i 02. DESIGN, INTE STELLA.',header=78).save(ROOT/'03_L1_UNZOOMED_CONTEXT_CROPS.png')
# source silhouette, big for auditing only
bw=[]
for pose in 'AB':
 for k,v in D:
  m=mask(v[pose],(10,10,10),(255,255,255),24,24)
  bw.append((m,k+' '+pose,'PIXELMATRIS FORSTORAD 24x, ej spelstorlek'))
panel_sheet(bw,4,192,288,'04 | SVARTVITA KALLSILHUETTER - FORSTORAT FOR GRANSKNING',footer='Samma 8x12 bitar; ingen ny detalj tillagd. DESIGN, INTE STELLA.',header=80).save(ROOT/'04_BLACK_WHITE_SILHOUETTES_ENLARGED.png')
# matrix board includes exact 12 binary rows, 4 groups x4 poses/sides -> 16 cards
cards=[]
for k,v in D:
 for pose in 'AB':
  for side in ('RIGHT','LEFT'):
   rs=v[pose] if side=='RIGHT' else v[pose+'_left'];board=Image.new('RGB',(355,353),PANEL);d=ImageDraw.Draw(board)
   for y,r in enumerate(rs):
    for x,b in enumerate(r):
     x0=16+x*25;y0=10+y*27
     d.rectangle((x0,y0,x0+23,y0+25),fill=GRAY if b=='1' else DARK,outline=(76,91,106))
    d.text((225,12+y*27),r,font=font(13),fill=MUTED)
   cards.append((board,k+' '+pose+' '+side,'right/left only; top-first row bits'))
panel_sheet(cards,4,355,353,'05 | EXAKTA 8x12 BITMAPPAR - T.HELA 2 POSER / 2 VANDNINGAR',footer='bit7 = bildens vansterkant. Left = exakt omvand bitordning per rad, inte vertikal flip. DESIGN.',header=78).save(ROOT/'05_EXACT_8x12_ROWS_ALL_DIRECTIONS.png')
# level 1/2/3 screen result with same source sprite, focus candidates (L1 primary), use crop 240x164
levels=[]
for lvl in (1,2,3):
 for k,v in D[2:]:levels.append((crop_tv(v['A'],lvl,NIGHT),k+' | L'+str(lvl),str(S['conceptual_sizes'][str(lvl)]['width_color_clocks'])+' cc x '+str(S['conceptual_sizes'][str(lvl)]['height_scanlines'])+' scanlines'))
panel_sheet(levels,3,240,164,'06 | TRE STORLEKAR - SAMMA 8x12 KALLBITAR',footer='L2/L3 ar ENDAST konceptuell skalning. Verkligt ART1-L3-fel #19 ej atgardat. INTE STELLA.',header=78).save(ROOT/'06_ALL_THREE_LEVELS_CONCEPTUAL.png')
# flat forest & night, source-level L1 full (cropped at current scale, no zoom)
contr=[]
for back,name in ((FOREST,'SKOG FLAT'),(NIGHT,'NATT FLAT')):
 for k,v in D:contr.append((crop_tv(v['A'],1,back),k,name+' - flat color only'))
panel_sheet(contr,4,240,164,'07 | SKOG / NATT - PLATTA BAKGRUNDER NIVA 1',footer='Ingen PF, halo eller sprite scheduler anvands; endast kontrastmockup. INTE STELLA.',header=78).save(ROOT/'07_L1_FOREST_NIGHT_FLAT.png')
# overlays changed A/B with warm diff border colors as technical annotation, not source
motion=[]
for k,v in D:
 im=Image.new('RGB',(560,315),PANEL);d=ImageDraw.Draw(im)
 for i,pose in enumerate('AB'):
  r=v[pose];ox=20+i*270;oy=9;size=23
  for y,row in enumerate(r):
   for x,b in enumerate(row):
    q=(r[y][x]!=v['B' if pose=='A' else 'A'][y][x]);col=YELLOW if q else (GRAY if b=='1' else DARK)
    d.rectangle((ox+x*size,oy+y*size,ox+(x+1)*size-2,oy+(y+1)*size-2),fill=col,outline=(75,90,106))
  writing(im,ox+202,oy+35,'POSE '+pose,14)
 motion.append((im,k+' A / B',str(v['A_B_different_cells'])+' bitceller skiljer; gul = annotering'))
panel_sheet(motion,2,560,315,'08 | TVASTEGSRORELSE, SKILLNADER I KALLPIXEL',footer='Gula celler ar markerade i analytisk bild, inte en extra spritefarg. INTE STELLA.',header=78).save(ROOT/'08_AB_GAIT_BIT_DIFFERENCES.png')
# explicit right/wrong visual principle labels; source is identical, no painterly stand-in
rw=[]
for k,v,truth in [('U1_FACE',D[2][1],'RATT KROPPSAXEL / KANDIDAT'),('U2_BODY',D[3][1],'RATT KROPPSAXEL / KANDIDAT'),('P1_A_PRONE_NEGATIVE',D[1][1],'FEL: LIGGANDE / NEGATIV KONTROLL')]:
 card=Image.new('RGB',(520,380),DARK);d=ImageDraw.Draw(card);rows=v['A'];s=23
 for y,r in enumerate(rows):
  for x,b in enumerate(r):d.rectangle((160+x*s,40+y*s,160+(x+1)*s-2,40+(y+1)*s-2),fill=GRAY if b=='1' else PANEL)
 writing(card,25,330,truth,16,INK,True)
 rw.append((card,k,'uppifran, staende tolkat vs liggande feltolkning'))
panel_sheet(rw,3,520,380,'09 | KORREKT VISUELL GRUNDPRINCIP VS GAMMAL FELTOLKNING',footer='U1/U2 ar designforsok, EJ finala. P1 liggande ar dokumenterad negativ kontroll. INTE STELLA.',header=78).save(ROOT/'09_UPRIGHT_VS_PRONE_DIRECTION.png')
# up and down movement uses EXACT identical right and left assets, arrows overlay outside glyph; no new sprites
up=[]
for k,v in D[2:]:
 for face in ('RIGHT','LEFT'):
  rows=v['A'] if face=='RIGHT' else v['A_left']
  for motion_direction in ('UP', 'DOWN'):
   card=crop_tv(rows)
   sheet=Image.new('RGB',(240,164),FOREST);sheet.paste(card)
   ImageDraw.Draw(sheet).text((11,5),'MOVE '+motion_direction,font=font(14,True),fill=YELLOW)
   up.append((sheet,k+' / '+face,motion_direction+': exakt samma facing bitmap'))
panel_sheet(up,4,240,164,'10 | VERTIKAL SPELARRORELSE ANVANDER SAMMA UPPRATTA SIDOGRAFIK',footer='Gula rorelseetiketter ar ENDAST presentation; inga upp/ned-sprites eller ny gameplay. INTE STELLA.',header=78).save(ROOT/'10_UP_DOWN_REUSES_SAME_TWO_FACINGS.png')
# MAIN decision with honest native context and enlarged audit, both in one panel
summ=[]
for k,v in D:
 out=Image.new('RGB',(360,410),PANEL);d=ImageDraw.Draw(out)
 nn=crop_tv(v['A'],w=240,h=164);out.paste(nn,(60,16));writing(out,12,182,'OZOOMAD: 240x164 fran 4:3 TV',12,MUTED)
 m=mask(v['A'],GRAY,DARK,14,14);out.paste(m,(124,208));writing(out,12,389,'FORSTORAD bitmap for granskning',12,MUTED)
 summ.append((out,k,'RATT? source only, not approved'))
panel_sheet(summ,4,360,410,'00 | MAIN II - P3 UPPRATT TROLL OVANIFRAN: BESLUTSBLAD',footer='L1 neutral 4:3 crop OVERST; forstorad 8x12 bitmatris UNDERST. P1 A = liggande FELTOLKNING. DESIGN, INTE STELLA.',header=78).save(ROOT/'00_MAIN_II_P3_DECISION_SHEET.png')
# animations; ALL exact same fixed speed, 2 frames per gif, both facings U1/U2; historical controls for comparison
for k,v in D:
 for side in (('RIGHT','LEFT') if k.startswith(('U1','U2')) else ('RIGHT',)):
  frames=[arena(v[p] if side=='RIGHT' else v[p+'_left'],1,FOREST,True) for p in 'AB']
  frames[0].save(ROOT/f'GIF_{k}_{side}_A_B.gif',save_all=True,append_images=frames[1:],duration=[140,140],loop=0,disposal=2,optimize=False)
print('P3 previews generated: '+str(sum(1 for p in ROOT.iterdir() if p.suffix.lower() in ('.png','.gif'))))
