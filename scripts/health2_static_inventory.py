#!/usr/bin/env python3
"""Extract source-level RAM aliases and ROM occupancy from DASM .sym/.lst outputs.
SOURCE_ONLY: does not prove reachable lifetimes, dynamic cycle bounds or safe patch slots.
"""
from pathlib import Path
import re, json, sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('build/arrow_halo_romdev4')
report={'evidence_class':'SOURCE_ONLY','rom_banks':[],'ram_aliases':{},'tia_write_sites':[],'limitations':[]}
for bank in range(4):
    sym=root/f'bank{bank}.sym'; listing=root/f'bank{bank}.lst'
    aliases={}
    for line in sym.read_text(errors='replace').splitlines():
        m=re.match(r'^([A-Za-z_][\w]*)\s+([0-9A-Fa-f]{4})\b',line)
        if m and int(m.group(2),16)<0x100:
            aliases.setdefault(int(m.group(2),16),[]).append(m.group(1))
    for addr,names in aliases.items():
        report['ram_aliases'].setdefault(f'${addr:02X}',set()).update(names)
    occupied=set(); tia_writes=[]; rows=[]
    for line in listing.read_text(errors='replace').splitlines():
        m=re.match(r'^\s*\d+\s+([0-9A-Fa-f]{4})\s+(.*)$',line)
        if not m: continue
        pc=int(m.group(1),16); cols=line.split('\t')
        src=' '.join(cols[3:]) if len(cols)>3 else ''
        rows.append((pc,line))
        # Look for literal TIA write destinations in the source tail, not guesses from aliases.
        src_full=src
        w=re.match(r'^\s*(?:sta|stx|sty|inc|dec)\s+([A-Za-z_][\w]*|\$[0-9A-Fa-f]+)',src_full,re.I)
        if w:
            target=w.group(1)
            taddr=None
            if target.startswith('$'):
                try:taddr=int(target[1:],16)&0x3f
                except ValueError:pass
            elif target.upper() in {'VSYNC','VBLANK','WSYNC','RSYNC','NUSIZ0','NUSIZ1','COLUP0','COLUP1','COLUPF','COLUBK','CTRLPF','PF0','PF1','PF2','RESP0','RESP1','RESM0','RESM1','RESBL','GRP0','GRP1','ENAM0','ENAM1','ENABL','HMP0','HMP1','HMM0','HMM1','HMBL','HMOVE','HMCLR','CXCLR'}:
                taddr={'VSYNC':0,'VBLANK':1,'WSYNC':2,'RSYNC':3,'NUSIZ0':4,'NUSIZ1':5,'COLUP0':6,'COLUP1':7,'COLUPF':8,'COLUBK':9,'CTRLPF':10,'REFP0':11,'REFP1':12,'PF0':13,'PF1':14,'PF2':15,'RESP0':16,'RESP1':17,'RESM0':18,'RESM1':19,'RESBL':20,'GRP0':27,'GRP1':28,'ENAM0':29,'ENAM1':30,'ENABL':31,'HMP0':32,'HMP1':33,'HMM0':34,'HMM1':35,'HMBL':36,'HMOVE':42,'HMCLR':43,'CXCLR':44}.get(target.upper())
            if taddr is not None:
                tia_writes.append({'bank':bank,'pc':f'${pc:04X}','target':target,'line':line.strip()})
    # Derive emitted bytes from adjacent location counters, but never count
    # an ORG jump as occupancy. DASM abbreviates repeated DC/DS bytes with '*'.
    for i,(pc,line) in enumerate(rows):
        cols=line.split('\t'); src=' '.join(cols[3:]) if len(cols)>3 else ''
        op=re.match(r'^\s*(ORG|ds|dc\.b|dc\.w)\b\s*(.*)',src,re.I)
        obj=cols[2] if len(cols)>2 else ''
        count=0
        if op and op.group(1).lower()=='ds':
            mds=re.match(r'(\d+)\s*,',op.group(2)); count=int(mds.group(1)) if mds else 0
        elif op and op.group(1).lower()=='org':
            count=0
        elif i+1<len(rows):
            np, nline=rows[i+1]
            ncols=nline.split('\t'); nsrc=' '.join(ncols[3:]) if len(ncols)>3 else ''
            next_is_org=bool(re.search(r'\bORG\b',nsrc,re.I))
            if np>pc and not next_is_org:
                count=np-pc
            elif op and op.group(1).lower() in ('dc.b','dc.w'):
                vals=op.group(2).split(';',1)[0].strip()
                count=len([x for x in vals.split(',') if x.strip()])*(2 if op.group(1).lower()=='dc.w' else 1)
            else:
                count=len(re.findall(r'(?<![A-Za-z0-9])([0-9A-Fa-f]{2})(?![A-Za-z0-9])',obj))
        if count and pc<0x10000:
            lo=max(pc,0xF000); hi=min(pc+count,0x10000)
            if lo<hi: occupied.update(range(lo,hi))
    # The last vector row has no following DASM location-counter row.
    if rows:
        pc,line=rows[-1]; cols=line.split('\t'); src=' '.join(cols[3:]) if len(cols)>3 else ''
        if re.match(r'^\s*dc\.w\b',src,re.I): occupied.update(range(max(pc,0xF000),min(pc+2,0x10000)))
    # Count occupied 4KiB cartridge addresses only; DAT/ORG gaps remain visible as holes.
    span={a for a in occupied if 0xF000<=a<=0xFFFF}
    holes=[]; cursor=0xF000
    for a in sorted(span):
        if a>cursor: holes.append([f'${cursor:04X}',f'${a-1:04X}',a-cursor])
        cursor=a+1
    if cursor<=0xFFFF: holes.append([f'${cursor:04X}','$FFFF',0x10000-cursor])
    image=(root/f'bank{bank}.bin').read_bytes()
    unoccupied_non_ff=0
    for start,end,count in holes:
        lo=int(start[1:],16)-0xF000; hi=int(end[1:],16)-0xF000+1
        unoccupied_non_ff+=sum(v!=0xFF for v in image[lo:hi])
    if unoccupied_non_ff: raise SystemExit(f'LISTING_COVERAGE_MISMATCH bank={bank} unoccupied_non_ff={unoccupied_non_ff}')
    free=sum(x[2] for x in holes)
    report['rom_banks'].append({'bank':bank,'size_bytes':4096,'listing_occupied_addresses':len(span),'listing_unoccupied_ranges':holes,'unoccupied_ff_bytes':free,'note':'Candidate ROM addresses left at DASM fill value $FF; fixed ORG/hotspot/vector and runtime safety constraints still apply.'})
    report['tia_write_sites'].extend(tia_writes)
report['ram_aliases']={k:sorted(v) for k,v in sorted(report['ram_aliases'].items(),key=lambda kv:int(kv[0][1:],16))}
report['limitations']=['Aliases are declarations, not live-range proofs.','Static listing holes are not automatically safe insertion points.','Instruction cycle paths require branch/page-cross/runtime analysis; this report does not bound them.','RAM aliases observed via print *$xx are not substituted for Stella ram/dump.']
out=root/'HEALTH2_STATIC_INVENTORY.json'; out.write_text(json.dumps(report,indent=2)+'\n')
print(f'SOURCE_ONLY inventory banks={len(report["rom_banks"])} ram_addresses={len(report["ram_aliases"])} tia_writes={len(report["tia_write_sites"])} output={out}')
for b in report['rom_banks']:
    print(f"BANK{b['bank']} listing-covered={b['listing_occupied_addresses']}/4096 potential-hole-bytes={sum(x[2] for x in b['listing_unoccupied_ranges'])}")
