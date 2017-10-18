void setup() {
  Serial.begin(115200);
}

void loop() {
  byte sensorValue = analogRead(A1);
  byte angle = -3.91 * sensorValue + 990;
  Serial.write(angle);
  delay(200);
  }
