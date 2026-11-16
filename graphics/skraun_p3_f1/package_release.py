#!/usr/bin/env python3
"""Reproducible delivery ZIP. Run only after tests; no archive includes private source drawing."""
from pathlib import Path
import subprocess,sys,zipfile,hashlib
R=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(R/'validate_p3_f1.py')],check=True)
zipname=R.parent/(R.name+'.zip')
with zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in sorted(R.iterdir(),key=lambda x:x.name):
  if not p.is_file():continue
  info=zipfile.ZipInfo(p.name,date_time=(2026,11,16,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=0o644<<16
  archive.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(zipname) as archive:
 assert archive.testzip() is None
print('ZIP',zipname,'BYTES',zipname.stat().st_size,'SHA256',hashlib.sha256(zipname.read_bytes()).hexdigest())
