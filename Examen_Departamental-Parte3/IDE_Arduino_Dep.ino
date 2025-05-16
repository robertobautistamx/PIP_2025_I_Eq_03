#include <Servo.h>
int trigPin=3; //sensor ultrasonico
int echoPin=4;

//servomotor
int servoPin = 6;
Servo miServo;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  miServo.attach(servoPin);
  miServo.write(90);
}

long leerDistancia() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duracion = pulseIn(echoPin, HIGH, 30000); // 30 ms
  if (duracion==0) return 500;

  long distancia = duracion * 0.034 / 2;
  return distancia;
}

void loop() {
  //activar manual
  if (Serial.available()) {
    String comando=Serial.readStringUntil('\n');
    int separador=comando.indexOf('@');
    if (separador!=-1) {
      int indice=comando.substring(0, separador).toInt();
      int valor=comando.substring(separador + 1).toInt();

      if (indice == 0) {
        Serial.print("Ejecutando actuador ");
        Serial.print(indice);
        Serial.print(" durante ");
        Serial.print(valor);
        Serial.println(" ms");

        miServo.write(180);
        delay(valor);
        miServo.write(90);
      }
    }
  }
  long distancia = leerDistancia();
  Serial.print("Distancia: ");
  Serial.print(distancia);
  Serial.println(" cm");

  delay(500);
}
