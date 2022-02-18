// now working towards having the rPi and Arduino specifications working together. this sends TESTMSG once every 5 seconds, and turns on an led at the same time.
// the pi and arduino leds should blink in syncronicity.
#include<SPI.h>                   // spi library for connecting nrf
#include <Wire.h>                 // i2c libary fro 16x2 lcd display
#include<RF24.h>                  // nrf library


RF24 radio(9, 10) ;  // ce, csn pins
static byte signs[2][7] = {{'T', 'A', 'K', 'E', 'P', 'I', 'C'},
                           {'T', 'E', 'S', 'T', 'M', 'S', 'G'}}; //TAKEPIC, TESTMSG
int prevVal;
int count = 0;
int startTime;
void setup(void) {
//  SPI.begin();
//  SPI.setBitOrder(MSBFIRST);
  radio.begin(); // start radio at ce csn pin 9 and 10
  Serial.begin(9600) ; // start serial monitor baud rate
  Serial.println("Starting.. Setting Up.. Radio on.."); // debug message
  radio.setPALevel(RF24_PA_MIN); // set power level. one of RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
  radio.setChannel(76); // set chanel at 76
  //const uint64_t pipes[2] = {0x43414d5241,0x5249564552};
  uint8_t pipes[][6] = {"CAMRA", "RIVER"};
  radio.openReadingPipe(0, pipes[0]); // start reading pipe
  radio.openWritingPipe(pipes[1]);
  radio.setPayloadSize(16);
  radio.powerUp();

  pinMode(8, OUTPUT);
  pinMode(7, INPUT);
  prevVal = digitalRead(7);
}
void sendSign(int index) {
  radio.write(&signs[index], 7);
}
void loop(void) {
  int currentVal = digitalRead(7);
  int currentTime = millis();
  if(digitalRead(7) == 1 && prevVal == 0) {
    digitalWrite(8, 1);
    startTime = currentTime;
    sendSign(1);
    prevVal = 1;
    Serial.println("sending TESTMSG on switch");
  }
  if(digitalRead(7) == 0 && prevVal == 1) {
    digitalWrite(8,0);
    prevVal = 0;
  }
  if(currentVal == 1 && (currentTime - startTime) > 1000) {
    sendSign(0);
    startTime = currentTime;
    Serial.println("sending TAKEPIC after second");
  }
}
