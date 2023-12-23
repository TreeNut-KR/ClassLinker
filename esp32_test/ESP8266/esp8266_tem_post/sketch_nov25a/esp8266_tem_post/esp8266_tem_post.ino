#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "JeongOffice_2.4Ghz";
const char* password = "wjdantlf19";
const char* serverUrl = "http://192.168.219.101:5100//data";

WiFiClient client;

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

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    
    // generate fake temperature and humidity data
    float temperature = random(20, 30);
    float humidity = random(40, 60);
    
    // create the url for the POST request
    String url = serverUrl;
    url += "?temperature=" + String(temperature);
    url += "&humidity=" + String(humidity);
    http.begin(client, url);
    int httpCode = http.POST("");

    // check the returning code                                                                  
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
  delay(10000);  // send data every 10 seconds
}
