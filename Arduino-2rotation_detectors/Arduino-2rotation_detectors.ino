#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <Servo.h>

#define disc0 2
#define disc1 3

#define servopin0 7
#define servopin1 8

#define speaker0 10

Servo mservo0, mservo1;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

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
  mservo0.attach(servopin0);
  mservo1.attach(servopin1);
  pinMode(disc0, INPUT_PULLUP);
  pinMode(disc1, INPUT_PULLUP);
  pinMode(speaker0, OUTPUT);
}

void loop()
{
  String data = Serial.readStringUntil('\n');
  if (data == "5") {
    float tempObject = mlx.readObjectTempC();
    float tempAmbient = mlx.readAmbientTempC();
    mservo0.write(100);
    digitalWrite(speaker0, HIGH);
    delay(200);
    digitalWrite(speaker0, LOW);
    for (int count = 0; count < 30; count++) {
      Serial.println(tempObject);
      delay(100);
    }
    mservo0.write(180);
  }


  


  else if (data == "4"){
    mservo1.write(100);
    digitalWrite(speaker0, HIGH);
    delay(200);
    digitalWrite(speaker0, LOW);
    for (int count = 0; count < 30; count++) {
      
      delay(100);
    }
    
    mservo1.write(180);
  }
  else if (data == "6"){
    digitalWrite(speaker0, HIGH);
    delay(50);
    digitalWrite(speaker0, LOW);
    delay(50);
    digitalWrite(speaker0, HIGH);
    delay(50);
    digitalWrite(speaker0, LOW);
  }
  else{
    mservo0.write(180);
    mservo1.write(180);
  }
}
