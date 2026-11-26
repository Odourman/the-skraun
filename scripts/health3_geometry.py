"""Model PR61's unsigned AABB predicates on valid center bounds."""
from collections import deque
from pathlib import Path
import csv
import hashlib
import re
import sys

def tables(src):
    b0=(src/"bank0.asm").read_text()
    b3=(src/"bank3.asm").read_text()
    def to_bytes(text):
        return bytes(int(v,16) for v in re.findall(r"\$([0-9A-Fa-f]{2})(?![0-9A-Fa-f])",text))
    rect=to_bytes(re.sub(r";[^\n]*","",b0.split("WorldRects:\n")[1].split("ORG")[0]))
    pf=to_bytes(re.sub(r";[^\n]*","",b3.split("PlayPF1:\n")[1].split("ORG")[0]))
    assert len(rect)==128 and len(pf)==768
    return rect,pf

def run(root):
    rect,pf=tables(root)
    result=[]
    orbs=[96,88,80,80,92,84,88,76]
    for n,orb in enumerate(orbs):
        rects=[tuple(rect[i:i+4]) for i in range(n*16,n*16+16,4)]
        spaces=[]
        for level,(x1,x2,y1,y2,hw,hh) in enumerate([(8,153,10,167,4,6),(12,149,16,161,8,12),(20,141,22,155,16,18)],1):
            legal={(x,y) for x in range(x1,x2) for y in range(y1,y2)
              if all(x+hw<a or x-hw>=b or y+hh<c or y-hh>=d for a,b,c,d in rects)}
            unseen=set(legal)
            reached=set()
            if (80,88) in legal:
                todo=deque([(80,88)])
                unseen.remove((80,88))
                reached.add((80,88))
                while todo:
                    x,y=todo.popleft()
                    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                        p=(u,v)
                        if p in unseen:
                            unseen.remove(p)
                            reached.add(p)
                            todo.append(p)
            spaces.append(reached)
            result.append(dict(stage=n+1,level=level,legal=len(legal),spawn_reachable=len(reached),
                 orb_center_reachable=(orb,112) in reached, safe_grow_centers=None))
        for i,(hw,hh) in enumerate(((7,9),(11,15))):
            result[-3+i]["safe_grow_centers"]=sum(abs(x-orb)<hw and abs(y-112)<hh for x,y in spaces[i]&spaces[i+1])
    # ORB pointer FD23 plus index y reaches FD46..FD49. Actual orb rows use
    # y=(X>>1), so index 35..38. Include both rows in each pair.
    assert all(pf[n*96+i] == 0 for n in range(8) for i in range(35,39))
    return result, hashlib.sha256(pf).hexdigest()

for path in sys.argv[1:]:
    root=Path(path)
    data,sha=run(root)
    print(root,sha,"frames: not measured", "connected",sum(r["legal"]==r["spawn_reachable"] for r in data),"of 24")
    dest=Path("h3/delivery") / ("NAV_" + ("BASELINE" if "pr61" in path else "SWAP")+".csv")
    with dest.open("w") as f:
        w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
