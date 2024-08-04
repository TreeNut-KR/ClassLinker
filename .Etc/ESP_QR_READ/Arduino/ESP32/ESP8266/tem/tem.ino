#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h> 
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>


#define DHTPIN D2          // DHT21 센서의 데이터 핀 번호
#define DHTTYPE DHT21     // 사용하는 DHT 센서의 타입

DHT_Unified dht(DHTPIN, DHTTYPE);

const char* ssid = "Aeon_2G";
const char* password = "Sjmbee04!";
const char* serverUrl = "http://122.45.4.113:5100/QR";

WiFiClient client;

bool isFirstLoop = true;  // 첫 번째 반복 여부를 나타내는 플래그

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  dht.begin();  // DHT 센서 초기화

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  isFirstLoop = true;  // isFirstLoop 변수 초기화
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    sensors_event_t event;
    dht.temperature().getEvent(&event);  // 온도 값 읽기
    float temperature = event.temperature;
    dht.humidity().getEvent(&event);     // 습도 값 읽기
    float humidity = event.relative_humidity;

    if (!isFirstLoop) {  // 첫 번째 반복이 아닌 경우에만 POST 요청을 보냄
      HTTPClient http;
      String url = serverUrl;

      http.begin(client, url);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");

      String httpRequestData = "temperature=" + String(temperature) + "&humidity=" + String(humidity);

      int httpCode = http.POST(httpRequestData);

      if (httpCode > 0) {
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);
      } else {
        Serial.println("Error on sending POST");
        Serial.println(httpCode);
      }

      http.end();
    }
    
    isFirstLoop = false;  // 첫 번째 반복이 끝났으므로 플래그를 false로 변경
  }
  
  delay(10000);
}
