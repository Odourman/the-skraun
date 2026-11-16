#!/usr/bin/env python3
"""Only package already-frozen validated design package. Reproducible ZIP."""
from pathlib import Path
import zipfile,subprocess,sys,hashlib
R=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(R/'validate_u1_fix1.py')],check=True)
output=R.parent/(R.name+'.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for file in sorted(R.iterdir(),key=lambda p:p.name):
  if not file.is_file():continue
  info=zipfile.ZipInfo(file.name,date_time=(2026,11,16,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,file.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(output) as z: assert z.testzip() is None
print('ZIP',output,'size',output.stat().st_size,'SHA256',hashlib.sha256(output.read_bytes()).hexdigest())
