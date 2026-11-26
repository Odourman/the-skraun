"""Extract decision evidence, TIA write sites, and RIOT declarations from PR61."""
from collections import defaultdict
from pathlib import Path
import csv
import re
import sys

source, order, output = map(Path, sys.argv[1:])
banks = [(source / f"bank{i}.asm").read_text().splitlines() for i in range(4)]
# Each group points to a source route to inspect. Status covers only the
# source evidence specified here, never comprehensive runtime qualification.
routes = [
"3:UpdateScale 1:HaloVisualSelect","3:RecoverTable","3:RadiusTable 1:HaloRimReach","2:UpdateArrow","0:DamagePlayer",
"2:InitializeGame","0:DamageLife","3:UpdateOrb","2:NextStage","0:DamagePlayer 2:GameRunning",
"3:UpdateAttack","3:Frame","0:DamagePlayer","0:RangerCooldowns","0:RangerCooldowns",
"0:ChooseRanger","2:NextStage","0:ReserveTick","0:ReserveTick","3:MoveX 3:MoveY",
"0:KnightBlockRect","0:ChooseLiveP1","0:ChooseLiveP1","2:UpdateArrow","2:UpdateArrow",
"3:UpdateOrb","2:PlaceStageOrb","0:AwardKnight","0:AwardKnight","0:DamageLife",
"2:NextStage","2:NextStage","0:WorldRects","2:UpdateArrow","3:RadiusTable",
"2:SwordLineClear","0:KnightBlockRect","0:KnightBlockRect","0:RangerCooldowns","0:ChooseRanger",
"2:UpdateArrow","2:UpdateArrow","0:ChooseK1","0:DamagePlayer","0:ChooseLiveP1",
"3:DetectDiagonal","3:UpdateScale","3:RecoverTable","3:UpdateAttack","0:DamagePlayer 3:Frame",
"3:UpdateOrb","2:InitializeGame","2:GamePauseOnly","0:WorldRects 3:PlayPF1","3:MoveX 3:MoveY",
"3:HudDraw","1:AudioEngine","2:GameOverImpl 3:GateDispatch","0:ChooseLiveP1","2:NextStage"]
# Source facts with a focused, concrete diagnostic.
findings = {
 1:("PARTIAL","Upright mask route in normal mode. Rune replaces body under halo.","Compare original silhouette and radius across three levels"),
 2:("MATCH","Cooldown table 60/36/15 frames.","Measure sustained FIRE"),
 3:("PARTIAL","Radius table 18/28/38. Outer rim phased.","Measure phase coverage against hit mask"),
 5:("MATCH","Both damage paths decrement above L1. L1 decrements lives.","Force hits one at a time with 60-frame separation"),
 8:("MATCH","OrbMask is cleared after successful growth.","Compare same visit before/after life loss"),
 10:("PARTIAL","DamagePlayer sets 60. Visibility and exact decrement boundary need trace.","Check first and 60th frame"),
 11:("MATCH","Attack sets 30 frames.","Capture active-frame boundaries"),
 12:("MATCH","Motion continues via bank3 Frame while alive.","Compare natural moving FIRE with lock variant"),
 15:("PARTIAL","180/150/120/90 table. Actual cadence depends on shot and LOS.","Measure release timestamps"),
 27:("MISMATCH","One fixed StageOrbX per stage and fixed internal Y112.","Prove two safe X placements per map before variation"),
 34:("NOT_TESTED","UpdateArrow route identified.","Aim through each AABB and check removal"),
 46:("PARTIAL","Joystick axes sampled, low-bit phase throttles diagonals.","Record exact 8-direction natural displacement L1–L3"),
 48:("MATCH","RecoverTable 60/36/15.","Measure exact cooldown including first attack frame"),
 51:("PARTIAL","Pickup skipped at L3. BL shared with halo, visibility phased.","Measure orb before/after halo and a subsequent downgrade"),
 54:("PARTIAL","Eight PR61 tables. Approved layout swap is pending in PR61.","Swap B bands and test collisions/shapes"),
 56:("PARTIAL","Life masks for 4 through 9 identical.","Check 0,1,3,4,7,9 and rollover"),
 57:("PARTIAL","Two audio channels and event tables. No audio audition here.","Capture isolated PCM for events and priority mixes"),
 58:("SUPERSEDED","PR61 banner/FIRE is historical behavior.","Black score-only view and console RESET test"),
 59:("PARTIAL","Adaptive P1 selector and limited neutral duplication.","Measure continuous presentation and attack visibility"),
}
later = {"01":"A/B upright U1-LEG1", "03":"4A gold halo and invariant environment", "05":"4D confirmed damage order", "12":"4G motion remains; lock is an experiment","17":"4F limited flicker permitted","28":"4B exact world camo","47":"Frozen visual source and scaled output","54":"4C even stages swap vertical motifs","58":"4E black score-only RESET","59":"4F controlled flicker permitted"}
original = []
for line in order.read_text().split("# BILAGA A",1)[1].split("# BILAGA B",1)[0].splitlines():
    m = re.match(r"\| (\d\d) \| (.*?) \|$", line)
    if m:
        original.append(m.groups())
assert len(original) == 60
def loc(route):
    result = []
    for cell in route.split():
        bank, label = cell.split(":")
        idx = next((i for i,line in enumerate(banks[int(bank)],1) if line.startswith(label+":")), None)
        if idx:
            result.append(f"bank{bank}.asm:{idx} {label}")
    return " / ".join(result)
with (output/"DESIGN_01_60_AND_SUPERSESSION.csv").open("w") as f:
    writer=csv.writer(f)
    writer.writerow(["ID","Historisk lydelse","Senare regel","PR61 källa","Status","Obser­vation (SOURCE_ONLY)","Minsta riktade kontroll"])
    for (n,desc),route in zip(original,routes):
        status,evidence,test=findings.get(int(n),("NOT_TESTED","Källspår inventerat. Regelns fulla beteende ej fastställt.",f"Spela eller injicera isolerat starttillstånd för beslut {n} och kontrollera slutregel."))
        writer.writerow([n,desc,later.get(n,"Historisk regel gäller"),loc(route),status,evidence,test])
    for key,desc,route,stat,fact in [
	    ("4A","Miljön behåller världsfärg, orb guld vid halo","2:SetWorldColors 3:UpdateAttack","MISMATCH","COLUPF guld under halo i PR61."),
	    ("4B","Ranger exakt miljöfärg","0:ChooseRanger","PARTIAL","Neutral tabell identisk. Vid hot används ljusblått."),
	    ("4C","Byt övre/nedre motiv på 2,4,6,8","0:WorldRects 3:PlayPF1","MISMATCH","Historisk ordning i PR61."),
	    ("4D","L3→L2→L1→ett liv","0:DamagePlayer","MATCH","Ett DEC Level och separat livsgren."),
	    ("4E","Svart endast score, RESET","2:GameOverImpl 3:GateDispatch","MISMATCH","PR61 banner och FIRE."),
	    ("4F","Kontrollerat flimmer med tre logiska fiender","0:ChooseLiveP1","PARTIAL","Fasning finns. Ingen ny fysisk rättvisemätning här."),
	    ("4G","Fri rörelse, stillastående prövas","3:Frame","MATCH","Rörelse ingår under aktiv halo."),
    ]:
        writer.writerow([key,desc,desc,loc(route),stat,fact,"Riktad A/B enligt arbetsordern."])
aliases = defaultdict(list)
tia = []
regs = {"VSYNC","VBLANK","WSYNC","GRP0","GRP1","RESP0","RESP1","RESM0","RESM1","RESBL","HMP0","HMP1","HMM0","HMM1","HMBL","HMOVE","HMCLR","ENAM0","ENAM1","ENABL","PF0","PF1","PF2","COLUP0","COLUP1","COLUPF","COLUBK","CTRLPF","NUSIZ0","NUSIZ1","VDELP0","VDELP1","RESMP0","RESMP1"}
for n,lines in enumerate(banks):
    label = ""
    for i,line in enumerate(lines,1):
        code=line.split(";")[0].strip()
        if code.endswith(":"):
            label=code[:-1]
        m=re.fullmatch(r"(\w+)\s*=\s*\$([0-9a-fA-F]{2})",code)
        if m and int(m[2],16) >= 128:
            aliases[int(m[2],16)].append(f"b{n}:{i}:{m[1]}")
        m=re.fullmatch(r"st[axy]\s+(\w+)",code,re.I)
        if m and m[1] in regs:
            tia.append([n,i,label,m[1],code])
with (output/"RIOT_ADDRESSES.csv").open("w") as f:
    w=csv.writer(f);w.writerow(["address","declared aliases","measurement"])
    w.writerows([hex(a)," | ".join(aliases[a]),"SOURCE_ONLY; lifetime incomplete"] for a in range(128,256))
with (output/"TIA_WRITES.csv").open("w") as f:
    w=csv.writer(f);w.writerow(["bank","line","label","register","instruction"]);w.writerows(tia)
