"""P01-COL1 cycle-counting subset of 6502 / simple TIA WSYNC / RIOT INTIM.
This is a developer smoke model of the COMPILED ROM, not real Stella or independent Verification.
"""
import sys,collections
from pathlib import Path
ROM=Path(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/skraun_col1_work/artifact/build/col1/p01-col1.bin').read_bytes()
assert len(ROM)==4096

class CPU:
 def __init__(self,joy=0xff,switch=0xff):
  self.mem=bytearray(65536);self.mem[0xF000:0x10000]=ROM
  self.mem[0x280]=joy;self.mem[0x282]=switch
  self.pc=self.mem[0xfffc]|self.mem[0xfffd]<<8
  self.a=self.x=self.y=self.c=self.z=self.n=0;self.sp=0xfd
  self.cy=0;self.vsync=[];self.store_history=[];self.timer_start=-1;self.timer_value=0
  self.max_stack_used=0;self.steps=0;self.overflow=0
 def read(self,addr):
  addr &=65535
  if addr==0x284 and self.timer_start>=0:
   return max(0,self.timer_value-(self.cy-self.timer_start)//64)
  return self.mem[addr]
 def write(self,addr,v):
  addr &=65535;v&=255
  if addr==0x02:
   self.cy+=76-(self.cy%76)
  elif addr==0x296:
   self.timer_start=self.cy;self.timer_value=v
  elif addr==0x00:
   if v&2 and not self.mem[0]:self.vsync.append(self.cy)
   self.mem[0]=v
  else:
   self.mem[addr]=v
  if addr in (0x1b,0x0d,0x0e,0x0f) and len(self.vsync)>=2:
   self.store_history.append((addr,self.cy,v,self.mem[0x82],self.mem[0x80],self.mem[0x81]))
 def flag(self,v):
  v&=255;self.z=int(v==0);self.n=(v>>7)&1;return v
 def fetch(self):
  n=self.read(self.pc);self.pc=(self.pc+1)&65535;return n
 def zp(self):return self.fetch()
 def imm(self):return self.fetch()
 def abs(self):return self.fetch()|(self.fetch()<<8)
 def push(self,x):self.mem[0x100+self.sp]=x&255;self.sp=(self.sp-1)&255;self.max_stack_used=max(self.max_stack_used,255-self.sp)
 def pop(self):self.sp=(self.sp+1)&255;return self.mem[0x100+self.sp]
 def branch(self,cond):
  delta=self.fetch();self.cy+=2
  if cond:
   prev=self.pc;self.pc=(self.pc+(delta if delta<128 else delta-256))&65535
   self.cy+=1+((prev&0xff00)!=(self.pc&0xff00))
 def adc(self,n):
  z=self.a+n+self.c;self.c=int(z>255);self.a=self.flag(z)
 def sbc(self,n):
  z=self.a-n-(1-self.c);self.c=int(z>=0);self.a=self.flag(z)
 def cmp(self,left,right):
  self.c=int(left>=right);self.flag(left-right)
 def step(self):
  self.steps+=1;at=self.pc;op=self.fetch()
  if op==0x78 or op==0xD8:self.cy+=2 # sei,cld
  elif op==0x9A:self.sp=self.x;self.cy+=2
  elif op==0xA9:self.a=self.flag(self.imm());self.cy+=2
  elif op==0xA2:self.x=self.flag(self.imm());self.cy+=2
  elif op==0xA0:self.y=self.flag(self.imm());self.cy+=2
  elif op==0xA5:self.a=self.flag(self.read(self.zp()));self.cy+=3
  elif op==0xA6:self.x=self.flag(self.read(self.zp()));self.cy+=3
  elif op==0xA4:self.y=self.flag(self.read(self.zp()));self.cy+=3
  elif op==0xAD:self.a=self.flag(self.read(self.abs()));self.cy+=4
  elif op in (0xBD,0xB9):
   base=self.abs();ix=self.x if op==0xBD else self.y;self.a=self.flag(self.read(base+ix));self.cy+=4+((base&255)+ix>255)
  elif op==0xBC:
   base=self.abs();self.y=self.flag(self.read(base+self.x));self.cy+=4+((base&255)+self.x>255)
  elif op==0xB1:
   p=self.zp();base=self.read(p)|(self.read((p+1)&255)<<8);self.a=self.flag(self.read(base+self.y));self.cy+=5+((base&255)+self.y>255)
  elif op==0x85:self.cy+=3;self.write(self.zp(),self.a)
  elif op==0x8D:self.cy+=4;self.write(self.abs(),self.a)
  elif op==0x95:self.cy+=4;self.write((self.zp()+self.x)&255,self.a)
  elif op==0xE6:
   addr=self.zp();self.cy+=5;self.write(addr,self.flag(self.read(addr)+1))
  elif op==0xCA:self.x=self.flag(self.x-1);self.cy+=2
  elif op==0xC8:self.y=self.flag(self.y+1);self.cy+=2
  elif op==0x8A:self.a=self.flag(self.x);self.cy+=2
  elif op==0x98:self.a=self.flag(self.y);self.cy+=2
  elif op==0xA8:self.y=self.flag(self.a);self.cy+=2
  elif op==0x18:self.c=0;self.cy+=2
  elif op==0x38:self.c=1;self.cy+=2
  elif op==0x69:self.adc(self.imm());self.cy+=2
  elif op==0xE9:self.sbc(self.imm());self.cy+=2
  elif op==0xE5:self.sbc(self.read(self.zp()));self.cy+=3
  elif op==0x29:self.a=self.flag(self.a&self.imm());self.cy+=2
  elif op==0x49:self.a=self.flag(self.a^self.imm());self.cy+=2
  elif op==0x0A:self.c=(self.a>>7)&1;self.a=self.flag(self.a<<1);self.cy+=2
  elif op==0xC9:self.cmp(self.a,self.imm());self.cy+=2
  elif op==0xE0:self.cmp(self.x,self.imm());self.cy+=2
  elif op==0xC5:self.cmp(self.a,self.read(self.zp()));self.cy+=3
  elif op==0xD1:
   p=self.zp();base=self.read(p)|(self.read((p+1)&255)<<8);self.cmp(self.a,self.read(base+self.y));self.cy+=5+((base&255)+self.y>255)
  elif op==0xDD:
   base=self.abs();self.cmp(self.a,self.read(base+self.x));self.cy+=4+((base&255)+self.x>255)
  elif op in (0x10,0x30,0x90,0xb0,0xd0,0xf0):
   self.branch({0x10:not self.n,0x30:bool(self.n),0x90:not self.c,0xb0:bool(self.c),0xd0:not self.z,0xf0:bool(self.z)}[op])
  elif op==0x20:
   dest=self.abs();ret=(self.pc-1)&65535;self.push(ret>>8);self.push(ret&255);self.pc=dest;self.cy+=6
  elif op==0x60:self.pc=((self.pop()|(self.pop()<<8))+1)&65535;self.cy+=6
  elif op==0x4C:self.pc=self.abs();self.cy+=3
  else:raise RuntimeError(f'UNIMPLEMENTED ${op:02X} at ${at:04X} (cycle {self.cy}, step {self.steps}, stack{self.sp:02X})')
 def state(self):return (self.mem[0x80],self.mem[0x81],self.mem[0x82],self.mem[0x9A])
 def run_frames(self,frames):
  target=len(self.vsync)+frames
  for i in range(frames*18000+80000):
   self.step()
   if len(self.vsync)>=target:return
  raise RuntimeError('frames did not advance')

def stable(cpu,label):
    assert len(cpu.vsync)>=3,(label,len(cpu.vsync))
    deltas=[b-a for a,b in zip(cpu.vsync[1:-1],cpu.vsync[2:])]
    assert all(d==262*76 for d in deltas),(label,deltas)
    assert cpu.max_stack_used<32,(label,cpu.max_stack_used)

def fresh():
    c=CPU()
    c.run_frames(3)
    stable(c,'boot')
    return c

def set_scene(c,x,y,level,phase=2):
    c.mem[0x80]=x;c.mem[0x81]=y;c.mem[0x82]=level;c.mem[0x86]=phase
    c.mem[0x85]=0;c.mem[0x9A]=0

def step_controls(c,joy=0xff,switch=0xff,frames=1):
    c.mem[0x280]=joy;c.mem[0x282]=switch
    c.run_frames(frames)
    return c.state()

def test():
    c=fresh()
    assert c.state()==(80,88,1,0),c.state()
    print('BOOT PASS: NTSC 262 lines across regular frames, centred L1, compiled 4KiB ROM, max stack',c.max_stack_used)
    # Six independent 6502-runtime direction tests, no emulator source oracle.
    cases=[('Right',0x7f,81,88),('Left',0xbf,79,88),('Up',0xef,80,87),('Down',0xdf,80,89),
           ('RightUp',0x6f,81,87),('LeftDown',0x9f,79,89),('LeftUp',0xaf,79,87),('RightDown',0x5f,81,89)]
    for label,joy,x,y in cases:
        c=fresh();set_scene(c,80,88,1,phase=2)
        got=step_controls(c,joy)
        assert got[:3]==(x,y,1),(label,got,(x,y,1))
        stable(c,label)
        print('MOVE PASS',label,got)
    # Compiled ROM performs strictly protected corner slide, never the prior K0 diagonal cut.
    c=fresh();set_scene(c,48,69,3,phase=2)
    got=step_controls(c,0x9f)
    assert got[:3]==(48,70,3),('corner must slide Y only from true K0 source geometry',got)
    stable(c,'corner')
    print('CORNER PASS',got,'for left+down from (48,69), Level3')
    # The four diagnostic obstacles are physically blocked, separate from PF art.
    c=fresh();set_scene(c,48,60,3,phase=0)
    got=step_controls(c,0xbf)
    assert got[:3]==(48,60,3),('collision x47 should be forbidden at y60',got)
    print('SOLID EDGE PASS',got)
    # Level3 movement remains open in central combat corridor, without altered speed.
    c=fresh();set_scene(c,80,88,3,phase=0)
    got=step_controls(c,0x7f,frames=90)
    assert got[:3]==(140,88,3),('right bound + full movement',got)
    stable(c,'90-frame level3 motion')
    print('LEVEL3 SPACE PASS',got,'frames=90')
    # SELECT is edge-triggered; L2->L3 works if a valid footprint can be accommodated.
    c=fresh();set_scene(c,80,88,2)
    got=step_controls(c,0xff,0xfd)
    assert got[:3]==(80,88,3),('center growth should succeed',got)
    got=step_controls(c,0xff,0xfd,frames=8)
    assert got[2]==3,('held Select should not repeat',got)
    stable(c,'select level2->3')
    print('SAFE GROWTH PASS',got)
    # A Level2-legal centre that would overlap level3 must NOT grow.
    c=fresh();set_scene(c,12,64,2)
    got=step_controls(c,0xff,0xfd)
    assert got==(12,64,2,1),('growth into rock MUST be refused',got)
    stable(c,'blocked growth')
    assert c.mem[0x09]==0x42,('growth-block visual indication missing',c.mem[0x09])
    print('BLOCKED GROWTH PASS',got,'red background indicator',hex(c.mem[0x09]))
    print('ALL CPU 6502 ROM-MODEL SELF-TESTS PASS: 262 nominal NTSC lines; runtime eight directions, corner/solid, growth and Level3 free movement.')
    print('LIMIT: This subset CPU/WSYNC/TIM64T model does NOT verify real TIA raster output or replace real Stella debugger.')
if __name__=='__main__':test()
