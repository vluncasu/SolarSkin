#pragma once
#if __has_include("solarskin_config.h")
#include "solarskin_config.h"
#else
#include "config.example.h"
#endif
#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <freertos/queue.h>
#include "ui.h"
struct Command{char type;int32_t steps;int speed;};
struct Snapshot{int32_t position,stroke,target;int speed;bool stopped,waiting;uint32_t cycles,frames,uptime;};
Snapshot snapshot{};portMUX_TYPE snapshotLock=portMUX_INITIALIZER_UNLOCKED;
QueueHandle_t queue=nullptr;WebServer server(80);
void publishStatus(int32_t p,int32_t stroke,int32_t target,int speed,bool stopped,bool waiting,uint32_t cycles,uint32_t frames){portENTER_CRITICAL(&snapshotLock);snapshot={p,stroke,target,speed,stopped,waiting,cycles,frames,millis()/1000};portEXIT_CRITICAL(&snapshotLock);}
Snapshot readStatus(){portENTER_CRITICAL(&snapshotLock);Snapshot s=snapshot;portEXIT_CRITICAL(&snapshotLock);return s;}
bool readCommand(Command &c){return queue&&xQueueReceive(queue,&c,0)==pdTRUE;}
void submit(Command c){if(queue&&xQueueSend(queue,&c,0)==pdTRUE)server.send(202,"text/plain","Queued");else server.send(503,"text/plain","Please retry");}
void networkTask(void*){
 WiFi.setHostname("solarskin2");WiFi.mode(WIFI_AP);WiFi.setSleep(false);
 WiFi.softAPConfig(IPAddress(192,168,4,1),IPAddress(192,168,4,1),IPAddress(255,255,255,0));
 bool ready=WiFi.softAP(SOLARSKIN_WIFI_NAME,SOLARSKIN_WIFI_PASSWORD);Serial.println(ready?"AP SolarSkin ready: http://192.168.4.1":"AP unavailable; autonomous motor loop continues");
 if(MDNS.begin("solarskin2"))MDNS.addService("http","tcp",80);
 server.on("/",HTTP_GET,[]{server.send_P(200,"text/html; charset=utf-8",PAGE);});
 server.on("/cmd",HTTP_POST,[]{String a=server.arg("a");char c=a=="stop"?'s':a=="resume"?'r':a=="open"?'o':a=="close"?'c':0;
  if(!c){server.send(400,"text/plain","Invalid command");return;}submit({c,0,0});});
 server.on("/settings",HTTP_POST,[]{int32_t steps=server.arg("steps").toInt();int speed=server.arg("speed").toInt();Snapshot s=readStatus();
  if(!s.stopped){server.send(409,"text/plain","Stop before changing settings.");return;}
  if(steps<100||steps>50296||steps<s.position||speed<20||speed>180){server.send(400,"text/plain","Stroke: 100-50296 full steps, at least the current position. Rate: 20-180. Close first before reducing travel.");return;}
  submit({'t',steps,speed});});
 server.on("/status",HTTP_GET,[]{Snapshot s=readStatus();String j="{\"position\":"+String(s.position)+",\"stroke\":"+String(s.stroke)+",\"target\":"+String(s.target)+",\"speed\":"+String(s.speed)+",\"stopped\":"+String(s.stopped?"true":"false")+",\"waiting\":"+String(s.waiting?"true":"false")+",\"cycles\":"+String(s.cycles)+",\"frames\":"+String(s.frames)+",\"uptime\":"+String(s.uptime)+"}";server.send(200,"application/json",j);});
 server.begin();for(;;){server.handleClient();vTaskDelay(pdMS_TO_TICKS(2));}
}
void startNetwork(){queue=xQueueCreate(8,sizeof(Command));if(xTaskCreatePinnedToCore(networkTask,"network",8192,nullptr,1,nullptr,0)!=pdPASS)Serial.println("Network task unavailable; motor loop independent");}
