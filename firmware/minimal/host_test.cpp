
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

// Seven 74HC595: NEXT pin9 -> DATA pin14 of the next chip.
constexpr uint8_t DATA=23,CLOCK=18,LATCH=21,OE=22,REGISTERS=7;
constexpr uint16_t TRAVEL=6287;
constexpr uint8_t HALF[8]={1,3,2,6,4,12,8,9};
constexpr float MAX_RATE=180,MIN_RATE=40,ACCEL=80;
uint8_t phase=0;int direction=1;uint16_t done=0;
float rate=MIN_RATE;uint32_t nextUs=0,pauseUntil=0,lastRampUs=0;
bool waiting=true;
void sendPattern(uint8_t pattern){
 uint8_t byte=(pattern&15)|((pattern&15)<<4);
 digitalWrite(CLOCK,LOW);digitalWrite(LATCH,LOW);
 for(int r=REGISTERS-1;r>=0;r--)for(int b=7;b>=0;b--){
  digitalWrite(DATA,(byte>>b)&1);delayMicroseconds(5);
  digitalWrite(CLOCK,HIGH);delayMicroseconds(5);
  digitalWrite(CLOCK,LOW);delayMicroseconds(5);
 }
 digitalWrite(LATCH,HIGH);delayMicroseconds(5);digitalWrite(LATCH,LOW);
}
void setup(){
 digitalWrite(OE,HIGH);pinMode(OE,OUTPUT);digitalWrite(OE,HIGH);
 pinMode(DATA,OUTPUT);pinMode(CLOCK,OUTPUT);pinMode(LATCH,OUTPUT);
 digitalWrite(DATA,LOW);digitalWrite(CLOCK,LOW);digitalWrite(LATCH,LOW);
 sendPattern(0);digitalWrite(OE,LOW);
 Serial.begin(115200);
 Serial.println("SolarSkin CONTINUOUS: 7 registers, 14 motors; no WiFi; +6287/-6287 forever; initial closed position assumed");
 pauseUntil=millis()+5000;
}
void loop(){
 if(waiting){
  if((int32_t)(millis()-pauseUntil)<0){delay(1);return;}
  waiting=false;done=0;rate=MIN_RATE;nextUs=lastRampUs=micros();
  Serial.printf("ALL 14: direction=%d, commanded halfsteps=%u\n",direction,TRAVEL);
 }
 uint32_t now=micros();if((int32_t)(now-nextUs)<0){delayMicroseconds(40);return;}
 float dt=(uint32_t)(now-lastRampUs)*.000001f;lastRampUs=now;
 float brake=sqrtf(2*ACCEL*(TRAVEL-done));
 rate=fminf(MAX_RATE,fminf(rate+ACCEL*dt,fmaxf(MIN_RATE,brake)));
 phase=(phase+(direction>0?1:7))&7;
 sendPattern(HALF[phase]);done++;
 // One bounded step per service; no burst catch-up after serial or other delays.
 nextUs=now+(uint32_t)(1000000.f/rate);
 if(done==TRAVEL){
  sendPattern(0);Serial.println("LEG COMPLETE; outputs zero; reverse after 1 second");
  direction=-direction;waiting=true;pauseUntil=millis()+1000;
 }
}

int main(){setup();assert(levels[22]==0);for(auto b:latched)assert(b==0);
 int legs=0;bool oldWaiting=waiting;unsigned moveFrames=0,lastFrames=frames;
 while(legs<4){loop();if(frames>lastFrames){moveFrames+=frames-lastFrames;lastFrames=frames;}
  if(waiting&&!oldWaiting){legs++;assert(done==6287);for(auto b:latched)assert(b==0);}
  oldWaiting=waiting;
 }
 assert(moveFrames==4*(6287+1));
 puts("PASS: actual firmware; 7 cascaded registers; 14 identical phase sequences; 4 alternating legs of 6287 steps; zero outputs during pauses; 56 CLOCK pulses per LATCH.");}
