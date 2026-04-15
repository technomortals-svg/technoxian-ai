#define BLYNK_PRINT Serial

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char auth[] = "YOUR_BLYNK_TOKEN";
char ssid[] = "YOUR_WIFI";
char pass[] = "YOUR_PASS";

#define TRIG D5
#define ECHO D6
#define GAS A0

BlynkTimer timer;

long duration;
int distance;
int gasValue;
float riskScore;

// Ultrasonic
int getDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  duration = pulseIn(ECHO, HIGH);
  return duration * 0.034 / 2;
}

// AI Logic (Improved)
void calculateRisk() {
  float distanceFactor = constrain(map(distance, 5, 50, 50, 0), 0, 50);
  float gasFactor = constrain(map(gasValue, 200, 800, 0, 50), 0, 50);

  // Weighted + smoothing
  riskScore = (distanceFactor * 0.6) + (gasFactor * 0.4);
}

// Send Data
void sendData() {
  distance = getDistance();
  gasValue = analogRead(GAS);

  calculateRisk();

  Blynk.virtualWrite(V0, distance);
  Blynk.virtualWrite(V1, gasValue);
  Blynk.virtualWrite(V2, riskScore);

  // Alert only
  if (riskScore > 60) {
    Blynk.virtualWrite(V3, 1);
  } else {
    Blynk.virtualWrite(V3, 0);
  }

  // Debug
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" Gas: ");
  Serial.print(gasValue);
  Serial.print(" Risk: ");
  Serial.println(riskScore);
}

void setup() {
  Serial.begin(115200);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Blynk.begin(auth, ssid, pass);

  timer.setInterval(2000L, sendData);
}

void loop() {
  Blynk.run();
  timer.run();
}