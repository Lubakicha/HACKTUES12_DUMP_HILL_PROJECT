#include <WiFi.h>

//  network credentials
const char* ssid = "Home45"; 
const char* password = "ObichamNikola";

void initWiFi() {
 WiFi.mode(WIFI_STA);    //Set Wi-Fi Mode as station
 WiFi.begin(ssid, password);   
 
 Serial.println("Connecting to WiFi ..");
 while (WiFi.status() != WL_CONNECTED) {
   Serial.print('.');
   delay(1000);
 }
 
 Serial.println(WiFi.localIP());
 Serial.print("RRSI: ");
 Serial.println(WiFi.RSSI());
}

void setup() {
 Serial.begin(9600);
 initWiFi();
}

void loop() {
 // put your main code here, to run repeatedly:
}