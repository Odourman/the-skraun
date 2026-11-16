#!/usr/bin/env python3
"""Pack a deterministic source-validated ZIP; no source changes, no ROM. Manifest must exist."""
import zipfile,hashlib,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(R/'validate_package.py')],check=True)
out=R.parent/(R.name+'.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(R.iterdir(),key=lambda x:x.name):
  if not p.is_file():continue
  zi=zipfile.ZipInfo(p.name,date_time=(2026,11,16,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16
  z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 print('ZIP',len(z.namelist()),'members',out.stat().st_size,'bytes, SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
