#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <Servo.h>

#define disc0 2
#define disc1 3
#define servopin0 7

Servo servo0;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

double new_emissivity = 0.35;
int baselineTemp = 34;
int celsius = 0;
int fahrenheit = 0;

// SDA 4
// SCL 5

void setup()
{
  Serial.begin(9600);
  mlx.begin(); 
  mlx.writeEmissivity(new_emissivity); 
  servo0.attach(servopin0);
  pinMode(7, OUTPUT);
  pinMode(disc0, INPUT_PULLUP);
  pinMode(disc1, INPUT_PULLUP);
  
}

void loop()
{
  float tempObject = mlx.readObjectTempC();
  float tempAmbient = mlx.readAmbientTempC();
  
  fahrenheit = ((tempObject * 9) / 5 + 32);
  Serial.print(tempObject);
  Serial.print(" C, ");
  Serial.print(fahrenheit);
  Serial.println(" F");
  
  if (tempObject < baselineTemp) {
    servo0.write(180);
    //Serial.println("180");

  }
  if (tempObject > baselineTemp + 1) {

    //Unlock Servo
    servo0.write(100);
    Serial.println("100");
    digitalWrite(7, HIGH);
    delay(50);
    digitalWrite(7, LOW);

    for (int count = 0; count < 30; count++) {
      byte discState0 = digitalRead(disc0);
      byte discState1 = digitalRead(disc1);
      
      //Disc0 Contact
      if (discState0 == LOW) {
          Serial.println("Disc0 rotated");
          break;
      }
      
      //Disc1 Non-contact
      else if (discState1 == HIGH){
          //Button is not pressed
      }
      
      //Disc1 Contact
      if (discState1 == LOW) {
          Serial.println("Disc1 rotated");
          break;
      }
      //Disc0 Non-contact
      else if (discState0 == HIGH){
          //Button is not pressed
      
      }
      delay(100);
    }
  }
  delay(500); 
}
