#include<Servo.h> 

Servo myservo; 
int servoPin = 12;
int centerPos = 90;  // 중앙 위치
int moveDegree = 27;  // 움직일 각도

void setup() 
{ 
  myservo.attach(servoPin); 
  Serial.begin(9600);  // 시리얼 통신 시작
  myservo.write(centerPos);  // 처음에 서보 모터를 중앙 위치로
} 

void loop() 
{ 
  if (Serial.available()) {  // 시리얼 통신으로 데이터가 들어올 경우
    char ch = Serial.read();
    if (ch == '1') {  // '1'이라는 신호가 들어올 경우
      myservo.write(centerPos - moveDegree);  // 중앙 위치에서 왼쪽으로 35도
    } else if (ch == '0' or '2') {  // '0', '2'이라는 신호가 들어올 경우
      myservo.write(centerPos + moveDegree+10);  // 중앙 위치에서 오른쪽으로 35도
    }
  }
}
