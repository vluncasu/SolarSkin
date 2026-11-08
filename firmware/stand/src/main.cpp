#ifndef SOLARSKIN_HOST_TEST
#include <Arduino.h>
#include "network.h"
#endif
#include "engine.h"
constexpr uint8_t DATA=23,CLOCK=18,LATCH=21,OE=22;
Engine engine;uint32_t sentFrames=0;
void sendPattern(uint8_t p){
 sentFrames++;uint8_t byte=(p&15)|((p&15)<<4);digitalWrite(CLOCK,LOW);digitalWrite(LATCH,LOW);
 for(int r=6;r>=0;r--)for(int b=7;b>=0;b--){digitalWrite(DATA,(byte>>b)&1);delayMicroseconds(5);digitalWrite(CLOCK,HIGH);delayMicroseconds(5);digitalWrite(CLOCK,LOW);delayMicroseconds(5);}
 digitalWrite(LATCH,HIGH);delayMicroseconds(5);digitalWrite(LATCH,LOW);
}
void setup(){
 digitalWrite(OE,HIGH);pinMode(OE,OUTPUT);digitalWrite(OE,HIGH);
 pinMode(DATA,OUTPUT);pinMode(CLOCK,OUTPUT);pinMode(LATCH,OUTPUT);
 digitalWrite(DATA,LOW);digitalWrite(CLOCK,LOW);digitalWrite(LATCH,LOW);sendPattern(0);digitalWrite(OE,LOW);
 Serial.begin(115200);engine.begin(millis());
 publishStatus(engine.position,engine.stroke,engine.target,engine.maximum,engine.stopped,engine.waiting,engine.cycles,sentFrames);
 startNetwork();Serial.println("SOLARSKIN STAND: autonomous, two-phase full-step; 25148 full steps = 50296 old halfsteps; 120 full steps/s");
}
void loop(){
 Command c;while(readCommand(c)){
  if(c.type=='s'){engine.stop();sendPattern(0);}
  else if(c.type=='r')engine.restart(millis());
  else if(c.type=='o'||c.type=='c')engine.choose(c.type=='o',millis());
  else if(c.type=='t'&&engine.stopped)engine.configure(c.steps,c.speed,millis());
 }
 if(engine.tick(millis(),micros()))sendPattern(engine.output);
 static uint32_t report=0;if((uint32_t)(millis()-report)>=100){report=millis();publishStatus(engine.position,engine.stroke,engine.target,engine.maximum,engine.stopped,engine.waiting,engine.cycles,sentFrames);}
 if(engine.stopped||engine.waiting)delay(1);else delayMicroseconds(40);
}
