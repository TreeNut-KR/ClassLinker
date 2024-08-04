#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"
#include <Adafruit_SSD1306.h>  // SSD1306 디스플레이 라이브러리
#include "U8x8lib.h"  // U8x8lib 라이브러리
#include "TYPE1SC.h"  // TYPE1SC 라이브러리

#define DHTTYPE DHT22
#define DHTPIN 0

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "IDF18 AP3_2.4G";
const char* password = "center#3121!";

const char* serverIP = "192.168.1.17"; // Flask 서버의 IP 주소
const int serverPort = 5000; // Flask 서버의 포트 번호
const char* endpoint = "/data"; // Flask 서버의 엔드포인트 경로

WiFiClient client;

// SSD1306 디스플레이 설정
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* reset=*/U8X8_PIN_NONE);
TYPE1SC TYPE1SC(Serial, Serial, 0, 0, 0); // 수정된 부분

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  dht.begin();

  // SSD1306 디스플레이 초기화
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }

  // 디스플레이 초기화 메시지 출력
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Display Initialized");
  display.display();
  delay(2000);
  display.clearDisplay();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + String(endpoint);

    http.begin(client, url);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String payload = "temperature=" + String(temperature) + "&humidity=" + String(humidity);
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode == 200) {
      Serial.println("Data sent successfully");

      // 디스플레이에 날짜, 온도, 습도, 전송 여부 출력
      display.clearDisplay();
      display.setTextColor(WHITE);
      display.setTextSize(1);
      display.setCursor(0, 0);
      display.print("Date: ");
      display.println(getCurrentDate());
      display.print("Temperature: ");
      display.print(temperature);
      display.println(" °C");
      display.print("Humidity: ");
      display.print(humidity);
      display.println(" %");
      display.print("Transmitted: ");
      display.println("OK");
      display.display();
    } else {
      Serial.print("Error sending data. HTTP response code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(5000); // 5초마다 데이터 전송
}

String getCurrentDate() {
  String dateStr = "";

  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return dateStr;
  }

  dateStr += (timeinfo.tm_year + 1900);
  dateStr += "-";
  if (timeinfo.tm_mon < 9) dateStr += "0";
  dateStr += (timeinfo.tm_mon + 1);
  dateStr += "-";
  if (timeinfo.tm_mday < 10) dateStr += "0";
  dateStr += timeinfo.tm_mday;

  return dateStr;
}
