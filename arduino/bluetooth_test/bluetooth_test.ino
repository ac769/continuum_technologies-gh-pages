int counter =0;

void setup() {
  Serial.begin(9600); 
}

void loop() {
  counter++;
  int sensorValue = analogRead(A0);
  Serial.print("Arduino: ");
  Serial.println(sensorValue);
  delay(50); // wait half a sec
}
