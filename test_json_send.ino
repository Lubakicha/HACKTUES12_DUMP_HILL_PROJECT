#include<WiFi.h>
#include <HTTPClient.h>
#define trigPin  12
#define echoPin  14

const char* ssid = "Home45"; 
const char* password = "ObichamNikola";
const char* server ="http://192.168.1.50:5000/data";

float duration, distance;
HTTPClient http;


void initWiFi() {
 WiFi.mode(WIFI_STA);
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
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH,30000);
  distance = (duration*.0343)/2;
  Serial.print("Distance: ");
  Serial.println(distance);
  delay(100);
//send http
  http.begin(server);
  http.addHeader("Content-Type","application/json");

  String json =
    "{\"speed\":10,\"angle\":3}" +string(distance);

  http.POST(json);
  http.end();
}