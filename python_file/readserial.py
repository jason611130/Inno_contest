import serial
SerialIn = serial.Serial("COM6",115200)
sensor_all_data=[0,0,0]
data_in = SerialIn.readline() 
data_raw = data_in.decode('utf-8') 

Co2=int(data_raw[5:8])
temperature=int(data_raw[19:21])
humidity=int(data_raw[31:33])
sensor_all_data[0]=Co2
sensor_all_data[1]=temperature
sensor_all_data[2]=humidity
print(sensor_all_data)

# while(1):
    

