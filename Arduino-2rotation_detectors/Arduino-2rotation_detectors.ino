#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <Servo.h>

#define disc0 2
#define disc1 3

#define servopin0 7
#define servopin1 8

#define speaker0 9
#define speaker0 10


double new_emissivity = 0.35;
int baselineTemp = 34;
int celsius = 0;
int fahrenheit = 0;
bool temp = false;


void setup()
{
  Serial.begin(9600);
  mlx.begin(); 
  mlx.writeEmissivity(new_emissivity); 
  servo0.attach(servopin0);
  servo1.attach(servopin1);
  pinMode(disc0, INPUT_PULLUP);
  pinMode(disc1, INPUT_PULLUP);
  pinMode(speaker0, OUTPUT);
}

void loop()
{
  String data = Serial.readStringUntil('\n');

  if (data == 'unlock0'){
    float tempObject = mlx.readObjectTempC();
    float tempAmbient = mlx.readAmbientTempC();

    for (int count = 0; count < 30; count++) {
      byte discState0 = digitalRead(disc0);

      if (tempObject < baselineTemp) {
        servo0.write(180);
      }
      else if (tempObject > baselineTemp + 1) {
        //Unlock Servo
        Serial.println (tempObject);
        servo0.write(100);
        digitalWrite(speaker0, HIGH);
        delay(50);
        digitalWrite(speaker0, LOW);
        for (int count = 0; count < 30; count++){
          //Lock
          if (discState0 > 0){
            servo0.write(180);
            Serial.println("unlocked0");
            break;
          }
        }
          delay(100);
        break;
      }
      delay(100);
    }

  else if (data == 'unlock1'){
    //Unlock
    servo1.write(180);
    for (int count = 0; count < 30; count++) {
      byte discState1 = digitalRead(disc1);

      //Lock
      if (discState1 > 0)
        servo0.write(100);
        Serial.println("unlocked1");
        break;
      }
      delay(100);
    }
}