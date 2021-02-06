void setup() {
  pinMode(2, OUTPUT); // Pump AUTO/MANUAL Control
  pinMode(3, OUTPUT); // Pump START/STOP Control
  pinMode(5, OUTPUT);
  pinMode(6, INPUT);  // Receive input from NI-DAQ
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  digitalWrite(5, LOW);
}

void loop() {
    if (digitalRead(6) == HIGH){
        digitalWrite(3, LOW);
    }
    else {
        digitalWrite(3, HIGH);
    }
}
