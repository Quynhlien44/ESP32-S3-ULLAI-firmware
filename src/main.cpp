#include <Arduino.h>
#include "sensor_driver.h"

void setup()
{
  Serial.begin(115200);
  delay(2000);
  Serial.println("Beginning setup...");
  sensor_init();
  Serial.println("Setup done!");
}

void loop()
{
  float ldr_voltage, temperature, humidity, tvoc, eco2;
  read_sensors(ldr_voltage, temperature, humidity, tvoc, eco2);

  Serial.print("LDR Voltage: ");
  Serial.print(ldr_voltage);
  Serial.print(" | Temp: ");
  Serial.print(temperature);
  Serial.print(" | Hum: ");
  Serial.print(humidity);
  Serial.print(" | TVOC: ");
  Serial.print(tvoc);
  Serial.print(" | eCO2: ");
  Serial.println(eco2);

  delay(1000);
}
