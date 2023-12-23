#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#define LED D5
#define ERRORLED D1
#define CO2_TX D3
#define CO2_RX D2

const char* ssid = "U+Net5B5C";
const char* password = "0D00212GA@";

String room = "L23";
String qrcode;
char str; 

SoftwareSerial gtSerial(CO2_RX, CO2_TX); // RX, TX

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(ERRORLED, OUTPUT);
  delay(10);
  digitalWrite(LED, LOW);
  digitalWrite(ERRORLED, HIGH);
  
  Serial.begin(115200);
  gtSerial.begin(9600);  // software serial port  
  delay(10);
  
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("."); 
     delay(500);
  }
  digitalWrite(ERRORLED, LOW);
  digitalWrite(LED, HIGH);
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print(WiFi.localIP());
  Serial.println("");
  long rssi = WiFi.RSSI();
  Serial.print("Signal (RSSI): ");
  Serial.print(rssi);
  Serial.println(" dBm");
  Serial.println("");
  delay(1000);
  digitalWrite(LED, LOW);
}
 
void loop() {
  while (gtSerial.available()>0){
    char str = gtSerial.read();
    qrcode = qrcode + str;
    if(str=='\n' || str=='\r'){
      qrcode.trim();
      if(qrcode.length() > 0){
        Serial.println(qrcode);
        sendPost(qrcode);
        qrcode = "";
      }
    }
  }
}

void sendPost(String qrCode) {
  if(WiFi.status()== WL_CONNECTED){
    WiFiClient client;
    HTTPClient http;  
    http.begin(client, "http://192.168.219.105:5100/QR");  
    http.addHeader("Content-Type", "application/json");   
    String postMessage = "{\"qrcode\":\"" + qrCode + "\"}";  
    int httpResponseCode = http.POST(postMessage);   

    if(httpResponseCode>0){
      String response = http.getString();  
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Error in WiFi connection");   
  }
}
