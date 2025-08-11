#include "sensor_driver.h"
#include <Arduino.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define LDR_PIN 7

// DEFINE variable here for 1 time
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SGP30 sgp;

void sensor_init()
{
    Serial.println("Init DHT...");
    dht.begin();
    Serial.println("Init I2C...");
    Wire.begin(I2C_SDA, I2C_SCL);
    // Serial.println("Init SGP30...");
    // if (!sgp.begin()) {
    //     Serial.println("SGP30 sensor not found!");
    //     while (1);
    // }
    // sgp.IAQinit();
    Serial.println("Init done.");
}

void read_sensors(float &ldr_voltage, float &temperature, float &humidity, float &tvoc, float &eco2)
{
    int ldr_adc = analogRead(LDR_PIN);
    ldr_voltage = (ldr_adc / 4095.0f) * 3.3f;

    humidity = dht.readHumidity();
    temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature))
    {
        Serial.println("Failed to read from DHT sensor!");
        humidity = -1;
        temperature = -1;
    }

    /*if (!sgp.IAQmeasure())
    {
        Serial.println("SGP30 measurement failed");
        tvoc = 0;
        eco2 = 0;
    }
    else
    {
        tvoc = sgp.TVOC;
        eco2 = sgp.eCO2;
    }*/
    tvoc = -1;
    eco2 = -1;
}
