#include <Arduino.h>
#include "sensor_driver.h"
#include "ai_inference.h"

#define N_OUTPUTS 3
float probabilities[N_OUTPUTS];
unsigned long t_start, t_end;

void setup()
{
  Serial.begin(115200);
  delay(2000);
  Serial.println("Beginning setup...");
  sensor_init(); // Initialize sensors
  ai_init();     // Initialize AI inference engine
  Serial.println("Setup done!");
}

// const char *scenario = "anomaly";
unsigned long lastMemLog = 0;

void loop()
{
  float ldr_voltage, temp, hum, tvoc, eco2;
  read_sensors(ldr_voltage, temp, hum, tvoc, eco2);
  t_start = micros(); // Time before AI

  // If SGP30 is not available, simulate average value
  if (tvoc < 0)
    tvoc = 60.0f;
  if (eco2 < 0)
    eco2 = 450.0f;
  // Create array input for AI model
  float input[5] = {ldr_voltage, temp, hum, tvoc, eco2};
  float output[N_OUTPUTS];
  ai_predict(input, output, 5, N_OUTPUTS); // AI inference

  softmax(output, probabilities, N_OUTPUTS);

  t_end = micros(); // Time after AI

  // Log line with latency
  Serial.printf("%lu,%.2f,%.2f,%.2f,%.2f,%.2f,%.0f,%.0f,%.0f,AI_latency_us:%lu\n",
                millis(),
                ldr_voltage, temp, hum, tvoc, eco2,
                probabilities[0] * 100,
                probabilities[1] * 100,
                probabilities[2] * 100,
                t_end - t_start);

  unsigned long now = millis();
  if (now - lastMemLog > 300000)
  { // 5 min
    Serial.printf("Free heap: %u bytes\n", ESP.getFreeHeap());
    lastMemLog = now;
  }
  delay(1000);
}
