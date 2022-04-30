#define disc0 2
#define disc1 3
void setup()
{
  Serial.begin(9600);
  pinMode(disc0, INPUT_PULLUP);
  pinMode(disc1, INPUT_PULLUP);
}
void loop()
{
  //30 Counts = 3 Second window
  for (int count = 0; count < 30; count++) {
    byte discState0 = digitalRead(disc0);
    byte discState1 = digitalRead(disc1);
    
    //Button0 Contact
  	if (discState0 == LOW) {
      	Serial.println("Button0 is pressed"); break;
  	}
    
    //Button1 Non-contact
  	else if (discState1 == HIGH){
      	//Button is not pressed
  	}
    
    //Button1 Contact
  	if (discState1 == LOW) {
      	Serial.println("Button1 is pressed"); break;
  	}
    //Button0 Non-contact
  	else if (discState0 == HIGH){
      	//Button is not pressed
		
  	}
    Serial.print("|");
    delay(100);
  }
  
  for (int i=0; i<8; i++){
    Serial.println("");
  }
  Serial.println("--------3 Second passed--------");
}
