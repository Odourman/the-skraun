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
    g.write(cmd, interval=.0005)
    g.press('enter')
    time.sleep(.05)
"""

def run(name, startup, cmds):
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
    env = dict(os.environ, DISPLAY=":170", XDG_CONFIG_HOME=str(out / "config"),
               SDL_AUDIODRIVER="dummy", SDL_VIDEODRIVER="x11", SDL_RENDER_DRIVER="software")
    with (out / "xvfb.log").open("w") as xvlog, (out / "stella.log").open("w") as stlog:
        xv = subprocess.Popen(["Xvfb", ":170", "-screen", "0", "1400x1000x24", "-ac"], stdout=xvlog, stderr=xvlog)
        try:
            time.sleep(.4)
            with subprocess.Popen(["/usr/bin/stella", "-debug", "-logtoconsole", "1",
                "-audio.enabled", "0", "-threads", "0", "-vsync", "0", "-video", "software",
                "-fullscreen", "0", str(local)], env=env, stdout=stlog, stderr=stlog) as stella:
                try:
                    time.sleep(2)
                    session = out / "SESSION.txt"
                    args = cmds + ["ram", "tia", "print _scanEnd", "saveSes " + str(session)]
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
    return dict(scanEnd=int(scan[-1]), x=ram[0x80], y=ram[0x81], level=ram[0x82],
                stage=ram[0xaa], lives=ram[0xac], halo=ram[0x9e],
                score=[ram[a] for a in (0xad,0xae)], tia=[s for s in raw.splitlines() if "COLU" in s])

boot = ["base hex", "frame #12"]
scenes = {
    "natural_idle": (boot, ["frame #10"]),
    "natural_move_halo": (boot, ["joy0fire #0", "joy0right #0", "frame #12", "joy0right #1"]),
    "fixture_death_idle": (boot, ["ram ac 00", "frame #4"]),
    "fixture_death_fire": (boot, ["ram ac 00", "frame #4", "joy0fire #1", "frame #2", "joy0fire #0", "frame #4"]),
    "fixture_death_reset": (boot, ["ram ac 00", "frame #4", "reset", "frame #4"]),
}
result = {}
for name, (start, cmds) in scenes.items():
    try:
        result[name] = run(name, start, cmds)
    except Exception as exc:
        result[name] = {"error": repr(exc)}
(root / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
assert all(row.get("scanEnd") == 262 for row in result.values()), result
