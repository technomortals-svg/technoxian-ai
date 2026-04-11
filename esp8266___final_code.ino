#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";

ESP8266WebServer server(80);

// Motor pins
#define IN1 D1
#define IN2 D2
#define IN3 D3
#define IN4 D4

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void left() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void right() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void stopBot() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

void handleControl() {
  String cmd = server.arg("cmd");

  if (cmd == "FWD") forward();
  else if (cmd == "LEFT") left();
  else if (cmd == "RIGHT") right();
  else stopBot();

  server.send(200, "text/plain", "OK");
}

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) delay(500);

  Serial.begin(115200);
  Serial.println(WiFi.localIP());

  server.on("/control", handleControl);
  server.begin();
}

void loop() {
  server.handleClient();
}
