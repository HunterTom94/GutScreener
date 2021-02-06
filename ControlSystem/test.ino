void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, INPUT); 
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
  digitalWrite(5, LOW);
}


void stage(long seconds, bool on, bool clkwise) {
  bool clkwise_value;
  bool on_value;
  unsigned long currentMillis = millis();
  
  if (clkwise == true) {
    clkwise_value = LOW;
    }
    else {
      clkwise_value = HIGH;
      }
  if (on == true) {
    on_value = LOW;
    }
    else {
      on_value = HIGH;
      }
  
  while (millis() - currentMillis <=  seconds*1000) {
    digitalWrite(3, on_value);
    }
  digitalWrite(3, HIGH);
}

void loop() {
  if (digitalRead(6) == HIGH){
    digitalWrite(2, LOW);
    // (Integer: duration(seconds) for the stage,
    //  Boolean: pump is on,
    //  Boolean: clockwise)
////////////////////////////////////////////////////////////
    stage(30, true, true);
    stage(30, true, true);
    stage(31, false, true);
    stage(1, false, true);
    
    
////////////////////////////////////////////////////////////
    stage(1800, false, true);
    digitalWrite(2, HIGH);
    }
  
  
  
}
