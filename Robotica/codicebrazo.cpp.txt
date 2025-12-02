#include <Stepper.h>
#include <Servo.h>

const int stepsPerRevolution = 2450;
const int stepsFor200deg = 1137;

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
Servo myServo;

int servoStart = 200;   // posizione iniziale servo
int servoEnd = 30;   // posizione finale servo
unsigned long movementStart;
const unsigned long movementDuration = 1500; // durata "delay" in ms

bool movingClockwise = true;
bool servoMoving = false;

void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(15);
  myServo.attach(6); // pin del servo

  myServo.write(servoStart);  // imposta subito la posizione iniziale
  delay(20);                   // piccolo ritardo per far stabilizzare il servo

  Serial.println("Orario 200 gradi");
  myStepper.step(stepsFor200deg);

  // Inizio movimento servo nello spazio vuoto
  servoMoving = true;
  movementStart = millis();
}


void loop() {
  if (servoMoving) {
    unsigned long elapsed = millis() - movementStart;
    if (elapsed <= movementDuration) {
      // Movimento servo proporzionale al tempo trascorso
      int servoPos = map(elapsed, 0, movementDuration, servoStart, servoEnd);
      myServo.write(servoPos);
    } else {
      // Movimento finito
      servoMoving = false;
      myServo.write(servoEnd);
      Serial.println("Servo movimento completato");

      // Ora facciamo il passo antiorario dello stepper
      Serial.println("Antiorario 200 gradi");
      myStepper.step(-stepsFor200deg);

      Serial.println("FINITO");
    }
  }
}
