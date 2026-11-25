#!/usr/bin/env python3
"""Rebuild all R2 graphics from the existing frozen source snippets and approved image.
Requires Pillow only. No network, GitHub writes, Stella, or ROM implementation.
"""
from pathlib import Path
import shutil,json,hashlib,re,math,collections,io,sys,zipfile
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'09_GENERATOR'
SRC=ROOT
REF=ROOT/'11_APPROVED_VISUAL_REFERENCE'
motifs={
'01_fir_A':[
'00011000','00011000','00111100','00111100','00111100','01111110','01111110','01111110','11111111','11111111','00011000','00011000','00011000','00011000'],
'01_round_A':[
'00111100','01111110','01111110','11111111','11111111','11111111','11111111','11111111','01111110','01111110','00111100','00011000','00011000','00011000','00011000'],
'02_fir_B':[
'00010000','00010000','00111000','00111000','01111100','01111100','00111000','01111110','01111110','11111111','11111111','00011000','00011000','00011000'],
'02_round_B':[
'00011100','00111110','01111111','01111111','11111111','11111111','11111111','01111111','01111110','00111100','00011000','00011000','00011000','00011000'],
'03_peak_A':[
'00011000','00011000','00111100','00111100','01111110','01111110','11111111','11111111','11111111','11111111'],
'03_hill_A':[
'00111100','00111100','01111110','01111110','11111111','11111111','11111111','11111111','11111111','11111111'],
'04_peak_B':[
'00110000','00110000','01111000','01111000','11111100','11111100','11111111','11111111','11111111','11111111'],
'04_hill_B':[
'00011100','00111110','01111111','01111111','11111111','11111111','11111111','11111111','11111111','11111111'],
'05_spiral_A':[
'11111110','11111110','00000010','00000010','11111010','11111010','10001010','10001010','10111010','10111010','10000010','10000010','11111110','11111110'],
'05_portal_A':[
'00111100','00111100','01111110','11111111','11111111','11100111','11000011','11000011','11000011','11000011','11000011','11000011'],
'06_spiral_B':[
'01111111','01111111','01000000','01000000','01011110','01011110','01010010','01010010','01011110','01011110','01000010','01000010','01111110','01111110'],
'06_portal_B':[
'00011000','00111100','00111100','01111110','11111111','11111111','11000011','11000011','11000011','11000011','11000011','11000011'],
'07_wall_A':[
'11011011','11011011','11011011','11111111','11111111','11111111','11111111','11111111','11111111'],
'07_ruin_A':[
'11000111','11000111','11100111','11101111','11111111','11111111','11111111','11111111','11111111'],
'08_wall_B':[
'10110101','10110101','10110101','11111111','11111111','11111111','11111111','11111111','11111111'],
'08_ruin_B':[
'11100001','11100011','11100111','11100111','11101111','11111111','11111111','11111111','11111111']
}
# Revision 2 visual review, Atari TV aspect: a 4-colour-clock PF1 bit is about 6-7
# square-ish 320x240 CRT pixels wide. Four/eight identical PF bytes overstretch
# glyphs; target 6-7 physical scanlines per original sketch row by holding
# hand-drawn PF lines 2-4 entries each. Every resulting table entry is still 2
# physical scanlines. Shapes, envelopes, and byte counts are never post-scaled.
def H(*pairs):
 return [row for row,count in pairs for _ in range(count)]
motifs.update({
 '01_fir_A': H(('00011000',3),('00111100',3),('01111110',4),('11111111',3),('01111110',1),('00011000',7)),
 '01_round_A': H(('00011000',2),('00111100',2),('01111110',3),('11111111',5),('01111110',3),('00111100',2),('00011000',5)),
 '02_fir_B': H(('00010000',2),('00111000',3),('01111100',3),('00111000',1),('01111110',3),('11111111',3),('00011000',6)),
 '02_round_B': H(('00011100',2),('00111110',3),('01111111',3),('11111111',5),('01111111',3),('00111110',2),('00011000',4)),
 '03_peak_A': H(('00011000',3),('00111100',3),('01111110',4),('11111111',7)),
 '03_hill_A': H(('00111100',3),('01111110',4),('11111111',9)),
 '04_peak_B': H(('00110000',3),('00111000',2),('01111100',4),('11111110',3),('11111111',5)),
 '04_hill_B': H(('00011100',2),('00111110',3),('01111111',4),('11111111',7)),
 '05_spiral_A': H(('11111110',3),('00000010',3),('11111010',3),('10001010',3),('10111010',3),('10000010',3),('11111110',3)),
 '05_portal_A': H(('00111100',3),('01111110',3),('11111111',3),('11100111',2),('11000011',9)),
 '06_spiral_B': H(('01111111',3),('01000000',3),('01011110',3),('01010010',3),('01011110',3),('01000010',3),('01111110',3)),
 '06_portal_B': H(('00011000',2),('00111100',3),('01111110',3),('11111111',3),('11000011',9)),
 '07_wall_A': H(('11011011',5),('11111111',15)),
 '07_ruin_A': H(('11000111',4),('11100111',3),('11101111',3),('11111111',9)),
 '08_wall_B': H(('10110101',5),('11111111',15)),
 '08_ruin_B': H(('11100001',3),('11100011',3),('11100111',3),('11101111',3),('11111111',7)),
})
# In REPEAT worlds, bit7 projects right PF1 copy at x96. Keep that bit clear
# so the level3 full-width P0 centre x80 remains unobstructed with halfwidth16.
for key in tuple(motifs):
 if int(key[:2])%2==0:
  motifs[key]=['0'+row[1:] for row in motifs[key]]
meta=[('Skog','Barrträd A','Rundkronat lövträd A','01_fir_A','01_round_A'),('Skog','Barrträd B','Rundkronat lövträd B','02_fir_B','02_round_B'),('Berg','Spetsigt berg A','Rundat berg A','03_peak_A','03_hill_A'),('Berg','Spetsigt berg B','Rundat berg B','04_peak_B','04_hill_B'),('Dröm','Spiral A','Portal A','05_spiral_A','05_portal_A'),('Dröm','Spiral B','Portal B','06_spiral_B','06_portal_B'),('Natt','Mur A','Ruin A','07_wall_A','07_ruin_A'),('Natt','Mur B','Ruin B','08_wall_B','08_ruin_B')]
for k,rows in motifs.items():
 assert all(len(r)==8 and set(r)<={'0','1'} for r in rows),k
assert len(motifs)==16

out={ 'status':'SOURCE_ONLY_REVISION2', 'source':{'pr':60,'head':'2af9855fbe8d3edbe6d01609d3e539547b744aef','rev1_commit':'bd18c41fc24e56759d13a182dceea6e4932eb16b','source_bank3_blob':'62e88de692df80024db8342e0990640a5310f620'}, 'format':{'visible_scanlines':186,'logical_colour_clocks':160,'PF1_bits':8,'PF1_bit_colour_clocks':4,'scanlines_per_table_byte':2,'world_bytes':96,'all_world_bytes':768,'renderer_index':'(186 - y) // 2 for 0 <= y < 186','data_screen_order':'reversed table bytes','preview_size':{'native':'160x186 logical colour clocks by scanlines','TV_pixel_ratio':'2 native display pixels per colour clock, 1 per scanline; rough device aspect visualization, not calibrated CRT'},'limitations':['top two PF1 table entries (indices 94,95) are not accessed by current 186-line visible loop','source-only graphics do not prove beam deadlines or sprite multiplexing']}, 'motifs':motifs,'stages':[] }
# Color proposals reused from R1, no changes to real TIA registers.
r1=json.loads((SOURCE/'R1_WORLD_GRAPHICS_REFERENCE_UNMODIFIED.json').read_text())
colors=r1['palette_proposals'];world_names=['Skog','Berg','Dröm','Natt']
# Colors are source-only approximate display RGB values; not actual hardware/firmware palette.
GOLD='#eebd4c'
# Existing source parse baseline direct from source, verify previous R1 published bytes match R1 json.
def parse_table_from_asm(s):
 return [int(x,16) for x in re.findall(r'\$([0-9a-fA-F]{2})',s.split('PlayPF1:',1)[1].split('ORG $FD00',1)[0])]
orig_bank3=(SOURCE/'BANK3_PR60_EXACT_SOURCE.asm').read_text()
pr60=parse_table_from_asm(orig_bank3)
assert len(pr60)==768,len(pr60)
rev1=[]
for rec in r1['worlds']:
  vals=rec.get('PF1_hex_top_order') or rec.get('PF1_hex_raw')
  if vals is None:
    print('R1 rec keys',rec.keys());raise RuntimeError('Missing R1 data')
  rev1+= [int(v.replace('$',''),16) for v in vals]
assert len(rev1)==768
# PNG from R1 package and current screenshots copied, authenticated older emulator evidence only.
for f in (SRC/'08_BEFORE_AFTER').glob('*PR60_ACTUAL_STELLA_UNMODIFIED.png'):
 dest=ROOT/'08_BEFORE_AFTER';dest.mkdir(exist_ok=True)
 if f.resolve() != (dest/f.name).resolve():shutil.copyfile(f,dest/f.name)

def make_data(k_top,k_bottom):
 data=[0]*96
 def fit_motif(k,location,center):
  rows=motifs[k]
  start=center-len(rows)
  if not(start%2):start-=1
  for j,bits in enumerate(rows):
   yi=start+2*j
   idx=(186-yi)//2
   assert idx>=0 and idx<=93 and data[idx]==0,(k,idx)
   data[idx]=int(bits,2)
  return {'name':k,'y_start':start,'y_end_exclusive':start+2*len(rows),'source_rows':len(rows),'height_scanlines':2*len(rows)}
 top=fit_motif(k_top,'top',37)
 bottom=fit_motif(k_bottom,'bottom',151)
 assert all(v==0 for v in data[30:62]), 'minimum 64-line open vertical center corridor preserved'
 return data,top,bottom

def line_bytes(vals):return [vals[(186-y)//2] for y in range(186)]

def rects_for(values,mirror):
 group=[[],[],[],[]]
 for y,b in enumerate(line_bytes(values)):
  if b==0:continue
  f=0 if y<90 else 2
  for bit in range(8):
   if b & (128>>bit):
    x=16+4*bit
    right=(140-4*bit) if mirror else (96+4*bit)
    for sub,x0 in [(f,x),(f+1,right)]:group[sub].extend([(x0,y),(x0+3,y)])
 assert all(group)
 return [[min(x for x,y in g),max(x for x,y in g)+1,min(y for x,y in g),max(y for x,y in g)+1] for g in group]

def check_nav(rects):
 # same bounds and L3 physical halfsize from PREVIOUS delivered source model
 free=set()
 for y in range(22,155):
  for x in range(20,141):
   if all(x+16<a or x-16>=b or y+18<c or y-18>=d for a,b,c,d in rects):free.add((x,y))
 start=(80,88)
 assert start in free
 queue=collections.deque([start]);seen={start}
 while queue:
  x,y=queue.popleft()
  for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if p in free and p not in seen:seen.add(p);queue.append(p)
 return {'source_only_l3_centers':len(free),'connected_from_spawn':len(seen),'all_free_centers_connected':len(free)==len(seen),'central_x80_y63_to119_passable':all((80,y) in free for y in range(63,120))}

stages=[]
for n,(world,top_label,bot_label,top_id,bot_id) in enumerate(meta,1):
 vals,top,bot=make_data(top_id,bot_id)
 mode='mirror' if n%2 else 'repeat'
 boxes=rects_for(vals,n%2==1)
 nav=check_nav(boxes)
 assert nav['all_free_centers_connected'] and nav['central_x80_y63_to119_passable'],(n,nav)
 # Compare existing collision envelope coverage explicitly, not claim same.
 existing=r1['worlds'][n-1]['raw_colliders_xyxy_exclusive']
 assert len(existing)==4
 metrics={}
 for label,section in [('top',line_bytes(vals)[:90]),('bottom',line_bytes(vals)[90:])]:
  metrics[label+'_row_width']=[max([x for x,v in enumerate(section) if v],default=0)]
 bbox=[]
 for q in boxes: bbox.append({'x0':q[0],'x1':q[1],'y0':q[2],'y1':q[3], 'width_cc':q[1]-q[0],'height_scanlines':q[3]-q[2]})
 stage={'stage':n,'world':world,'top_label':top_label,'bottom_label':bot_label,'top_motif':top,'bottom_motif':bot,'mode':mode,'PF1_hex':[f'${v:02X}' for v in vals], 'PF1_binary':[f'{v:08b}' for v in vals],'rects_xyxy_halfopen':boxes,'prior_rev1_rects':existing,'geometric_source_only_l3':nav,'object_bbox':bbox}
 stages.append(stage)
 out['stages'].append(stage)
new=sum([x['PF1_hex'] for x in stages],[])
assert len(new)==768
rawnew=bytes(int(v[1:],16) for v in new)
rawbase=bytes(pr60); rawr1=bytes(rev1)
assert len(rawnew)==len(rawr1)==len(rawbase)==768
newsha=hashlib.sha256(rawnew).hexdigest()
rev1sha=hashlib.sha256(rawr1).hexdigest()
basesha=hashlib.sha256(rawbase).hexdigest()
changed_from_rev1=sum(a!=b for a,b in zip(rawnew,rawr1))
changed_from_pr60=sum(a!=b for a,b in zip(rawnew,rawbase))
out['hashes']={'new_PF1_768B_sha256':newsha,'rev1_PF1_768B_sha256':rev1sha,'pr60_original_PF1_768B_sha256':basesha}
out['comparison']={'bytes_changed_against_rev1':changed_from_rev1,'bytes_changed_against_PR60':changed_from_pr60}
out['palette_proposals_only_unchanged_from_rev1']=colors

# This exact text is the replacement source: every display preview below is based ONLY on these values.
asm=[
'; THE SKRAUN GRAPHICS II / MAIN V / 2026-11-25 / REVISION 2',
'; SOURCE_ONLY; not built into a ROM and not observed in Stella.',
'; Replace only the existing 768 B PlayPF1 region after ORG $FA00 in PR60 bank3.asm.',
'; Current Visible/VisibleArrow read WorldPFIndex[X]=X//2 at X=186...1.',
'; Bit7=leftmost PF1 cell; one bit = 4 TIA colour clocks, each table row = 2 scanlines.',
'; Original U1 / enemy / colors / WorldPFIndex / WorldPFPtr / CTRLPF unchanged.',
'        ORG $FA00',
'PlayPF1:'
]
for s in stages:
 asm.append(f'; World {s["stage"]}: {s["world"]} / {s["mode"]} / TOP {s["top_motif"]["name"]} / BOTTOM {s["bottom_motif"]["name"]}')
 for j in range(0,96,16): asm.append('        dc.b '+','.join(s['PF1_hex'][j:j+16]))
asm+=['; 8 x 96 = 768 bytes, ends at $FD00 (exclusive).','']
(ROOT/'03_PLAYFIELD_DATA.asm').write_text('\n'.join(asm),encoding='utf8')

# Reparse EXACT delivered table and compare to generator's bytes.
block=(ROOT/'03_PLAYFIELD_DATA.asm').read_text().split('PlayPF1:',1)[1]
actual_bytes=[int(q,16) for l in block.splitlines() if 'dc.b' in l for q in re.findall(r'\$([A-Fa-f0-9]{2})',l)]
assert bytes(actual_bytes)==rawnew
assert len(actual_bytes)==768

(ROOT/'04_WORLD_GRAPHICS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rect_data={
 'status':'SOURCE_ONLY_CANDIDATES_NOT_APPLIED',
 'coordinate_system':'X [0,160) colour clocks, Y [0,186) visible rasterlines; each rectangle [x0,x1,y0,y1] with end EXCLUSIVE',
 'warning':'Conservative AABB encloses visual voids of spirals and arch portals; original WorldRects do NOT match all new pixels; no gameplay collision changes authorized',
 'baseline_pr60':'2af9855fbe8d3edbe6d01609d3e539547b744aef',
 'rect_order':['top_left','top_right','bottom_left','bottom_right'],
 'source_only_L3_half_width':16,
 'source_only_L3_half_height':18,
 'stages':[{ 'stage':s['stage'], 'world':s['world'], 'mode':s['mode'], 'new_rectangles':s['rects_xyxy_halfopen'], 'prior_rev1_rectangles':s['prior_rev1_rects'], 'source_only_l3_reachability':s['geometric_source_only_l3']} for s in stages]
}
(ROOT/'05_COLLISION_RECOMMENDATIONS.json').write_text(json.dumps(rect_data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rectasm=['; SOURCE_ONLY collisions. NOT applied to bank0 WorldRects or game ROM.','; [x0,x1,y0,y1] exclusive max bounds, 16 B per stage.','; Requires separate MAIN scope and runtime validation.','ProposedWorldRects:']
for s in stages:
 rectasm.append(f'; Stage {s["stage"]}: {s["world"]}')
 rectasm.append('        dc.b '+','.join(f'${v:02X}' for box in s['rects_xyxy_halfopen'] for v in box))
(ROOT/'05_COLLISION_CANDIDATES_NOT_APPLIED.asm').write_text('\n'.join(rectasm)+'\n')

# Previews: one TIA colour clock per native X, one physical rasterline per native Y.
# 320x186 variant doubles horizontal only. 640x372 doubles both 320x186 display axes.
W,H=160,186

def draw_pfield(vals,world,mode,gold=False):
 c=colors[world]
 im=Image.new('RGB',(W,H),c['background']);dr=ImageDraw.Draw(im)
 col=GOLD if gold else c['world']
 for y,v in enumerate(line_bytes(vals)):
  for bit in range(8):
   if v & (128>>bit):
    left=16+4*bit
    right=140-4*bit if mode=='mirror' else 96+4*bit
    dr.rectangle((left,y,left+3,y),fill=col)
    dr.rectangle((right,y,right+3,y),fill=col)
 return im

u1=json.loads((SOURCE/'SOURCE_U1_LEG1.json').read_text())
u1a=u1['one_candidate_U1_LEG1']['A']
assert len(u1a)==12 and all(len(r)==8 for r in u1a)

def add_L3(im,cx=80,cy=90):
 d=ImageDraw.Draw(im)
 for j,row in enumerate(u1a):
  for i,c in enumerate(row):
   if c=='1':
    x=cx-16+i*4;y=cy-18+j*3
    d.rectangle((x,y,x+3,y+2),fill='#d2d2d1')

def font(size,bold=False):
 fn='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf'
 return ImageFont.truetype(fn,size)

def zoom_tv(im,scale=2):
 # Native x2 horizontal for approximate Atari colour clock aspect; x2 both axes to view.
 return im.resize((W*2*scale,H*scale),Image.Resampling.NEAREST)

def overlay_collisions(im,boxes):
 v=im.convert('RGBA');layer=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(layer)
 for x0,x1,y0,y1 in boxes:d.rectangle((x0,y0,x1-1,y1-1),fill=(250,78,66,65),outline=(255,112,66,240),width=1)
 return Image.alpha_composite(v,layer).convert('RGB')

IMG=ROOT/'06_PREVIEWS';MOT=ROOT/'07_INDIVIDUAL_MOTIFS';COMP=ROOT/'08_BEFORE_AFTER';
for d in [IMG,MOT,COMP]:d.mkdir(exist_ok=True)

def ref_crop(world):
 crops={'Skog':(31,136,537,693),'Berg':(570,136,1075,693),'Dröm':(31,768,537,1323),'Natt':(570,768,1075,1323)}
 return Image.open(REF/'USER_APPROVED_GRAPHIC_REFERENCE_UNMODIFIED.png').convert('RGB').crop(crops[world])

for world in world_names:
 ref_crop(world).save(REF/f'APPROVED_{world.upper().replace("Ö","O")}_UNMODIFIED_CROP.png')

def scene_image_raw(values,world,mode):return draw_pfield(values,world,mode)

for i,s in enumerate(stages):
 n=s['stage'];w=s['world'];mode=s['mode'];name=f'{n:02d}_{w.lower().replace("ö","o")}';vals=[int(v[1:],16) for v in s['PF1_hex']]
 im=scene_image_raw(vals,w,mode)
 im.save(IMG/f'{name}_NATIVE_160x186_SOURCE_ONLY.png')
 zoom_tv(im,2).save(IMG/f'{name}_TV_ASPECT_4X_SOURCE_ONLY.png')
 gold=scene_image_raw(vals,w,mode);gold=draw_pfield(vals,w,mode,True)
 zoom_tv(gold,2).save(IMG/f'{name}_HALO_GOLD_4X_SOURCE_ONLY.png')
 spr=im.copy();add_L3(spr)
 zoom_tv(spr,2).save(IMG/f'{name}_SKRAUN_L3_4X_SOURCE_ONLY.png')
 coll=overlay_collisions(im,s['rects_xyxy_halfopen'])
 zoom_tv(coll,2).save(IMG/f'{name}_COLLISION_PROPOSAL_4X_SOURCE_ONLY.png')
 r1_vals=rev1[i*96:(i+1)*96]
 r1img=scene_image_raw(r1_vals,w,mode)
 r1img.save(COMP/f'{name}_REVISION1_DATA_RECONSTRUCTION_NATIVE.png')
 panel_w=3*380+2*12; panel=Image.new('RGB',(panel_w,580),'#eae8e3');d=ImageDraw.Draw(panel)
 guide=ref_crop(w).resize((365,438),Image.Resampling.NEAREST)
 r1_tv=zoom_tv(r1img,1).resize((365,438),Image.Resampling.NEAREST)
 r2_tv=zoom_tv(im,1).resize((365,438),Image.Resampling.NEAREST)
 for j,pic in enumerate((guide,r1_tv,r2_tv)):
  x=j*392;panel.paste(pic,(x+3,65))
 for j,t in enumerate(('GODKAND RIKTNING, EJ ROM','REVISION 1, SOURCE_ONLY','REVISION 2, SOURCE_ONLY')):
  d.text((j*392+3,14),t,fill='#101010',font=font(16,True))
 d.text((6,525),f'Bana {n} / {w}: två olika motiv | {mode.upper()} | 8-bit PF1, 2 rasterrader per byte',fill='#151515',font=font(17))
 panel.save(COMP/f'{name}_APPROVED_REV1_REV2_COMPARISON.png')

# Pixel artwork extracted from the delivered bytes, not from separate illustration code.
for n,s in enumerate(stages,1):
 w=s['world'];col=colors[w]['world']
 for pos in ('top','bottom'):
  k=s[f'{pos}_motif']['name'];rows=motifs[k]
  xpix=Image.new('RGB',(8,len(rows)),colors[w]['background']);d=ImageDraw.Draw(xpix)
  for y,rr in enumerate(rows):
   for x,c in enumerate(rr):
    if c=='1':d.point((x,y),fill=col)
  xpix.save(MOT/(k+'_PF1_8BIT_ROWS_NATIVE.png'))
  # Rectangle grid intentionally depicts real 4-colour-clock/2-scanline data cells.
  scale_x=42;scale_y=26
  canvas=Image.new('RGB',(8*scale_x+70,len(rows)*scale_y+110),'#eceae6');d=ImageDraw.Draw(canvas)
  pixel=xpix.resize((8*scale_x,len(rows)*scale_y),Image.Resampling.NEAREST)
  canvas.paste(pixel,(35,68))
  for j in range(9):d.line((35+j*scale_x,68,35+j*scale_x,68+len(rows)*scale_y),fill='#777',width=1)
  for j in range(len(rows)+1):d.line((35,68+j*scale_y,35+8*scale_x,68+j*scale_y),fill='#777',width=1)
  d.text((35,12),f'{k} / PF1 SOURCE_ONLY',fill='#161616',font=font(17,True))
  canvas.save(MOT/(k+'_SOURCE_PIXELS_GRID.png'))

# World preview boards with properly styled pixel ratios (native X aspect doubled only).
def board(kind='normal'):
 cw=670;ch=475;output=Image.new('RGB',(cw*4+18*3,ch*2+18),'#eeece7');d=ImageDraw.Draw(output)
 for j,s in enumerate(stages):
  x=j%4*(cw+18);y=j//4*(ch+18)
  vals=[int(v[1:],16) for v in s['PF1_hex']]
  im=draw_pfield(vals,s['world'],s['mode'],gold=(kind=='gold'))
  if kind=='actors':add_L3(im)
  if kind=='collisions':im=overlay_collisions(im,s['rects_xyxy_halfopen'])
  pic=zoom_tv(im,2)
  output.paste(pic,(x+10,y+48))
  d.text((x+12,y+9),f'{s["stage"]}. {s["world"]} | {s["mode"].upper()}',font=font(21,True),fill='#181818')
  d.text((x+10,y+429),f'{s["top_label"]} + {s["bottom_label"]}',font=font(15),fill='#222')
 return output
for kind,filename in [('normal','ALL_EIGHT_ARENAS_REV2_TV_ASPECT_SOURCE_ONLY.png'),('gold','ALL_EIGHT_HALO_GOLD_REV2_SOURCE_ONLY.png'),('actors','ALL_EIGHT_L3_SKRAUN_REV2_SOURCE_ONLY.png'),('collisions','ALL_EIGHT_COLLISIONS_REV2_SOURCE_ONLY.png')]:board(kind).save(IMG/filename)

# Comparison board: original approved screenshot (unchanged), R1 old exact source and R2 new exact source.
compboard=Image.new('RGB',(3*690+32,4*485),'#f0eee9');bd=ImageDraw.Draw(compboard)
for j,w in enumerate(world_names):
 i=2*j;s=stages[i];vals=[int(v[1:],16) for v in s['PF1_hex']]
 approved=ref_crop(w).resize((620,420),Image.Resampling.NEAREST)
 a=zoom_tv(draw_pfield(rev1[i*96:(i+1)*96],w,s['mode']),2).resize((620,420),Image.Resampling.NEAREST)
 b=zoom_tv(draw_pfield(vals,w,s['mode']),2).resize((620,420),Image.Resampling.NEAREST)
 for col,im in enumerate((approved,a,b)):
  x=col*690+20;y=j*485+40
  compboard.paste(im,(x,y))
  bd.text((x,y-32),['ANVANDARREF / DESIGN','R1 / PF1 SOURCE_ONLY','R2 / PF1 SOURCE_ONLY'][col],font=font(18,True),fill='#161616')
compboard.save(COMP/'FOUR_WORLDS_APPROVED_REV1_REV2_OVERVIEW.png')

# Visual metrics from EXACT visible mask. Top/bottom bboxes computed from raw pixels.
metrics=[]
for s in stages:
 t,b=s['top_motif'],s['bottom_motif'];topbox=s['object_bbox'][0];botbox=s['object_bbox'][2]
 metrics.append({'stage':s['stage'],'world':s['world'],'top_y_start':t['y_start'],'bottom_y_end':b['y_end_exclusive'],'top_object_width_cc':topbox['width_cc'],'top_object_height_lines':topbox['height_scanlines'],'bottom_width_cc':botbox['width_cc'],'bottom_height_lines':botbox['height_scanlines'],'top_native_width_to_height':round(topbox['width_cc']/topbox['height_scanlines'],2),'bottom_native_width_to_height':round(botbox['width_cc']/botbox['height_scanlines'],2)})
(ROOT/'METRICS_SOURCE_ONLY.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')

# Full report, handoff and source register are generated deterministically from these exact data.
lines=[]
for s in stages:
 lines.append(f'| {s["stage"]} | {s["world"]} | {s["top_label"]} ({s["top_motif"]["height_scanlines"]} rader) | {s["bottom_label"]} ({s["bottom_motif"]["height_scanlines"]} rader) | {s["mode"]} |')
report=f'''# THE SKRAUN — GRAPHICS II → MAIN V | FINAL WORLD GRAPHICS REVISION 2

**2026-11-25 — SOURCE_ONLY; estetiskt ej slutgodkänd.** Exakt användarreferens (oförändrad) samt samtliga 8 banor, 16 egna grundmotiv och färdig PlayPF1-table enligt befintlig Atari-2600-kernel. Ingen ROM, DASM/Stella-nykörning, ingen main-merge.

## Teknisk diagnos och förbättring

- Ursprungliga Revision 1 repeterade 6 motivrader × 8 fysiska scanlines för 14 motiv (spiraler 12 × 4). Därför blev formerna visuellt långsmala och klippte på överkanten.
- Originalbank3 PR60 visar: 186 synliga rasterrader i `Visible` / `VisibleArrow`, `WorldPFIndex[X] = floor(X/2)`, `LDA (WorldPFPtr),Y; STA PF1`. **En tabellpost visas i två rasterrader**, inte åtta. Det finns **96 bytes per arena**.
- Revision 2 ger oberoende PF1-byte per **2 scanlines**: kompaktare proportioner, 15–25 rasterrader övre marginal, minst 13 rasterrader nedre marginal. Övergången i mitten är tom och väl tilltagen; inga extra TIA-skrivningar/RAM/mapper.
- TIA bit7→bit0 vänster-till-höger i PF1 x16..47; varje bit är **4 färgklockor** bred. Spelplanen är 160 färgklockor och 186 scanlines i den aktuella synliga loopen. Därför levereras både exakt 160×186 native och TV-proportionerad presentation med **2 horisontella bildpunkter per färgklocka**. Exakt analog CRT-kalibrering ingår inte.
- **Viktig risktolkning:** De två oanvända toppindex 94/95 ändras inte; y=0–15 lämnas tomt. Indextabell, bankpekare, spegling/upprepning, färg och source ownership är oförändrade.

## Åtta banor

| Bana | Värld | Övre motiv | Nedre motiv | PF-sätt |
|---|---|---|---|---|
{chr(10).join(lines)}

## Byteproveniens

- PR60 fryst baseline commit: `2af9855fbe8d3edbe6d01609d3e539547b744aef`; ROM SHA256 `3977c1e04e2cb5a43944e32477b8fa6f443bff270e3af8db4ae3d25e497b9647` **(den gamla ROM:en, inte en ny körning)**.
- Revision 1 grafikcommit `bd18c41fc24e56759d13a182dceea6e4932eb16b`, oförändrad; ursprunglig R1 PF1 data SHA256 `{rev1sha}`.
- Revision 2 PlayPF1 **768 bytes** SHA256 `{newsha}`; {changed_from_rev1} ändrade byte mot R1 och {changed_from_pr60} mot PR60 original PF1.
- Alla bitmasker och samtliga PNG-renderingar kommer från EXAKT samma 768 byte som _PLAYFIELD_DATA.asm`. Kontrollera med `09_GENERATOR/rebuild.py` efter behov; assertions av längd, parser och navigationsmodell.

## Visuell självgranskning (16 motiv)

1. Skog: barrträd A/B bredare och nivåsluttande triangulära kronor, ordentligt smala stammar; lövträd A/B rundare större kronor och kortare stammar.
2. Berg: spetsar A/B har två tydliga stegsluttningar, rundare berg har kompakt slätare topp och låg bred kropp.
3. Dröm: spiraler A/B statiska och avsiktligt tvåradigt upprepade för att se kvadratiska ut; portaler A/B har bred båge med negativ öppning i mitten. PF-bitbredden begränsar fortfarande inre slingdetaljer.
4. Natt: breda murkrön med skilda tinnar; ruiner varierar höjd på varje sidopelare och faller mot en låg, bred grund.
5. Placering: överst och nederst tydliga kantmarginaler. Öppen centrumyta; inget motiv inverterat. Åtta grupper använder olika bitmasker även inom samma värld.

## Kollisionsanalys och kvarstående osäkerhet

- Alla 8 banor har **fyra separata konservativa AABB-förslag**, baserade på synlig faktiska masker och nuvarande mirror/repeat. Befintliga bank0 WorldRects` matchar inte exakt och har INTE modifierats.
- Source-only BFS på spelarcentrum med L3 half-width=16 och half-height=18 anger sammanhängande rörelseområde från (80,88) i samtliga 8 arenor, under denna enkla axeljusterade rektangelmodell. Det är **inte** ett bevis på fysisk 8-vägs rörelse, diagonalglid, orb-säkerhet, fiendeplacering eller verkliga Stella-kollisioner.
- Portaler och spiraler innehåller synliga hål som omsluts av konservativa solida rektanglar. Detta är en estetik/soliditet-kompromiss att MAIN måste välja vid separat ROM-integration; spelmotorn är oförändrad.
- Halo-testmodell B: all PF blir guldfärgad när halo aktiv; GPU/ROM begränsar synlig full 360° ring. SOURCE_ONLY guldbilder är en PF-färgmodell, inte ett bevis på rörlig ring.

## Nästa steg (endast rekommendation)

MAIN V godkänner eventuellt konst. Därefter separat ROM DEVELOPMENT-uppdrag för att byta de 768 databyten i bank3 och eventuellt de 128 WorldRects-byten i bank0. Kör verklig DASM/Stella NTSC, äkta ban- och kollisionsspeltest L3, 262 scanlines, beamdeadlines, och mot aktuell gameplay-Halo. Ingen fryst sprite eller canon ändras av denna grafikleverans.

**STOP: GRAPHICS II, SOURCE_ONLY_REVISION2, ingen implementationsorder.**
'''
# replace Unicode control characters from string templates explicitly
report=report.replace('\u0016','1').replace('\u0003','`').replace('\u0002','`')
(ROOT/'01_GRAPHICS_REPORT.md').write_text(report,encoding='utf8')

handoff=f'''# THE SKRAUN | MAIN V och ROM DEVELOPMENT — REVISION 2 SOURCE_ONLY

**Inget implementationsuppdrag.** R2 kandidatdata för PR60 baseline `2af9855fbe8d3edbe6d01609d3e539547b744aef`.

När MAIN ger separat ROM-order: byt enbart tabellraderna efter `ORG $FA00` och `PlayPF1:` i `experiments/fullgame1_arrow_halo_20261125/bank3.asm` fram till `ORG $FD00` mot **03_PLAYFIELD_DATA.asm**. Kontrollera ORG och bevara befintliga `WorldPFIndex`, `Visible`, `VisibleArrow`, `WorldPFPtr`, `CTRLPF`, bankning och all fiend-/U1-kod. **PF1-byte 768, hash `{newsha}`.**

Rekommenderade (ej införda!) WorldRects i `05_COLLISION_RECOMMENDATIONS.json` och `05_COLLISION_CANDIDATES_NOT_APPLIED.asm`, totalt 8×16 byte. Kontrollera byteordningen `x0,x1,y0,y1` med bank0 `InstallWorldMap` och `CandidateValid`; behåll kollisionsmodell separat från synlig port-/spiralöppning. Front-end använder fyra verkligt solida AABB, inte pixel-maskkollision.

Färger och guldfärgade hinder under halo, spelarnas storlekar, sprites, kontroller, AI, orber, pilar och nivå-3-regler ändras inte.

Före GO: fysisk Stella med verkliga spelinput, samtidiga fall, 262 NTSC, TIA beamdeadlines, korrekt synlig mask/ordning/mirroring, kollision/diagonalglid vid L3, säkra orbpositioner. SOURCE_ONLY BFS är inte oberoende verifiering. Ingen merge utan nytt beslut.
'''
(ROOT/'02_HANDOFF_TO_ROM_DEVELOPMENT.md').write_text(handoff,encoding='utf8')

start='''# THE SKRAUN — FINAL WORLD GRAPHICS REVISION 2

MAIN V:s explicit beställda grafikrevision. **SOURCE_ONLY**; vänta på användarens estetiska godkännande och separat ROM-auktorisation.

01_GRAPHICS_REPORT.md: huvudrapport och teknisk genomgång.
02_HANDOFF_TO_ROM_DEVELOPMENT.md: avgränsad integrationsbeskrivning.
03_PLAYFIELD_DATA.asm: 8 × 96 B färdiga PF1-masker, hex.
04_WORLD_GRAPHICS.json: 16 motiv, alla exakta tabellbyte och placeringar.
05_COLLISION_RECOMMENDATIONS.json / 05_COLLISION_CANDIDATES_NOT_APPLIED.asm: föreslagen men EJ implementerad AABB.
06_PREVIEWS: åtta banor, 4x pixelvy, L3 Skraun, golden halo-PF och kollision.
07_INDIVIDUAL_MOTIFS: 16 originalmasker och zoomade pixelgrids.
08_BEFORE_AFTER: per-bana användarref/R1/R2 och gamla original Stella-källbilder (kontext, ej R2 Stella).
09_GENERATOR: fryst PR60 bank0/bank3, R1 rådata, U1 referens och reproducerbar rebuild.py.
11_APPROVED_VISUAL_REFERENCE: båda tidigare referensbilderna oförändrade + fyra ursprungliga världscrops.
SHA256SUMS.txt: kontrollera SHA256 för alla levererade filer utom manifestet självt.

ZIP är endast en art-/designleverans. Ingen ROM eller core-modifiering.
'''
(ROOT/'00_START_HAR.md').write_text(start,encoding='utf8')

source_register=f'''# Revisionsproveniens och tillstånd

- 2026-11-25. MAIN V grafisk explicit revisionsorder från denna konversation.
- User APPROVED_GRAPHICS direction: `11_APPROVED_VISUAL_REFERENCE/USER_APPROVED_GRAPHIC_REFERENCE_UNMODIFIED.png` (användarbild, ej TIA-proof).
- R1 image: `11_APPROVED_VISUAL_REFERENCE/REVISION1_EIGHT_WORLDS_UNMODIFIED.png`, source-based screenshot, not Stella.
- R1 public frozen HEAD `bd18c41fc24e56759d13a182dceea6e4932eb16b`; delivered package, 118 files, SHA256 `35673f0474790336cfea58326ca318f444cc2175297e8cc7b86f3b2881233a78`.
- ROM baseline: draft [PR #60](https://github.com/Odourman/the-skraun/pull/60) frozen HEAD `2af9855fbe8d3edbe6d01609d3e539547b744aef`; 16KiB actual ROM SHA256 `3977c1e04e2cb5a43944e32477b8fa6f443bff270e3af8db4ae3d25e497b9647` (NOT updated by GRAPHICS).
- PR60 `bank3.asm` GitHub blob `62e88de692df80024db8342e0990640a5310f620` read through GitHub connector 2026-11-25; frozen exact original code snapshot in 09_GENERATOR.
- R2 new PF1 bytes SHA256 `{newsha}` 768 bytes; created from exactly 16 source masks in generator.
- Rendering: Python Pillow nearest neighbour, derived from raw PF1 data; R2 previews are **NOT actual Stella**.
- Unmodified 8 older PR60 Stella images in 08_BEFORE_AFTER/ are for historic comparison only, not from a new R2 ROM.
- Bounded SOURCE_ONLY geometry BFS and mask parser, NOT actual joystick input, physical beam timings, RAM/stack or independent verification.
- No player/enemy sprite, sprites' original U1 masks, mapper, RAM, game ROM, gameplay rules, active branch or main were touched.
'''
(ROOT/'10_SOURCE_REGISTER.md').write_text(source_register,encoding='utf8')

# Copy generator source into package after building. Make this same file self-contained by modifying prefix at copy time.
current_code=Path(__file__).read_text(encoding='utf8')
cut=current_code.index('motifs={')
portable_prefix='''#!/usr/bin/env python3
"""Rebuild all R2 graphics from the existing frozen source snippets and approved image.
Requires Pillow only. No network, GitHub writes, Stella, or ROM implementation.
"""
from pathlib import Path
import shutil,json,hashlib,re,math,collections,io,sys,zipfile
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'09_GENERATOR'
SRC=ROOT
REF=ROOT/'11_APPROVED_VISUAL_REFERENCE'
'''
portable_code=portable_prefix+current_code[cut:]
(SOURCE/'rebuild.py').write_text(portable_code,encoding='utf8')
# Remove unintended intermediate pycache from distribution
for cache in ROOT.rglob('__pycache__'):shutil.rmtree(cache)
# Manifest for every delivered file, including generator and references, excluding itself
manifest=[]
for file in sorted(ROOT.rglob('*')):
 if file.is_file() and file.name!='SHA256SUMS.txt':
  h=hashlib.sha256(file.read_bytes()).hexdigest();manifest.append(f'{h}  {file.relative_to(ROOT).as_posix()}')
(ROOT/'SHA256SUMS.txt').write_text('\n'.join(manifest)+'\n')

# Cross-check SHA, number of assets, no accidental mutations to known reference snapshots.
assert len(list(MOT.glob('*PF1_8BIT_ROWS_NATIVE.png')))==16
assert len(list(IMG.glob('*NATIVE_160x186_SOURCE_ONLY.png')))==8
assert len(list(IMG.glob('*TV_ASPECT_4X_SOURCE_ONLY.png')))==8
for entry in manifest:
 hashval,path=entry.split('  ',1);assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==hashval
print(json.dumps({'out':str(ROOT),'PF1_sha256':newsha,'PR60_PF1_sha256':basesha,'R1_PF1_sha256':rev1sha,'bytes_changed_R1':changed_from_rev1,'bytes_changed_PR60':changed_from_pr60,'file_count':len(manifest)+1,'stage_clearance':[{ 'stage':r['stage'],'top_y':r['top_motif']['y_start'],'bottom_end':r['bottom_motif']['y_end_exclusive'],'l3_connected':r['geometric_source_only_l3']['all_free_centers_connected']}for r in stages]},ensure_ascii=False,indent=2))
