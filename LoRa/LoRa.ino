#include <MKRWAN.h>
// #include <RBD_LightSensor.h>
#include <ArduinoLowPower.h>
#include <SimpleDHT.h>
#include <Ultrasonic.h>
// #include "arduino_secrets.h"

LoRaModem modem;
// RBD::LightSensor light_sensor(A2);
int pinDHT11 = A1;
SimpleDHT11 dht11(pinDHT11);
int triggerPin = A2;
int echoPin = 2;
Ultrasonic ultrasonic(triggerPin, echoPin);
typedef struct
{
  uint8_t temp;
  uint8_t hum;
  uint8_t phot;
//   uint8_t batt;

} LoraMessage;

String appEui = "a8610a3037266b08";
String appKey = "00000000000000000000000000000000000000";

void setup() {
  Serial.begin(9600);
  while(!Serial){}

  if(!modem.begin(EU868)){
    Serial.println("Ha fallado algo!!");
    return;
    }

  int connected = modem.joinABP(modem.deviceEUI(), appEui, appKey);  
  delay(100);

}

void loop() {
  LoraMessage msg;
  // start working...
  Serial.println("=================================");
  Serial.println("Sample DHT11...");
  
  // read without samples.
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.print(SimpleDHTErrCode(err));
    Serial.print(","); Serial.println(SimpleDHTErrDuration(err)); delay(1000);
    return;
  }
  
  Serial.print("Sample OK: ");
  msg.temp = (uint8_t)temperature;
  Serial.print(msg.temp); Serial.print(" C, "); 
  msg.hum = (uint8_t)humidity;
  Serial.print(msg.hum); Serial.println(" H");
 
  Serial.println(" ");
  Serial.println("Sample Ultrasonic...");
//   msg.phot = (uint8_t)light_sensor.getInversePercentValue ();
//   Serial.println(msg.phot); Serial.println(" %");
  Serial.print(ultrasonic.read(CM)); Serial.print(" cm");
  Serial.println(" ");
  // delay(1500);
  enviar(msg);

  delay(1000 * 1);
}

void enviar(LoraMessage msg){

  Serial.println("Empezando paquete...");
  modem.beginPacket();
  delay(100);
  modem.write((uint8_t*)&msg, sizeof(msg));
  Serial.println("Enviando... ");
  modem.endPacket(true);
  Serial.print("Hecho!!");
  }
