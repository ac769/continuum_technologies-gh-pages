#include <Wire.h>
#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads1115;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Hello!");

  Serial.println("Getting differential reading from AIN0 (P) and AIN1 (N)");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 0.188mV)");
  ads1115.begin();

  ads1115.setGain(GAIN_TWOTHIRDS);
}

void loop() {
  // put your main code here, to run repeatedly:
  int16_t results1;
  int16_t results2;

  results1 = ads1115.readADC_Differential_0_1();
  results2 = ads1115.readADC_Differential_2_3();
  Serial.print("Differential #1: ");
  Serial.print(results1);
  Serial.print("(");
  Serial.print(results1 * 0.188);
  Serial.println("mV)");
  
  Serial.print("Differential #2: ");
  Serial.print(results2);
  Serial.print("(");
  Serial.print(results2 * 0.188);
  Serial.println("mV)");

  delay(1);
}
