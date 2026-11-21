#!/usr/bin/python3
from pathlib import Path
from PIL import Image
import sys,json,hashlib
root=Path(sys.argv[1])
files=sorted(root.glob('PLAY1_FRAME_*.png'))
assert len(files)==13,(len(files),'must capture actual Stella GUI 12 consecutive frames')
data=[]
for f in files:
  im=Image.open(f).convert('RGB')
  assert im.size==(1400,1000),im.size
  crop=im.crop((121,115,441,343)) # debugger TIA pane, exact raw pixels
  crop.save(root/f.name.replace('FRAME','TIA'))
  pixels=crop.getcolors(320*228)
  data.append({'frame':f.name,'color_count':len(pixels),'RGB_sha256':hashlib.sha256(crop.tobytes()).hexdigest(),'palette':sorted(pixels,reverse=True)[:8]})
assert all(x['color_count']>2 for x in data),data
(root/'STELLA_ACTUAL_TIA_RGB_SUMMARY.json').write_text(json.dumps(data,indent=2))
print('13 genuine Stella Xvfb screens captured; visible palette:',data[1]['palette'])
print('Hashes:',[x['RGB_sha256'][:12] for x in data])
print('NOTE: screenshot presence is NOT validated orb/halo/target gameplay.')
