
#include <cstdint>
#include <cmath>
#include <cstdio>
#include <cassert>
#include <array>
#define HIGH 1
#define LOW 0
#define OUTPUT 1
uint64_t us=0;uint32_t micros(){return us;}uint32_t millis(){return us/1000;}
void delay(unsigned x){us+=x*1000;}void delayMicroseconds(unsigned x){us+=x;}
void pinMode(int,int){}
struct SerialMock{void begin(int){}void println(const char*){}template<class...T>void printf(const char*,T...) {}}Serial;
int levels[40]={};std::array<uint8_t,7> shifted{},latched{};unsigned edges=0,frames=0;
void digitalWrite(int p,int v){
 if(p==18&&v&&!levels[p]){int carry=levels[23];for(int r=0;r<7;r++){int next=shifted[r]>>7;shifted[r]=(shifted[r]<<1)|carry;carry=next;}edges++;}
 if(p==21&&v&&!levels[p]){latched=shifted;frames++;assert(edges==frames*56);for(auto b:latched){assert(b==latched[0]);assert((b&15)==(b>>4));int mask=b&15;assert(mask==0||__builtin_popcount(mask)==2);}}
 levels[p]=v;
}


#include <deque>
struct Command{char type;int32_t steps;int speed;};std::deque<Command> input;
void startNetwork(){}
void publishStatus(int32_t,int32_t,int32_t,int,bool,bool,uint32_t,uint32_t){}
bool readCommand(Command &c){if(input.empty())return false;c=input.front();input.pop_front();return true;}
#define SOLARSKIN_HOST_TEST
#include "../src/main.cpp"
void leg(){int direction=engine.target>engine.position?1:-1;int before=engine.position,steps=0;unsigned ticks=0;
 for(;;){assert(++ticks<12000000);int p=engine.position;loop();int delta=engine.position-p;assert(abs(delta)<=1);steps+=abs(delta);assert(engine.position>=0&&engine.position<=engine.stroke);assert(engine.rate<=engine.maximum+.01f);
  if(steps>0&&engine.waiting)break;
 }
 assert(abs(engine.position-before)==steps);assert((engine.position-before)*direction>0);assert(engine.position==0||engine.position==engine.stroke);
 assert(engine.output&&__builtin_popcount(engine.output)==2);
}
int main(){setup();assert(!engine.stopped);assert(levels[OE]==LOW);assert(engine.stroke*2==50296);
 for(int i=0;i<4;i++){int start=engine.position;leg();assert(abs(engine.position-start)==25148);}assert(engine.cycles==2);
 input.push_back({'s',0,0});loop();int p=engine.position;unsigned f=frames;for(int i=0;i<10000;i++)loop();assert(engine.position==p&&frames==f);for(auto byte:latched)assert(byte==0);
 input.push_back({'t',50296,120});loop();assert(!engine.stopped&&engine.stroke==50296);leg();assert(engine.position==50296);
 input.push_back({'c',0,0});loop();leg();assert(engine.position==0);leg();assert(engine.position==50296);
 assert(edges==frames*56);
 Engine wrap;uint32_t ms=0xfffffff0u,usClock=0xffff0000u;wrap.stroke=100;wrap.target=100;wrap.begin(ms);for(unsigned i=0;i<100000;i++){wrap.tick(ms,usClock);ms++;usClock+=1000;assert(wrap.position>=0&&wrap.position<=100);}assert(wrap.cycles>1);
 puts("PASS: actual stand firmware; 14 identical motor outputs; exactly two coils per active phase; continuous full-stroke reversal without network; 50296 equivalent halfsteps per leg; stop/restart/settings/manual override; 56 clocks per latch; speed/position limits; time counter wrap.");
}
