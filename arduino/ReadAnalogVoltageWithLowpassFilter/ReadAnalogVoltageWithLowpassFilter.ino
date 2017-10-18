/*
  ReadAnalogVoltage
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}
#define NZEROS 2
#define NPOLES 2
#define GAIN   7.485478157e+01

static float xv[NZEROS+1], yv[NPOLES+1];

// the loop routine runs over and over again forever:
void loop() {
  //filterloop();
  Serial.println(analogRead(A0));
  //Serial.println(3.0*(yv[NZEROS] - 3.0));
}

static void filterloop()
  {
  int sensorValue = analogRead(A0);
  float voltage = sensorValue * (5.0 / 1023.0);
      xv[0] = xv[1]; 
        xv[1] = voltage / GAIN;
        yv[0] = yv[1];
        yv[1] =   (xv[0] + xv[1])
                     + (  0.5095254495 * yv[0]);
  }

