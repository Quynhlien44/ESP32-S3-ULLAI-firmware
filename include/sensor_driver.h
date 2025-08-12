#ifndef SENSOR_DRIVER_H
#define SENSOR_DRIVER_H

#define I2C_SDA 17
#define I2C_SCL 18

#include <DHT.h>
#include <Adafruit_SGP30.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define LDR_PIN 7

extern DHT dht;
extern Adafruit_SGP30 sgp;

void sensor_init();
void read_sensors(float &ldr_voltage, float &temperature, float &humidity, float &tvoc, float &eco2);

#endif
