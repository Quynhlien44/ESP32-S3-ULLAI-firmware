# ULLAI ESP32-S3 Project

This is a PlatformIO project for the ESP32-S3 microcontroller.

## Hardware Requirements

- ESP32-S3-DevKitC-1 development board
- USB-C cable for programming and power
- Optional: External components as needed for your specific application

## Features

- Arduino framework support
- Built-in LED control
- Button input handling
- Serial communication for debugging
- PSRAM support enabled
- Exception decoder for better debugging

## Getting Started

1. **Install PlatformIO**: If you haven't already, install PlatformIO in VS Code or as a standalone tool.

2. **Open Project**: Open this folder in VS Code with the PlatformIO extension installed.

3. **Build**: Use the PlatformIO build command or press `Ctrl+Alt+B`.

4. **Upload**: Connect your ESP32-S3 board and use the upload command or press `Ctrl+Alt+U`.

5. **Monitor**: Open the serial monitor to see debug output using `Ctrl+Alt+S`.

## Project Structure

```
ULLAI-ESP32S3/
├── platformio.ini      # PlatformIO configuration
├── src/
│   └── main.cpp       # Main application code
├── include/           # Header files (if needed)
├── lib/              # Local libraries
└── test/             # Unit tests
```

## Configuration

The project is configured for:
- **Board**: ESP32-S3-DevKitC-1
- **Framework**: Arduino
- **Upload Speed**: 921600 baud
- **Monitor Speed**: 115200 baud
- **Debug Level**: Verbose (level 3)

## Pin Configuration

- **Built-in LED**: GPIO 48
- **Boot Button**: GPIO 0
- **USB Serial**: Built-in USB CDC

## Customization

You can modify the `platformio.ini` file to:
- Add library dependencies in the `lib_deps` section
- Change build flags and options
- Modify upload and monitor settings
- Add multiple environments for different configurations

## Troubleshooting

1. **Upload Issues**: 
   - Make sure the correct port is selected
   - Try holding the boot button during upload
   - Check that the USB cable supports data transfer

2. **Serial Monitor**: 
   - Ensure the correct baud rate (115200)
   - Try different USB ports
   - Reset the board after upload

3. **Build Errors**: 
   - Update PlatformIO platform and tools
   - Check library compatibility
   - Verify ESP32-S3 board selection

## Next Steps

This template provides a basic starting point. You can extend it by:
- Adding sensor libraries and code
- Implementing WiFi connectivity
- Adding web server functionality
- Integrating with cloud services
- Implementing OTA updates

Happy coding with your ESP32-S3!
