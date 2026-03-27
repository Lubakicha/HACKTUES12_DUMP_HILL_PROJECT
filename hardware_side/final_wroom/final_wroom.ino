#include <SPI.h>
#include <RadioLib.h>

// ESP32 WROOM
#define PIN_CSN   5
#define PIN_GDO0  4
#define PIN_GDO2  27
#define PIN_SCK   18
#define PIN_MISO  19
#define PIN_MOSI  23

#define trigPin 14
#define echoPin 12

float duration, distance;
CC1101 radio = new Module(PIN_CSN, PIN_GDO0, RADIOLIB_NC, PIN_GDO2);

void find_distance(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH,30000);
  distance = (duration*.0343)/2;
}


void setup() {
  //hypersonic setup
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  //radio setup
  Serial.begin(115200);
  delay(2000);
  Serial.println("TX starting...");

  SPI.begin(PIN_SCK, PIN_MISO, PIN_MOSI, PIN_CSN);

  int state = radio.begin(433.92, 4.8, 5.0, 135.0, 10, 16);
  Serial.print("radio.begin: ");
  Serial.println(state);

  if (state != RADIOLIB_ERR_NONE) {
    Serial.println("TX init problem");
    while (true) delay(100);
  }

  state = radio.setSyncWord(0x12, 0x34);
  Serial.print("syncWord: ");
  Serial.println(state);

  Serial.println("CC1101 TX ready");
}

void loop() {
find_distance();

  char msg[16];   
  snprintf(msg, sizeof(msg), "%.2f", distance);

  Serial.print("Sending: ");
  Serial.println(msg);
  Serial.print("Distance:");
  Serial.println(distance);
 radio.transmit((uint8_t*)msg, strlen(msg) + 1);

  

  delay(1000);
}