#pragma once
#include <stdint.h>
#include <math.h>
#include <stdlib.h>
// Full steps, two phases ON; one full step is two old half-step units.
struct Engine {
 static constexpr int32_t DEFAULT_STROKE=25148,MAX_STROKE=50296;
 int32_t position=0,stroke=DEFAULT_STROKE,target=DEFAULT_STROKE;
 float maximum=120,rate=20;uint8_t phase=0,output=0;
 bool stopped=false,waiting=true;uint32_t deadline=0,next=0,last=0,cycles=0;
 void begin(uint32_t ms){deadline=ms+3000;}
 void restart(uint32_t ms){stopped=false;waiting=true;deadline=ms+300;rate=20;target=position>=stroke?0:stroke;}
 void stop(){stopped=true;output=0;}
 void choose(bool opening,uint32_t ms){restart(ms);target=opening?stroke:0;if(target==position)target=position==0?stroke:0;}
 bool configure(int32_t steps,int speed,uint32_t ms){
  if(steps<100||steps>MAX_STROKE||steps<position||speed<20||speed>180)return false;
  stroke=steps;maximum=speed;restart(ms);return true;
 }
 bool tick(uint32_t ms,uint32_t us){
  if(stopped)return false;
  if(waiting){if((int32_t)(ms-deadline)<0)return false;waiting=false;rate=20;last=next=us;}
  if((int32_t)(us-next)<0)return false;
  int32_t remaining=target-position;if(!remaining)return false;
  float dt=(uint32_t)(us-last)*.000001f;last=us;
  rate=fminf(maximum,fminf(rate+40.f*dt,fmaxf(20.f,sqrtf(80.f*abs(remaining)))));
  int direction=remaining>0?1:-1;phase=(phase+(direction>0?1:3))&3;
  static const uint8_t phases[4]={3,6,12,9};output=phases[phase];position+=direction;
  next=us+(uint32_t)(1000000.f/rate);
  if(position==target){if(position==0)cycles++;target=position==0?stroke:0;waiting=true;deadline=ms+300;}
  return true;
 }
};
