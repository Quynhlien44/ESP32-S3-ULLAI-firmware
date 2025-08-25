import serial
import csv

def main():
    ser = serial.Serial('/dev/ttyACM0', 115200)  # Adjust port
    with open('data/ai_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['millis', 'ldr_voltage', 'temp', 'hum', 'tvoc', 'eco2',
                         'prob0', 'prob1', 'prob2', 'AI_latency_us'])
        try:
            while True:
                line = ser.readline().decode(errors='ignore').strip()
                if line.startswith('Free heap'):
                    print(line)  # Or log separately
                    continue
                if 'AI_latency_us:' in line:
                    # Parse CSV line
                    parts = line.split(',')
                    values = []
                    for val in parts:
                        if 'AI_latency_us:' in val:
                            latency = val.split(':')[1]
                            values.append(latency)
                        else:
                            values.append(val)
                    if len(values) == 10:
                        writer.writerow(values)
                        print("Logged:", values)
        except KeyboardInterrupt:
            print("Stopped logging")

if __name__ == '__main__':
    main()
