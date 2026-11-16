#!/usr/bin/env python3
"""Create reproducible ZIP with stable entry order and fixed zip times; run validator first."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import subprocess,sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'validate_p3.py')],check=True)
out=root.parent/(root.name+'.zip')
with ZipFile(out,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(root.iterdir(),key=lambda x:x.name):
  if not p.is_file():continue
  info=ZipInfo(p.name,date_time=(2026,11,16,0,0,0))
  info.compress_type=ZIP_DEFLATED
  info.external_attr=0o644<<16
  z.writestr(info,p.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
print(str(out),out.stat().st_size)
