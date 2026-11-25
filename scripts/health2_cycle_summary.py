#!/usr/bin/env python3
"""Read one explicitly delimited native Stella counter capture per session.
Fail closed on ambiguous, missing or stale measurements. Frame totals only.
"""
import csv,hashlib,json,re,sys
from pathlib import Path
KEYS=('_scanEnd','_fCycles','_fWsyncCycles','_fTimReadCycles','_sp','_bank','pc')
FIELDS=['scene','source','input_class','rom_sha256','symbol','expected_pc','expected_bank',*KEYS]
def parse_capture(text,expected_pc,expected_bank):
    # The harness emits the start/end commands without stepping between them.
    starts=list(re.finditer(r'^> print \$6a51\s*$',text,re.M|re.I)); ends=list(re.finditer(r'^> print \$6a52\s*$',text,re.M|re.I))
    if len(starts)!=1 or len(ends)!=1 or starts[0].end()>=ends[0].start(): raise ValueError('missing/ambiguous measurement markers')
    part=text[starts[0].end():ends[0].start()]
    row={}
    for key in KEYS:
        m=re.findall(r'^> print '+re.escape(key)+r'\s*\n([^\n]+)',part,re.M|re.I)
        if len(m)!=1: raise ValueError(f'COUNTER_MISSING_OR_DUPLICATE {key}')
        v=re.search(r'#(\d+)\b',m[0]); h=re.search(r'\$([0-9a-f]+)\b',m[0],re.I)
        if not (v or h): raise ValueError(f'BAD_COUNTER {key} {m[0]}')
        row[key]=int(v[1]) if v else int(h[1],16)
    if row['pc']!=expected_pc or row['_bank']!=expected_bank: raise ValueError('PC/BANK mismatch')
    return row
if __name__=='__main__':
    root,out,rom=map(Path,sys.argv[1:4]); sha=hashlib.sha256(rom.read_bytes()).hexdigest(); rows=[]
    for p in sorted(root.glob('*/COUNTERS.txt')):
        meta=json.loads(p.with_name('CAPTURE.json').read_text()); sym=Path(meta['sym_path']); lst=Path(meta['lst_path'])
        if meta['rom_sha256']!=sha or not sym.is_file() or not lst.is_file() or hashlib.sha256(sym.read_bytes()).hexdigest()!=meta['sym_sha256'] or hashlib.sha256(lst.read_bytes()).hexdigest()!=meta['lst_sha256']: raise SystemExit('ROM/symbol/listing provenance mismatch')
        symbols=dict((n,int(v,16)) for n,v in re.findall(r'^([\w.]+)\s+([0-9a-fA-F]{4})\b',sym.read_text(),re.M))
        if symbols.get(meta['symbol'])!=meta['expected_pc']: raise SystemExit('Symbol address mismatch')
        rows.append(dict(scene=p.parent.name,source=p.name,input_class=meta['input_class'],rom_sha256=sha,symbol=meta['symbol'],expected_pc=meta['expected_pc'],expected_bank=meta['expected_bank'],**parse_capture(p.read_text(),meta['expected_pc'],meta['expected_bank'])))
    if not rows: raise SystemExit('NO VALID CAPTURES')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'evidence_class':'DEVELOPER_OBSERVED','limits':'Breakpoint counters; not per-line deadlines or stack high-water','scenes':rows},indent=2)+'\n')
    with out.with_suffix('.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    print('CAPTURES',len(rows))
