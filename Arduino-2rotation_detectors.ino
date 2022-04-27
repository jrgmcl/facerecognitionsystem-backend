#define BUTTON_PIN0 2
#define BUTTON_PIN1 3
void setup()
{
  Serial.begin(9600);
  pinMode(BUTTON_PIN0, INPUT_PULLUP);
  pinMode(BUTTON_PIN1, INPUT_PULLUP);
}
void loop()
{
  //30 Counts = 3 Seconds window
  for (int count = 0; count < 30; count++) {
    byte buttonState0 = digitalRead(BUTTON_PIN0);
    byte buttonState1 = digitalRead(BUTTON_PIN1);
    
    //Button0 Contact
  	if (buttonState0 == LOW) {
      	Serial.println("Button0 is pressed"); break;
  	}
    
    //Button1 Non-contact
  	else if (buttonState1 == HIGH){
      	//Button is not pressed
  	}
    
    //Button1 Contact
  	if (buttonState1 == LOW) {
      	Serial.println("Button1 is pressed"); break;
  	}
    //Button0 Non-contact
  	else if (buttonState0 == HIGH){
      	//Button is not pressed
		
  	}
    Serial.println(count);
    delay(100);
  }
  Serial.println("-----------3 Second passed-----------");
}
