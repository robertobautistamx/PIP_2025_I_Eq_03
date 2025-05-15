int v;
//instalar librería  DHT sensor library by Adafruit 

#include <Servo.h>
#include <DHT.h>
#define DHTTYPE DHT11

bool modoLuzAutomatico = true;
int sensores[] = {2, A0, 3, 4}; //Sensores digitales o analogicos: temperatura, luz, distancia: trigger y echo
int actuadores[] = {6, 11, 12}; //Poner los 3: servomotor, led, buzzer activo

// Objetos
Servo miServo;
DHT dht(sensores[0], DHTTYPE); //Sensor de temperatura y humedad

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  // Inicializar sensores
  dht.begin();
  pinMode(sensores[2], OUTPUT); //Distancia trigger
  pinMode(sensores[3], INPUT); //Distancia echo

  // Inicializar actuadores
  miServo.attach(actuadores[0]); //Servo
  pinMode(actuadores[1], OUTPUT); //LED
  pinMode(actuadores[2], OUTPUT); //Buzzer
  
}

float leerTemperatura() {
  return dht.readTemperature();  // Usa el objeto DHT para usar su metodo readTemperature()
}
int leerLuz() {
  return analogRead(sensores[1]);  // A0, no ocupa ninguna modificación
}

long leerDistancia() {
  digitalWrite(sensores[2], LOW);   // TRIG
  delayMicroseconds(2);
  digitalWrite(sensores[2], HIGH); //Enciende el pulso muy poco tiempo, 10 microsegundos
  delayMicroseconds(10);
  digitalWrite(sensores[2], LOW);
  //ECHO
  long duracion = pulseIn(sensores[3], HIGH, 30000); // ECHO,  30000 microsegundos = 30 milisegundos
  
  if (duracion == 0) { // No se detectó nada, retornar un valor alto, que se consideraria fuera del rango del sensor, y por ende de las graficas
    return 500; 
  }
  
  long distancia = duracion * 0.034 / 2; //Velocidad de sonido entre 2, ir y volver
  return distancia;
}
void moverServoTemporal(int angulo, int duracionMs) {
  miServo.write(angulo);
  delay(duracionMs);
  miServo.write(90); // Posición neutral
}
void beepBuzzer(int duracionMs) { // 500 = medio segundo prendido, medio segundo apagado
  for (int i = 0; i < 5; i++) 
  {
    digitalWrite(actuadores[2], HIGH); //Suena
    delay(duracionMs);
    digitalWrite(actuadores[2], LOW); //Se apaga
    delay(duracionMs);
  }
}


void loop() {

// Sensores, envia las lecturas a python en formato "lecturaTemp@lecturaLuz@lecturaDistancia@ "
//#Valores esperados: 0-50 grados celsius, 0-1023 de luz, y  0-400 cm de distancia aunque suele ser menor a 300 cm. 23@845@56

float temp = leerTemperatura();
int tempEntera = round(temp); // o simplemente: (int)temp
int luz = leerLuz();
long distancia = leerDistancia();


char cadena[40];
sprintf(cadena, "%d@%d@%ld@", tempEntera, luz, distancia);
Serial.println(cadena);

 // Verificar si la temperatura alcanza los grados y mover el servo
  if (tempEntera >= 30) { // Si la temperatura es igual o mayor a 30 grados
    moverServoTemporal(180, 1000); // Mueve el servo a 180° durante 1000 ms
  }

// Actuadores, recibe mensaje "numActuador@valor" desde python

  if (Serial.available() > 0) 
  {
    String comando = Serial.readStringUntil('\n');
    int separador = comando.indexOf('@');
    if (separador != -1) 
    {
      int indice = comando.substring(0, separador).toInt();
      int valor = comando.substring(separador + 1).toInt();

      switch (indice) 
      {
        case 0: // Servo
          moverServoTemporal(180, valor); // mueve a 180° grados durante x milisegundos
          break;
        case 1: // LED
          digitalWrite(actuadores[1], valor ? HIGH : LOW); // Prende o apaga el led segun el valor, maneja a 1 como true->HIGH y 0 como false->LOW
          break;
        case 2: // Buzzer
          beepBuzzer(valor); // usa 5 repeticiones  con x milisegundos de encendido y apagado
          break;
      }
    }
  }
  
  // Activar buzzer automaticamente si la distancia es menor o igual a 10 cm
  if (distancia <= 10) {
    digitalWrite(actuadores[2], HIGH);
  } else {
    digitalWrite(actuadores[2], LOW);
  }

  delay(100);
}
