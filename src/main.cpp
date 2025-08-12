#include <Arduino.h>
#include "sensor_driver.h"
#include "ai_inference.h"

#define N_OUTPUTS 3
float probabilities[N_OUTPUTS];

void setup()
{
  Serial.begin(115200);
  delay(2000);
  Serial.println("Beginning setup...");
  sensor_init(); // Initialize sensors
  ai_init();     // Initialize AI inference engine
  Serial.println("Setup done!");
}

void loop()
{
  float ldr_voltage, temp, hum, tvoc, eco2;
  read_sensors(ldr_voltage, temp, hum, tvoc, eco2);

  // If SGP30 is not available, simulate average value
  if (tvoc < 0)
    tvoc = 60.0f;
  if (eco2 < 0)
    eco2 = 450.0f;
  // Create array input for AI model
  float input[5] = {ldr_voltage, temp, hum, tvoc, eco2};
  float output[3];
  ai_predict(input, output, 5, 3); // Predict using AI model

  softmax(output, probabilities, 3);

  Serial.printf("Raw input: LDR=%.2fV, Temp=%.2fC, Hum=%.2f%%, TVOC=%.2f, eCO2=%.2f\n",
                ldr_voltage, temp, hum, tvoc, eco2);

  Serial.print("AI probabilities: ");
  for (int i = 0; i < N_OUTPUTS; i++)
  {
    Serial.printf("%.3f ", probabilities[i]);
  }
  Serial.println();

  delay(1000);
}
