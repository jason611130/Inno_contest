#include <Wire.h>
#include "Adafruit_SGP30.h"
#include <SimpleDHT.h>

Adafruit_SGP30 sgp;

/* return absolute humidity [mg/m^3] with approximation formula
* @param temperature [°C]
* @param humidity [%RH]
*/
uint32_t getAbsoluteHumidity(float temperature, float humidity) {
    // approximation formula from Sensirion SGP30 Driver Integration chapter 3.15
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
    return absoluteHumidityScaled;
}
int pinDHT11 = 15;
SimpleDHT11 dht11(pinDHT11);

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); } // Wait for serial console to open!
  pinMode( 2 , OUTPUT );
  Serial.println("SGP30 test");

  if (! sgp.begin()){
    Serial.println("Sensor not found :(");
    while (1);
  }
  Serial.print("Found SGP30 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);

  // If you have a baseline measurement from before you can assign it to start, to 'self-calibrate'
  //sgp.setIAQBaseline(0x8E68, 0x8F41);  // Will vary for each sensor!
}

int counter = 0;
int char_OX = '1';
void loop() {
  // If you have a temperature / humidity sensor, you can set the absolute humidity to enable the humditiy compensation for the air quality signals
  //float temperature = 22.1; // [°C]
  //float humidity = 45.2; // [%RH]
  //sgp.setHumidity(getAbsoluteHumidity(temperature, humidity));

  byte temperature = 0;
  byte humidity = 0;
  
  char_OX =Serial.read() ; 
  if(char_OX=='O'||char_OX=='X'){
    if(char_OX=='O'){
      digitalWrite(2,HIGH);
    }
    else{
      digitalWrite(2,LOW);
    }
    int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.print(SimpleDHTErrCode(err));
    Serial.print(","); Serial.println(SimpleDHTErrDuration(err)); delay(1000);
    return;
  }
  
  // Serial.print("Sample OK: ");
  Serial.print("temp= "); 
  Serial.print((int)temperature);
  Serial.print(" humidity= ");
  Serial.print((int)humidity); 
  if (! sgp.IAQmeasure()) {
    Serial.println("Measurement failed");
    return;
  }
  // Serial.print("TVOC "); Serial.print(sgp.TVOC); Serial.print(" ppb\t");
  Serial.print(" eCO2 "); Serial.print(sgp.eCO2); Serial.println(" ppm");

  if (! sgp.IAQmeasureRaw()) {
    Serial.println("Raw Measurement failed");
    return;
  }
  // Serial.print("Raw H2 "); Serial.print(sgp.rawH2); Serial.print(" \t");
  // Serial.print("Raw Ethanol "); Serial.print(sgp.rawEthanol); Serial.println("");

  
  delay(1000);
  }
  
  
}