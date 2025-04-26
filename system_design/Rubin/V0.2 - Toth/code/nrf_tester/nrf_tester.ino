// this is uploaded on the dummy arduino I used for testing.
#include<SPI.h>                   // spi library for connecting nrf
#include <Wire.h>                 // i2c libary fro 16x2 lcd display
#include<RF24.h>                  // nrf library


RF24 radio(9, 10) ;  // ce, csn pins
static byte signs[1][16] = {{0x54,0x41,0x4b,0x45,0x50,0x49,0x43,0xc2,0xa9,0x6b,0xc2,0xa7,0xd,0xc2,0x9d,0x68}};
int count = 0;
void setup(void) {
//  SPI.begin();
//  SPI.setBitOrder(MSBFIRST);
  radio.begin(); // start radio at ce csn pin 9 and 10
  Serial.begin(9600) ; // start serial monitor baud rate
  Serial.println("Starting.. Setting Up.. Radio on.."); // debug message
  radio.setPALevel(RF24_PA_LOW); // set power level
  radio.setChannel(76); // set chanel at 76
  //const uint64_t pipes[2] = {0x43414d5241,0x5249564552};
  uint8_t pipes[][6] = {"CAMRA", "RIVER"};
  radio.openReadingPipe(0, pipes[0]); // start reading pipe
  radio.openWritingPipe(pipes[1]);
  radio.setPayloadSize(16);
  radio.powerUp();
}
void sendSign() {
//  Serial.println("within sendSign");
  radio.write(&signs[0], 16);
//  int i;
//  for (i = 0; i < 16; i++)
//  {
//    if (i > 0) Serial.print(":");
//    Serial.print(signs[0][i]);
//  }
//  Serial.print("\n");
}
void loop(void) {
  Serial.println("sign sent");
  sendSign();
  delay(10000);
  count ++;
  Serial.println(count);
}
