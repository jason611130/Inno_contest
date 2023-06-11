import datetime
import time
import tkinter 
from tkinter import ttk
from tkinter import messagebox
import string
import random
import threading
import numpy as np

from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer

import serial

# --------------------------------------------
# init value
course = np.zeros((7,14),dtype=int)
for j in range(0,7):
    if(j%2==0):
      for i in range(0,14):
        course[j][i]=1

data_set={"Day":0,"Classtime":0,"Co2":0,"Temperature":0,"Humidity":0,"Course":course}
# --------------------------------------------

def predict_open_ac():
# predict open condition Co2 > 1000
# 空調開後檢測CO2有無超標(有人)反之停止送風
  if(read_sensor()[0]<=1000):
    #預測錯誤將下禮拜課表清空
     course[data_set['Day']][data_set["Classtime"]]=0

  return 0
def read_sensor(): 
  # CO2  temperature humidity
  SerialIn = serial.Serial("COM6",115200)
  sensor_all_data=[0,0,0]
  data_in = SerialIn.readline() 
  data_raw = data_in.decode('utf-8') 
  print(data_raw)
  
  while True:
      try:
        Co2=int(float(data_raw[27:31]))
        break
      except ValueError:
        Co2=int(float(data_raw[27:30]))

  while True:
      try:
        temperature=int(float(data_raw[6:8]))
        humidity=int(float(data_raw[19:21]))
        break
      except ValueError:
        for a in range(0,2):
          print("wating DHT11")
          time.sleep(1)
          
          sensor_all_data=[0,0,0]
          data_in = SerialIn.readline() 
          data_raw = data_in.decode('utf-8') 
          print(data_raw)   
          
  if(Co2<=200):
      Co2=Co2*10
  data_set['Co2']=Co2
  data_set['Temperature']=temperature
  data_set['Humidity']=humidity
  # sensor_all_data[0]=Co2
  # sensor_all_data[1]=temperature
  # sensor_all_data[2]=humidity
  return 0

def generateConfig():
      config = EdgeConfig()
      nodeConfig = NodeConfig(nodeType = constant.EdgeType['Gateway'])
      config.node = nodeConfig
      deviceConfig = DeviceConfig(id = 'Dorm_323',
      name = 'CO2_Temp_humi',
      description = 'Device',
      deviceType = '323-2_Device',
      retentionPolicyName = '')
        
      analog = AnalogTagConfig(name = 'Co2',
      description = 'Co2 ',
      readOnly = False,
      arraySize = 0,
      spanHigh = 1000,
      spanLow = 0,
      engineerUnit = '',
      integerDisplayFormat = 4,
      fractionDisplayFormat = 2)
      deviceConfig.analogTagList.append(analog)

      analog = AnalogTagConfig(name = 'Temperature',
      description = 'Temperature',
      readOnly = False,
      arraySize = 0,
      spanHigh = 1000,
      spanLow = 0,
      engineerUnit = '',
      integerDisplayFormat = 4,
      fractionDisplayFormat = 2)
      deviceConfig.analogTagList.append(analog)

      analog = AnalogTagConfig(name = 'Humidity',
      description = 'Humidity',
      readOnly = False,
      arraySize = 0,
      spanHigh = 1000,
      spanLow = 0,
      engineerUnit = '',
      integerDisplayFormat = 4,
      fractionDisplayFormat = 2)
      deviceConfig.analogTagList.append(analog)

        
      discrete = DiscreteTagConfig(name = 'DTag',
      description = 'DTag ',
      readOnly = False,
      arraySize = 0,
      state0 = '0',
      state1 = '1')
      deviceConfig.discreteTagList.append(discrete)
      
        
      text = TextTagConfig(name = 'TTag',
      description = 'TTag ',
      readOnly = False,
      arraySize = 0)
      deviceConfig.textTagList.append(text)
      config.node.deviceList.append(deviceConfig)
      return config

def generateData():
      edgeData = EdgeData()
  
      deviceId = 'Dorm_323'
      tagName = 'Co2'
      read_sensor()
      value = data_set['Co2']
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      deviceId = 'Dorm_323'
      tagName = 'Temperature'
      read_sensor()
      value = data_set['Temperature']
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      deviceId = 'Dorm_323'
      tagName = 'Humidity'
      read_sensor()
      value = data_set['Humidity']
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)
      print(read_sensor())
        
      deviceId = 'Dorm_323'
      tagName = 'status'
      value = 1
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)
       
      deviceId = 'Dorm_323'
      tagName = 'text'
      value = "running"
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      edgeData.timestamp = datetime.datetime.now()
      #edgeData.timestamp = datetime.datetime(2020,8,24,6,10,8)  # you can defne the timestamp(local time) of data 
      return edgeData

# default_nodeId=233c19cb-325e-4209-a319-d8816b798e49
# Credential Key=856e0a0ad738fe0fda4e23a3ccc165xk
# DCCS API URL =https://api-dccs-ensaas.sa.wise-paas.com
options = EdgeAgentOptions(
  nodeId = '233c19cb-325e-4209-a319-d8816b798e49',        
  type = constant.EdgeType['Gateway'],                    # 節點類型 (Gateway, Device), 預設是 Gateway
  deviceId = 'deviceId',                                  # 若 type 為 Device, 則必填
  heartbeat = 60,                                         # 預設是 60 seconds
  dataRecover = True,                                     # 是否需要斷點續傳, 預設為 true
  connectType = constant.ConnectType['DCCS'],             # 連線類型 (DCCS, MQTT), 預設是 DCCS
  MQTT = MQTTOptions(                                     # 若連線類型是 MQTT, MQTTOptions 為必填
    hostName = '127.0.0.1',
    port = 1883,
    userName = 'admin',
    password = 'admin',
    protocalType = constant.Protocol['TCP']               # MQTT protocal (TCP, Websocket), 預設是 TCP
  ),
                                                          # 若連線類型是 DCCS, DCCSOptions 為必填
  DCCS = DCCSOptions(
    apiUrl = 'https://api-dccs-ensaas.sa.wise-paas.com/',           # DCCS API Url
    credentialKey = '9764829d109bde7b3469518c96f53e02'    # Creadential key
  )
)

edgeAgent = EdgeAgent( options = options )
edgeAgent.connect()

config=generateConfig()
edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)

# read_sensor()
print(course)
while(1):
  config=generateConfig()
  edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)
  data=generateData()
  result = edgeAgent.sendData(data)
  print("sendData")
  time.sleep(0.1)
  
  edgeAgent.uploadConfig(action = constant.ActionType['Delete'], edgeConfig = config)
  time.sleep(0.1)
  print("delete_Data")