
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
 if(p==21&&v&&!levels[p]){latched=shifted;frames++;assert(edges==frames*56);for(auto b:latched){assert(b==latched[0]);assert((b&15)==(b>>4));}}
 levels[p]=v;
}


#include <deque>
std::deque<char> input;int networkStarts=0;
void startNetwork(){networkStarts++;}
void publishStatus(int32_t,uint32_t,int,bool,bool){}
char readCommand(){if(input.empty())return 0;char c=input.front();input.pop_front();return c;}
#define SOLARSKIN_HOST_TEST
#include "../src/main.cpp"
void finishLeg(){int32_t initial=position;int d=direction;int steps=0;unsigned ticks=0;
 while(true){assert(++ticks<2000000);int32_t before=position;loop();int change=position-before;assert(abs(change)<=1);steps+=abs(change);assert(position>=0&&position<=TRAVEL);
  if(steps>0&&waiting&&direction!=d)break;
 }
 assert(steps==abs(position-initial));assert(steps>0);assert((position-initial)*d>0);assert(position==0||position==TRAVEL);for(auto b:latched)assert(b==0);
}
int main(){setup();assert(networkStarts==1);assert(!stopped);assert(levels[OE]==LOW);
 for(int i=0;i<4;i++){int start=position;finishLeg();assert(abs(position-start)==6287);}
 while(position<123)loop();input.push_back('s');loop();int pos=position;for(int i=0;i<10000;i++)loop();assert(stopped&&position==pos);for(auto b:latched)assert(b==0);
 input.push_back('r');loop();assert(!stopped);finishLeg();assert(position==TRAVEL);
 input.push_back('c');loop();finishLeg();assert(position==0);finishLeg();assert(position==TRAVEL);
 assert(edges==frames*56);
 puts("PASS: actual restored firmware, 7 simulated cascaded registers / 14 outputs, four full 6287-step legs without network service, stop/resume, manual close then automatic reopen, bounds, phase packing, 56 clocks per latch.");
}
