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
struct Snapshot {int32_t position;uint32_t frames;int direction;bool stopped,waiting;};
Snapshot snapshot{};portMUX_TYPE snapshotLock=portMUX_INITIALIZER_UNLOCKED;
QueueHandle_t commandQueue;WebServer server(80);
void publishStatus(int32_t p,uint32_t f,int d,bool s,bool w){
 portENTER_CRITICAL(&snapshotLock);snapshot={p,f,d,s,w};portEXIT_CRITICAL(&snapshotLock);
}
char readCommand(){char c=0;if(commandQueue)xQueueReceive(commandQueue,&c,0);return c;}
const char PAGE[] PROGMEM=R"HTML(<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SolarSkin</title><style>body{font:18px system-ui;background:#101820;color:#f4f6f8;max-width:740px;margin:auto;padding:24px}h1{color:#ff943c}button{font:inherit;border:0;border-radius:10px;padding:14px;margin:5px;background:#ff943c;color:#111;cursor:pointer}.stop{background:#ef6060}.panel{background:#1e2c38;border-radius:16px;padding:20px;margin:18px 0}progress{width:100%;height:28px;accent-color:#ff943c}.grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}.motor{border:2px solid #597284;padding:10px 0;text-align:center;border-radius:8px}.moving{border-color:#ff943c}small{color:#b6c8d7}@media(max-width:500px){.grid{grid-template-columns:repeat(4,1fr)}}</style><h1>SolarSkin</h1><p>Continuous demo · 4 November baseline with controls</p><div class="panel"><h2 id="state">Connecting…</h2><progress id="bar" max="6287" value="0"></progress><p id="position"></p><button onclick="cmd('resume')">Resume continuous demo</button><button class="stop" onclick="cmd('stop')">STOP</button><p><button onclick="cmd('open')">Open now</button><button onclick="cmd('close')">Close now</button></p><small>Open/Close override direction; automatic cycling then continues. STOP stays active until Resume.</small></div><div class="panel"><div id="motors" class="grid"></div><p><small>All 14 channels receive the same phase. Indicators show commands, not measured rotation.</small></p></div><p><small>6,287 half-steps per direction · maximum 180 half-steps/s · 1-second endpoint pause. Starts without a phone or web page.</small></p><p><small>Startup assumes a closed mechanism. No homing or end sensors.</small></p><script>async function cmd(a){try{let r=await fetch('/cmd?a='+a,{method:'POST'});if(!r.ok)throw Error(await r.text())}catch(e){alert(e.message)}}async function update(){try{let r=await fetch('/status');if(!r.ok)throw Error();let s=await r.json();document.getElementById('state').textContent=s.stopped?'Stopped':s.waiting?'Endpoint pause':s.direction>0?'Opening':'Closing';document.getElementById('bar').value=s.position;document.getElementById('position').textContent='Commanded position: '+s.position+' / 6287 half-steps';document.getElementById('motors').innerHTML=Array.from({length:14},(_,i)=>'<div class="motor '+(!s.stopped&&!s.waiting?'moving':'')+'">M'+String(i+1).padStart(2,'0')+'</div>').join('')}catch(e){document.getElementById('state').textContent='Device disconnected'}setTimeout(update,1000)}update()</script></html>)HTML";
void networkTask(void*){
 WiFi.mode(WIFI_AP);WiFi.setSleep(false);
 WiFi.softAPConfig(IPAddress(192,168,4,1),IPAddress(192,168,4,1),IPAddress(255,255,255,0));
 bool ok=WiFi.softAP(SOLARSKIN_WIFI_NAME,SOLARSKIN_WIFI_PASSWORD);Serial.println(ok?"SolarSkin AP ready: 192.168.4.1":"WiFi unavailable; motor demo remains autonomous");
 if(MDNS.begin("solarskin2"))MDNS.addService("http","tcp",80);
 server.on("/",HTTP_GET,[]{server.send_P(200,"text/html; charset=utf-8",PAGE);});
 server.on("/cmd",HTTP_POST,[]{String a=server.arg("a");char c=a=="stop"?'s':a=="resume"?'r':a=="open"?'o':a=="close"?'c':0;
  if(!c){server.send(400,"text/plain","Invalid command");return;}
  if(commandQueue&&xQueueSend(commandQueue,&c,0)==pdTRUE)server.send(200,"text/plain","OK");else server.send(503,"text/plain","Please retry");});
 server.on("/status",HTTP_GET,[]{portENTER_CRITICAL(&snapshotLock);Snapshot s=snapshot;portEXIT_CRITICAL(&snapshotLock);
  String j="{\"position\":"+String(s.position)+",\"frames\":"+String(s.frames)+",\"direction\":"+String(s.direction)+",\"stopped\":"+String(s.stopped?"true":"false")+",\"waiting\":"+String(s.waiting?"true":"false")+"}";server.send(200,"application/json",j);});
 server.begin();for(;;){server.handleClient();vTaskDelay(pdMS_TO_TICKS(2));}
}
void startNetwork(){commandQueue=xQueueCreate(8,sizeof(char));xTaskCreatePinnedToCore(networkTask,"network",8192,nullptr,1,nullptr,0);}
