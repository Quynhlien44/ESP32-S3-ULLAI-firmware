# Ultra Low Latency AI for ESP32-S3 (ULLAI Project)

## 1. Project objectives
- Build an ultra low latency embedded AI system (<1ms inference, <5ms total sensor-to-AI).
- Lightweight AI model, <20KB capacity with int8 quantization.
- Use 3 sensors: NSL 19M51 (light), DHT22 (temperature/humidity), Grove VOC/eCO2.
- Ensure accuracy >90% on real environmental scenarios.
- Stable continuous operation for 24 hours, ensuring privacy - no data transmission outside.


## 2. AI pipeline overview - Firmware
- Collect sensor data via ADC, digital, I2C.
- Normalize data according to pre-calculated scaler.
- Run inference model TensorFlow Lite Micro, output probabilities.
- Log data, probability, latency via serial.
- Support testing, benchmarking and stress testing.


## 3. Hardware instructions
- Connect NSL 19M51 sensor to ADC pin [pin 7]
- Connect DHT22 to digital GPIO pin [pin 4]
- Connect Grove VOC/eCO2 to I2C bus [SDA, SCL - pin 17, 18]
- Supply 3.3V and GND to sensors according to the diagram


## 4. Instructions for building & flashing firmware

### Environment setup
- Install PlatformIO extension for VSCode or install CLI PlatformIO directly.
- Install Python (version 3.8+).

### Build & flash
```bash
cd firmware
platformio run # build firmware
platformio run --target upload # upload firmware ESP32-S3
```

### Monitor serial
```bash
platformio device monitor --port /dev/ttyACM0 --baud 115200
```


## 5. Instructions for getting logs with Python script
- Connect the ESP32-S3 board via USB, remember to turn off Serial Monitor if it is open.
- Run the Python script to collect serial logs into a CSV file:
```bash
cd ai_pipeline
python log_serial_to_csv.py
```
- Log files will be saved at `ai_log.csv` for analysis.


## 6. Benchmark target

| Characteristics | Target |
|---------------------------|---------------------|
| Latency inference AI | < 1ms |
| Total latency sensor → AI | < 5ms |
| Model size (quantized) | < 20KB |
| Accuracy | > 90% on scenarios |
| Continuous operation | ≥ 24 hours without error |
| Data security | No external transmission |


## 7. Common problems & solutions
- DHT22 sensor reports reading error: check connection, cable and GPIO pin.
- Serial port cannot be connected when opening Serial Monitor/Script log at the same time: turn off 1 of 2 before running the other.
- AI output does not change: check input data, scaler, or retrain the model.
- High latency: check synchronous tasks, split FreeRTOS core if needed.