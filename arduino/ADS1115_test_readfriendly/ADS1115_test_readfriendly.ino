#include <Wire.h>
#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads1115;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  ads1115.begin();
  ads1115.setGain(GAIN_TWOTHIRDS);
}

void loop() {
  // put your main code here, to run repeatedly:
  int16_t results1;

  results1 = ads1115.readADC_Differential_0_1();

  // this is in mV
  Serial.println(results1);
  delay(5);
}
