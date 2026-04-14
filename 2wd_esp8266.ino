#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";

ESP8266WebServer server(80);

// Motor Pins
#define IN1 D1  // Left Motor
#define IN2 D2
#define IN3 D3  // Right Motor
#define IN4 D4

// ===== MOVEMENT FUNCTIONS =====

void forward(){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void left(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void right(){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopBot(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

// ===== SERVER HANDLER =====

void handleControl(){
  String cmd = server.arg("cmd");

  if(cmd == "FWD") forward();
  else if(cmd == "BACK") backward();
  else if(cmd == "LEFT") left();
  else if(cmd == "RIGHT") right();
  else stopBot();

  server.send(200, "text/plain", "OK");
}

// ===== SETUP =====

void setup(){
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopBot();

  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
  }

  server.on("/control", handleControl);
  server.begin();
}

// ===== LOOP =====

void loop(){
  server.handleClient();
}