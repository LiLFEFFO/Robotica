#define ENA 5
#define IN1 6
#define IN2 7
#define ENB 9
#define IN3 10
#define IN4 11

int leftSpeed = 0;
int rightSpeed = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      leftSpeed = data.substring(0, commaIndex).toInt();
      rightSpeed = data.substring(commaIndex + 1).toInt();
      driveMotors(leftSpeed, rightSpeed);
    }
  }
}

void driveMotors(int left, int right) {
  // Motore sinistro
  analogWrite(ENA, abs(left));
  digitalWrite(IN1, left >= 0);
  digitalWrite(IN2, left < 0);

  // Motore destro
  analogWrite(ENB, abs(right));
  digitalWrite(IN3, right >= 0);
  digitalWrite(IN4, right < 0);
}
