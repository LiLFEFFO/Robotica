// Pin motore sinistro
#define ENA 9
#define IN1 8
#define IN2 7

// Pin motore destro
#define ENB 10
#define IN3 6
#define IN4 5

String comando = "";
int velocita = 150;     // regola la velocità (0–255)

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotori();
}

void loop() {

  // Controllo se arrivano dati dal Raspberry
  if (Serial.available() > 0) {
    comando = Serial.readStringUntil('\n');
    comando.trim();    // rimuove spazi o \r\n

    Serial.print("Ricevuto: ");
    Serial.println(comando);

    // Interpretazione comandi
    if (comando == "CENTRO") {
      avanti();
    }
    else if (comando == "DESTRA") {
      destra();
    }
    else if (comando == "SINISTRA") {
      sinistra();
    }
    else {
      stopMotori();
    }
  }
}


// === FUNZIONI DI MOVIMENTO ===

void avanti() {
  // motore sinistro avanti
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  // motore destro avanti
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, velocita);
  analogWrite(ENB, velocita);
}

void destra() {
  // gira a destra: sinistro avanti, destro fermo o indietro
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);  // destro indietro per una curva più stretta

  analogWrite(ENA, velocita);
  analogWrite(ENB, velocita);
}

void sinistra() {
  // gira a sinistra: destro avanti, sinistro fermo o indietro
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);  // sinistro indietro

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, velocita);
  analogWrite(ENB, velocita);
}

void stopMotori() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
