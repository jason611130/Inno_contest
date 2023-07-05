import serial
import time

ser = serial.Serial('COM3', 115200)  # 将'/dev/ttyUSB0'替换为ESP32的串行端口号，以及合适的波特率
data = "O"
ser.write(data.encode())
data_in = ser.readline() 
data_raw = data_in.decode('utf-8') 
print(data_raw)
time.sleep(1)

data = "X"
ser.write(data.encode())

time.sleep(1)
data_in = ser.readline() 
data_raw = data_in.decode('utf-8') 
print(data_raw)
ser.close()