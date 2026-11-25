#!/usr/bin/env python3
"""Stella 6.7.1 SDL disk real-time audio: verify float32 stereo then save PCM16 WAV.
This establishes genuine output bytes, not aesthetic listening approval.
"""
from pathlib import Path
from array import array
import math, sys, wave, json, hashlib
d=Path("build/fullgame1/audio")
raw=d/"STELLA_REAL_AUDIO_FLOAT32.raw"
if not raw.exists() or raw.stat().st_size < 8192:
    raise SystemExit("NO_REAL_STELLA_AUDIO_CAPTURE")
data=raw.read_bytes()
if len(data)%8:
    raise SystemExit("UNEXPECTED_AUDIO_BYTE_ALIGNMENT")
samples=array('f')
samples.frombytes(data)
if sys.byteorder!='little': samples.byteswap()
finite=all(math.isfinite(x) for x in samples)
peak=max(map(abs,samples)) if finite else float('nan')
mean_sq=sum(float(x)*float(x) for x in samples)/len(samples) if finite else float('nan')
rms=math.sqrt(mean_sq)
if not finite or not (0<peak<=1.0) or rms<0.00001:
    raise SystemExit(f"AUDIO_FORMAT_OR_SIGNAL_UNPROVEN: peak={peak}, rms={rms}")
out=array('h',(max(-32768,min(32767,round(x*32767))) for x in samples))
if sys.byteorder!='little':out.byteswap()
wav=d/"STELLA_REAL_AUDIO_SAMPLE.wav"
with wave.open(str(wav),"wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(out.tobytes())
summary={
 "source":"real Stella 6.7.1 SDL disk capture (audio enabled)",
 "rom":"THE_SKRAUN_FULLGAME1_F6_NTSC.bin",
 "raw_sha256":hashlib.sha256(data).hexdigest(),
 "raw_bytes":len(data),
 "interpreted_audio":"float32 little endian, interleaved stereo, 44100 Hz",
 "channel_frames":len(samples)//2,
 "seconds":round(len(samples)/2/44100,3),
 "peak":round(peak,6),
 "rms":round(rms,6),
 "wave_sha256":hashlib.sha256(wav.read_bytes()).hexdigest(),
 "subjective_listening":"NOT PERFORMED",
 "per_event_audit":"NOT PERFORMED",
 "original_hardware":"NOT TESTED"
}
(d/"REAL_AUDIO_EVIDENCE.json").write_text(json.dumps(summary,indent=2)+"\n")
print("REAL_STELLA_AUDIO_CAPTURE",json.dumps(summary,sort_keys=True))
