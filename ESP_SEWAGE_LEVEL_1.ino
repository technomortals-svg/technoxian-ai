#define BLYNK_PRINT Serial

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char auth[] = "YOUR_BLYNK_TOKEN";
char ssid[] = "YOUR_WIFI";
char pass[] = "YOUR_PASS";

#define FLOW_PIN D2

volatile int pulseCount = 0;
float flowRate = 0;

BlynkTimer timer;

void ICACHE_RAM_ATTR pulseCounter() {
  pulseCount++;
}

void calculateFlow() {
  flowRate = pulseCount / 7.5;  // L/min
  pulseCount = 0;

  Blynk.virtualWrite(V0, flowRate);
}

void setup() {
  Serial.begin(115200);

  pinMode(FLOW_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), pulseCounter, FALLING);

  Blynk.begin(auth, ssid, pass);

  timer.setInterval(1000L, calculateFlow);
}

void loop() {
  Blynk.run();
  timer.run();
}