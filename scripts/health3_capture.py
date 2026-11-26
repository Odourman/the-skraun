"""Native Stella A/B with deterministic debugger checkpoints and saved pixels."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
variant = sys.argv[2]
built = root / "build/arrow_halo_romdev4"
rom = built / "THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin"
print("ROM SHA-256", hashlib.sha256(rom.read_bytes()).hexdigest())
gui = """import sys, time, pyautogui as g
g.PAUSE=.008
g.click(155,650)
for cmd in sys.argv[1:]:
    if cmd.startswith('__measure__'):
        prefix = cmd.split(' ',1)[1]
        for block in range(12):
            for sub in ['cls'] + ['frame #1', 'print _scanEnd'] * 10 + ['saveSes '+prefix+str(block)+'.txt']:
                g.write(sub, interval=.0003)
                g.press('enter')
                time.sleep(.06)
        continue
    if cmd == '__console_reset__':
        g.press(chr(96))
        time.sleep(.45)
        g.keyDown('f2')
        time.sleep(.16)
        g.keyUp('f2')
        time.sleep(.25)
        g.press(chr(96))
        time.sleep(.45)
        g.click(155,650)
        continue
    g.write(cmd, interval=.0005)
    g.press('enter')
    time.sleep(.05)
"""

def run(name, startup, cmds, display):
    out = root / "stella" / name
    out.mkdir(parents=True, exist_ok=True)
    config = out / "config" / "stella"
    config.mkdir(parents=True)
    local = out / "skraun.bin"
    shutil.copyfile(rom, local)
    for ext in ("sym", "lst"):
        shutil.copyfile(built / f"bank3.{ext}", local.with_suffix("." + ext))
    (config / "autoexec.script").write_text("\n".join(startup) + "\n")
    (out / "INPUT.txt").write_text("\n".join(startup + cmds) + "\n")
    auth = out / "xauth"
    auth.touch()
    env = dict(os.environ, XAUTHORITY=str(auth), DISPLAY=display, XDG_CONFIG_HOME=str(out / "config"),
               SDL_AUDIODRIVER="dummy", SDL_VIDEODRIVER="x11", SDL_RENDER_DRIVER="software")
    with (out / "xvfb.log").open("w") as xvlog, (out / "stella.log").open("w") as stlog:
        xv = subprocess.Popen(["Xvfb", display, "-screen", "0", "1400x1000x24", "-ac"], stdout=xvlog, stderr=xvlog)
        try:
            time.sleep(.4)
            with subprocess.Popen(["/usr/bin/stella", "-debug", "-logtoconsole", "1",
                "-audio.enabled", "0", "-threads", "0", "-vsync", "0", "-video", "software",
                "-fullscreen", "0", str(local)], env=env, stdout=stlog, stderr=stlog) as stella:
                try:
                    subprocess.run(["xdotool","search","--sync","--onlyvisible","--pid",str(stella.pid)], 
                                   env=env, stdout=subprocess.DEVNULL, check=True, timeout=20)
                    time.sleep(1)
                    session = out / "SESSION.txt"
                    controls = [cmd.replace("__measure__", "__measure__ " + str(out / "FRAME_BLOCK_")) for cmd in cmds]
                    args = controls + ["ram", "tia", "print _scanEnd", "print _scan", "print _sCycles", "print _fCycles", "print _fWsyncCycles", "print _fTimReadCycles", "saveSes " + str(session)]
                    subprocess.run([sys.executable, "-c", gui, *args], env=env, cwd=out, check=True, timeout=60)
                    subprocess.run(["scrot", "-o", str(out / "desktop.png")], env=env, check=True)
                    raw = session.read_text()
                finally:
                    stella.terminate()
        finally:
            xv.terminate()
            xv.wait(timeout=4)
    scan = re.findall(r"> print _scanEnd\s*\n[^\n]*?#(\d+)", raw)
    if not scan or "> ram" not in raw:
        raise RuntimeError(f"Missing data in {name}")
    ram = {}
    for m in re.finditer(r"^([89a-f][0-9a-f]):\s+((?:[0-9a-f]{2}\s*){16})$", raw, re.M | re.I):
        ram.update({int(m[1],16)+i:int(v,16) for i,v in enumerate(m[2].split())})
    assert len(ram) == 128, (name, len(ram))
    if "__measure__" in cmds:
        endpoints = []
        for i in range(12):
            log = (out / ("FRAME_BLOCK_" + str(i) + ".txt")).read_text()
            points = re.findall(r"> print _scanEnd\s*\n[^\n]*?#(\d+)",log)
            assert len(points) == 10, (i, len(points))
            endpoints.extend(int(x) for x in points)
        (out/"MEASURED_ENDPOINTS.json").write_text(json.dumps(endpoints))
        assert endpoints == [262]*120, endpoints
    return dict(scanEnd=int(scan[-1]), x=ram[0x80], y=ram[0x81], level=ram[0x82],
                stage=ram[0xaa], lives=ram[0xac], halo=ram[0x9e],
                score=[ram[a] for a in (0xad,0xae)], tia=[s for s in raw.splitlines() if "COLU" in s])

boot = ["base hex", "frame #12"]
scenes = {
    "natural_idle": (boot, ["frame #10"]),
    "natural_move_halo": (boot, ["joy0Fire #0", "joy0Right #0", "frame #12", "joy0Right #1"]),
    "fixture_death_idle": (boot, ["ram ac 00 57 13", "frame #4"]),
    "fixture_death_fire": (boot, ["ram ac 00 57 13", "frame #4", "joy0Fire #1", "frame #2", "joy0Fire #0", "frame #4"]),
    "fixture_death_reset": (boot, ["ram ac 00 57 13", "frame #4", "__console_reset__", "frame #4"]),
}
for stage in (2, 4, 6, 8):
    scenes[f"fixture_stage_{stage}"] = (boot, [
        f"ram aa {stage-1:02x} 01", "ram be 01", "frame #4",
        "ram 80 50 58 03", "ram b3 60", "frame #4"])
if variant == "single":
    scenes["natural_120"] = (boot, ["joy0Fire #0", "joy0Right #0", "__measure__"])
    scenes["natural_legacy_stage_route"] = (boot, ["joy0Right #0","frame #16","joy0Right #1",
        "joy0Down #0","frame #24","joy0Down #1","joy0Fire #0","joy0Up #0","frame #40",
        "joy0Up #1","joy0Right #0","frame #14","joy0Right #1","frame #420","joy0Fire #1",
        "joy0Right #0","frame #8","joy0Right #1","joy0Down #0","frame #24","joy0Down #1",
        "frame #65","joy0Fire #0","frame #2","joy0Right #0","joy0Up #0","frame #12",
        "joy0Right #1","joy0Up #1","joy0Fire #1"])
result = {}
for idx, (name, (start, cmds)) in enumerate(scenes.items()):
    try:
        result[name] = run(name, start, cmds, f":{170+idx}")
    except Exception as exc:
        result[name] = {"error": repr(exc)}
(root / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
assert all(row.get("scanEnd") == 262 for row in result.values()), result

assert result["natural_move_halo"]["halo"] > 0, result
if variant in ("combined", "locked", "single"):
    assert result["fixture_death_fire"]["lives"] == 0, result
    assert result["fixture_death_fire"]["score"] == [0x57, 0x13], result
    assert result["fixture_death_reset"]["lives"] == 3, result
for stage in (2, 4, 6, 8):
    row = result[f"fixture_stage_{stage}"]
    assert (row["stage"], row["level"]) == (stage, 3), row
