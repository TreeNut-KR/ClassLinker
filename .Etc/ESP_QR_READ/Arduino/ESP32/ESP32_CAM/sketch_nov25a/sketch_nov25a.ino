// ESP32 code
#define RXD2 25
#define TXD2 27

void setup() {
  // Note the format for setting a serial port is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
  Serial.println("Serial Txd is on pin: "+String(TX));
  Serial.println("Serial Rxd is on pin: "+String(RX));
}

void loop() { //Choose Serial1 or Serial2 as required
  while (Serial2.available()) {
    String barcode_Data = Serial2.readStringUntil('\n');
    Serial.print("read : ");
    Serial.println(barcode_Data);
  }
  delay(20);
}
