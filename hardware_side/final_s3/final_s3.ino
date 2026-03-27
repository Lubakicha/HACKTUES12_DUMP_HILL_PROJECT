#include <WiFi.h>
#include <SPI.h>
#include <RadioLib.h>
#include <HTTPClient.h>

// ESP32-S3 Zero
#define PIN_CSN   7
#define PIN_GDO0  6
#define PIN_GDO2  5
#define PIN_SCK   12
#define PIN_MISO  13
#define PIN_MOSI  11

const char* device_id="ABCDE";
const char* ssid = "Home45"; 
const char* password = "ObichamNikola";
const char* server = "http://192.168.43.213:8000/receive";

CC1101 radio=new Module(PIN_CSN, PIN_GDO0, RADIOLIB_NC, PIN_GDO2);
uint8_t buf[64];

void wifi_ON() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);   
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(200);
  }
  Serial.println();
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void send_json(const char* distanceStr) {
  HTTPClient http;

  http.begin(server);
  http.addHeader("Content-Type", "application/json");

  String json = "{\"device_id\":\"";
  json += device_id;
  json += "\",\"distance\":";
  json += distanceStr;
  json += "}";
  Serial.print("POST JSON: ");
  Serial.println(json);

  int httpCode = http.POST(json);
  Serial.print("HTTP Response: ");
  Serial.println(httpCode);

  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  wifi_ON();

  SPI.begin(PIN_SCK, PIN_MISO, PIN_MOSI, PIN_CSN);

  int state = radio.begin(433.92, 4.8, 5.0, 135.0, 10, 16);
  Serial.print("radio.begin: ");
  Serial.println(state);

  if (state != RADIOLIB_ERR_NONE) {
    Serial.println("RX init problem");
    while (true) delay(100);
  }

  state = radio.setSyncWord(0x12, 0x34);
  Serial.print("syncWord: ");
  Serial.println(state);

  Serial.println("CC1101 RX ready");
}

void loop() {
  size_t len = sizeof(buf);
  int state = radio.receive(buf, len);

  if (state == RADIOLIB_ERR_NONE) {
    if (len < sizeof(buf)) {
      buf[len] = '\0';
    } else {
      buf[sizeof(buf) - 1] = '\0';
    }

    Serial.print("Received: ");
    Serial.println((char*)buf);
    send_json((char*)buf);
  } else if (state == RADIOLIB_ERR_RX_TIMEOUT) {
    Serial.println("RX timeout");
  } else {
    Serial.print("RX error: ");
    Serial.println(state);
  }

  delay(100);
}