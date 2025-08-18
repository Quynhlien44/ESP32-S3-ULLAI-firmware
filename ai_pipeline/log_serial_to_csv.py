import serial
import re

ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
with open('anomaly.csv', 'w') as f:
    f.write("timestamp,ldr_v,temp_c,hum_pct,tvoc_ppb,eco2_ppm,scenario\n")
    while True:
        line = ser.readline().decode("utf-8").strip()
        if re.match(r'^\d', line):
            f.write(line + '\n')
            print(line)
