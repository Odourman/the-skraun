"""Minimal task-specific 6502/WSYNC smoke simulation for The Skraun P01.

NOT a TIA emulator, not independent verification or a hardware acceptance test.
Only implements the instructions used by the current P01 ROM.
"""
from pathlib import Path
import sys

rom=Path(sys.argv[1] if len(sys.argv)>1 else 'build/the-skraun-p01.bin').read_bytes()
mem=bytearray(65536)
mem[0xF000:0x10000]=rom
mem[0x280]=0xFF
mem[0x282]=0xFF

class CPU:
 def __init__(self):
  self.pc=mem[0xFFFC]|(mem[0xFFFD]<<8)
  self.a=0;self.x=0;self.y=0;self.sp=0xFD;self.z=0;self.n=0;self.c=0
  self.cycles=0;self.vsync=[];self.wsync=[];self.visible_grps=[]
  self.vblank=2
 def fetch(self):
  v=mem[self.pc];self.pc=(self.pc+1)&65535;return v
 def addr(self):
  lo=self.fetch();hi=self.fetch();return lo|(hi<<8)
 def nz(self,v):
  v&=255;self.z=1 if v==0 else 0;self.n=(v>>7)&1;return v
 def write(self,addr,v):
  addr&=65535;v&=255
  if addr==2:
   self.wsync.append(self.cycles)
   self.cycles+= (76-self.cycles%76) or 76
  elif addr==0:
   if v&2 and not mem[0]:self.vsync.append(self.cycles)
   mem[0]=v
  elif addr==1:
   self.vblank=v
   mem[1]=v
  elif addr==0x1B:
   mem[addr]=v
   if not self.vblank:
    self.visible_grps.append((self.cycles//76,v,mem[0x80],mem[0x81],mem[0x82]))
  else:mem[addr]=v
 def push(self,v):mem[0x100+self.sp]=v&255;self.sp=(self.sp-1)&255
 def pop(self):self.sp=(self.sp+1)&255;return mem[0x100+self.sp]
 def branch(self,condition):
  n=self.fetch();self.cycles+=2
  if condition:
   old=self.pc
   self.pc=(self.pc+(n if n<128 else n-256))&65535
   self.cycles+=1+(1 if old>>8!=self.pc>>8 else 0)
 def step(self):
  pc=self.pc; op=self.fetch()
  if op==0x78: self.cycles+=2 # SEI
  elif op==0xD8:self.cycles+=2 # CLD
  elif op==0xA2:self.x=self.nz(self.fetch());self.cycles+=2
  elif op==0x9A:self.cycles+=2 # TXS
  elif op==0xA9:self.a=self.nz(self.fetch());self.cycles+=2
  elif op==0x95:
   addr=(self.fetch()+self.x)&255;self.cycles+=4;self.write(addr,self.a)
  elif op==0x85:
   addr=self.fetch();self.cycles+=3;self.write(addr,self.a)
  elif op==0x8D:
   addr=self.addr();self.cycles+=4;self.write(addr,self.a)
  elif op==0xCA:self.x=self.nz(self.x-1);self.cycles+=2
  elif op==0x10:self.branch(not self.n)
  elif op==0xD0:self.branch(not self.z)
  elif op==0xF0:self.branch(bool(self.z))
  elif op==0x90:self.branch(not self.c)
  elif op==0xB0:self.branch(bool(self.c))
  elif op==0x20:
   dest=self.addr();ret=(self.pc-1)&65535;self.push(ret>>8);self.push(ret&255);self.pc=dest;self.cycles+=6
  elif op==0x60:self.pc=((self.pop()|(self.pop()<<8))+1)&65535;self.cycles+=6
  elif op==0xAD:self.a=self.nz(mem[self.addr()]);self.cycles+=4
  elif op==0xA5:self.a=self.nz(mem[self.fetch()]);self.cycles+=3
  elif op==0xE6:addr=self.fetch();self.write(addr,self.nz(mem[addr]+1));self.cycles+=5
  elif op==0xC6:addr=self.fetch();self.write(addr,self.nz(mem[addr]-1));self.cycles+=5
  elif op==0x29:self.a=self.nz(self.a&self.fetch());self.cycles+=2
  elif op==0xC9:
   val=self.fetch();res=self.a-val;self.c=int(self.a>=val);self.nz(res);self.cycles+=2
  elif op==0xC5:
   val=mem[self.fetch()];res=self.a-val;self.c=int(self.a>=val);self.nz(res);self.cycles+=3
  elif op==0xE0:
   val=self.fetch();res=self.x-val;self.c=int(self.x>=val);self.nz(res);self.cycles+=2
  elif op==0x38:self.c=1;self.cycles+=2 # SEC
  elif op==0xE9:
   val=self.fetch();res=self.a-val-(1-self.c);self.c=int(res>=0);self.a=self.nz(res);self.cycles+=2
  elif op==0xE5:
   val=mem[self.fetch()];res=self.a-val-(1-self.c);self.c=int(res>=0);self.a=self.nz(res);self.cycles+=3
  elif op==0x49:self.a=self.nz(self.a^self.fetch());self.cycles+=2
  elif op==0x0A:self.c=(self.a>>7)&1;self.a=self.nz(self.a<<1);self.cycles+=2
  elif op==0xB1:
   zp=self.fetch();ptr=mem[zp]|(mem[(zp+1)&255]<<8)
   addr=(ptr+self.y)&65535;self.a=self.nz(mem[addr]);self.cycles+=5+((ptr&0xFF)+self.y>255)
  elif op==0xA8:self.y=self.nz(self.a);self.cycles+=2 # TAY
  elif op==0x8A:self.a=self.nz(self.x);self.cycles+=2 # TXA
  elif op==0x4C:self.pc=self.addr();self.cycles+=3
  else: raise Exception(f'unsupported ${op:02X} at ${pc:04X}, cycles {self.cycles}')

cpu=CPU()
for i in range(200000):
 cpu.step()
 if len(cpu.vsync)>=5:break
print('VSYNC starts (cycles)',cpu.vsync)
print('frame scanlines',[(b-a)//76 for a,b in zip(cpu.vsync,cpu.vsync[1:])])
print('frame cycle counts',[(b-a) for a,b in zip(cpu.vsync,cpu.vsync[1:])])
print('controls state', {k:mem[k] for k in range(0x80,0x8E)})
assert len(cpu.vsync)>=5
assert all((b-a)==262*76 for a,b in zip(cpu.vsync[1:-1],cpu.vsync[2:]))
assert len(cpu.visible_grps)>0
# The smoke model validates simple ROM logic, not an accurate TIA picture.
def scenario(label, joy, switch, frames=15):
 for a in range(0x300): mem[a]=0
 mem[0x280]=joy
 mem[0x282]=switch
 c=CPU()
 for i in range(frames*6000):
  c.step()
  if len(c.vsync)>=frames:break
 assert len(c.vsync)==frames,(label, len(c.vsync))
 assert all(b-a==262*76 for a,b in zip(c.vsync[1:-1],c.vsync[2:])),label
 state=(mem[0x80],mem[0x81],mem[0x82])
 print(label,'pos_x,y,level',state, 'vsync_intervals',len(c.vsync)-1)
 return state

idle=scenario('idle',0xff,0xff)
right=scenario('right',0x7f,0xff)
up=scenario('up',0xef,0xff)
diag=scenario('right/up',0x6f,0xff)
select=scenario('select held',0xff,0xfd)
assert idle==(64,80,1),idle
assert right[0]>idle[0] and right[1]==idle[1]
assert up[1]>idle[1] and up[0]==idle[0]
assert diag[0]>idle[0] and diag[1]>idle[1]
assert diag[0]-idle[0] < right[0]-idle[0]
assert select[2]==2 # edge detection: held button increments only once
print('PASS: ROM movement, diagonals, SELECT edge, frames (model; not Stella)')
# Extended movement and edge checks.
# These are model-only regression tests, not Stella/TIA evidence.
left=scenario('left',0xbf,0xff)
down=scenario('down',0xdf,0xff)
assert left[0]<idle[0] and left[1]==idle[1]
assert down[1]<idle[1] and down[0]==idle[0]
right_bound=scenario('right boundary',0x7f,0xff,130)
left_bound=scenario('left boundary',0xbf,0xff,130)
up_bound=scenario('upper boundary',0xef,0xff,210)
down_bound=scenario('lower boundary',0xdf,0xff,180)
assert right_bound==(118,80,1),right_bound
assert left_bound==(12,80,1),left_bound
assert up_bound==(64,150,1),up_bound
assert down_bound==(64,10,1),down_bound
right_down_bound=scenario('diagonal lower-right',0x5f,0xff,140)
assert right_down_bound==(118,10,1),right_down_bound
print('PASS: model boundaries left/right/up/down, diagonal, stable 262-line frames')
