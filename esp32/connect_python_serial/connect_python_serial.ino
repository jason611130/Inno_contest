void setup() {
  Serial.begin(115200);
  
}
 
void loop() {
  if(Serial.read()=='O'){
      Serial.println("ON");
      digitalWrite(2,HIGH);
      // delay(10);
  }
  else if(Serial.read()=='X'){
    Serial.println("OFF");
    digitalWrite(2,LOW);
    // delay(10);
  }
}