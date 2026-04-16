#define BLYNK_TEMPLATE_ID "TMPL3YugwY8Wk"
#define BLYNK_TEMPLATE_NAME "ASTRA"
#define BLYNK_AUTH_TOKEN "l6NUfEJvhtnACBZBAN310UcQ0oEEUZ6U"

#define BLYNK_PRINT Serial

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

// 🔐 WiFi Credentials
char ssid[] = "Techno Mortals";
char pass[] = "87654321";

// 🔁 DEVICE TYPE
// 1 = INLET, 2 = OUTLET
#define DEVICE_TYPE 1

// 📌 Flow Sensor Pin
#define FLOW_PIN D2

volatile int pulseCount = 0;
float flowRate = 0;

BlynkTimer timer;

// Interrupt
void ICACHE_RAM_ATTR pulseCounter() {
  pulseCount++;
}

// Flow calculation
void calculateFlow() {
  flowRate = pulseCount / 7.5;
  pulseCount = 0;

  // Send based on device type
  if (DEVICE_TYPE == 1) {
    Blynk.virtualWrite(V0, flowRate); // Inlet
  } else {
    Blynk.virtualWrite(V1, flowRate); // Outlet
  }

  Serial.print("Flow: ");
  Serial.println(flowRate);
}

void setup() {
  Serial.begin(115200);

  pinMode(FLOW_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), pulseCounter, FALLING);

  // Connect to Blynk
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  timer.setInterval(1000L, calculateFlow);
}

void loop() {
  Blynk.run();
  timer.run();
}