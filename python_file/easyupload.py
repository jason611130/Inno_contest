import datetime
import time
import tkinter 
from tkinter import ttk
from tkinter import messagebox
import string
import random
import threading
import numpy as np
import requests

from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer

import serial

# --------------------------------------------
# init value
course = np.ones((7,14),dtype=int)
data_set={"Course":course,"flag":0,"Co2":0,"Temperature":0,"Humidity":0,
          "Min":0,"Hour":0,"Weekday":0,"ACfunc":0,"AvgCo2":[400,400,400,400,400,400,400,400,400,400],
          "AvgTemp":[25,25,25,25,25,25,25,25,25,25],
          "AvgHumi":[50,50,50,50,50,50,50,50,50,50],"Count":0,
          "Avg":[0,0,0],"Humithre":80,"Co2thre":1000,"Tempthre":26,
          "CourseTime":"0000000000000000000000000000"}
# --------------------------------------------

def binary_to_hex(arr):
  binary_string = ''.join(str(bit) for bit in arr)  # 將陣列中的值串起來
  decimal_num = int(binary_string, 2)  # 將二進制轉換為十進制
  hex_num = hex(decimal_num)[2:]  # 將十進制轉換為16進制，並刪除前兩個字元 '0x'
  return hex_num
def coding():
  hex_code=''
  for i in range(7):
    binary_array = data_set["Course"][i]
    hex_code += binary_to_hex(binary_array)
  data_set["CourseTime"]=hex_code

def readtime():
  # 抓小時
  data_set["Min"]=int(str(datetime.datetime.now())[14:16])
  data_set["Hour"]=int(str(datetime.datetime.now())[11:13])
# 抓日期(星期一是0星期日是6)
  data_set["Weekday"]=datetime.datetime.weekday(datetime.datetime.now())
    
def predict_open_ac():
# predict open condition Co2 > 1000
# 空調開後檢測CO2有無超標(有人)反之停止送風
  read_sensor()
  if(data_set['Co2']<=1000):
    #預測錯誤將下禮拜課表清空
     course[data_set["Weekday"]][data_set["Hour"]]=0

  return 0
def read_sensor(): 
  # CO2  temperature humidity
  SerialIn = serial.Serial("COM6",115200)
  data_in = SerialIn.readline() 
  data_raw = data_in.decode('utf-8') 
  # print(data_raw)
  
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

          data_in = SerialIn.readline() 
          data_raw = data_in.decode('utf-8') 
          print(data_raw)   
          
  if(Co2<=200):
      Co2=Co2*10
  data_set['Co2']=Co2
  data_set['Temperature']=temperature
  data_set['Humidity']=humidity
  return 0

def generateConfig():
      config = EdgeConfig()
      nodeConfig = NodeConfig(nodeType = constant.EdgeType['Gateway'])
      config.node = nodeConfig
      deviceConfig = DeviceConfig(id = 'Tr202',
      name = 'CO2_Temp_humi',
      description = 'Device',
      deviceType = 'Tr202',
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

        
      discrete = DiscreteTagConfig(name = 'ACmode',
      description = 'ACmode',
      readOnly = False,
      arraySize = 0,
      state0 = '0',
      state1 = '1')
      deviceConfig.discreteTagList.append(discrete)
      
        
      text = TextTagConfig(name = 'CourseTime',
      description = 'CourseTime',
      readOnly = False,
      arraySize = 0)
      deviceConfig.textTagList.append(text)
      config.node.deviceList.append(deviceConfig)
      return config

def generateData():
      edgeData = EdgeData()
  
      deviceId = 'Tr202'
      tagName = 'Co2'
      value = data_set['Co2']

      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      deviceId = 'Tr202'
      tagName = 'Temperature'
      value = data_set['Temperature']

      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      deviceId = 'Tr202'
      tagName = 'Humidity'
      value = data_set['Humidity']
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)
      print(read_sensor())
        
      deviceId = 'Tr202'
      tagName = 'ACmode'
      value = data_set["ACfunc"]
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)
       
      deviceId = 'Tr202'
      tagName = 'CourseTime'
      value = data_set["CourseTime"]
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      edgeData.timestamp = datetime.datetime.now()
      #edgeData.timestamp = datetime.datetime(2020,8,24,6,10,8)  # you can defne the timestamp(local time) of data 
      return edgeData

def Avgvalue_Cal():
  if(data_set["Count"]<=9):
    data_set["AvgCo2"][data_set["Count"]]=data_set["Co2"]
    data_set["AvgTemp"][data_set["Count"]]=data_set["Temperature"]
    data_set["AvgHumi"][data_set["Count"]]=data_set["Humidity"]
    data_set["Count"]+=1
  else:
    data_set["Count"]=0
  for i in range(3):
     data_set['Avg'][i]=0
  for i in range(10):
     data_set['Avg'][0]+=data_set['AvgCo2'][i]/10
  for i in range(10):
     data_set['Avg'][1]+=data_set['AvgTemp'][i]/10
  for i in range(10):
     data_set['Avg'][2]+=data_set['AvgHumi'][i]/10
def line_notify(message):
  token = 'pBKi8Q17Gz1nuJVoFd1F7zGbeukEKxzmA8NOvriRWwu'
  headers = { "Authorization": "Bearer " + token }
  data = { 'message': message }

  # 要傳送的圖片檔案
  # image = open('my_image.jpg', 'rb')
  # files = { 'imageFile': image }
  requests.post("https://notify-api.line.me/api/notify",
      headers = headers, data = data, files = None)   

# default_nodeId=1ea9cb44-bd3e-4c1f-ba9c-df68ac712323
# Credential Key=522eedd5e981fb65ea466be3268b67t1
# DCCS API URL =https://api-dccs-ensaas.sa.wise-paas.com
options = EdgeAgentOptions(
  nodeId = '1ea9cb44-bd3e-4c1f-ba9c-df68ac712323',        
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
    credentialKey = '522eedd5e981fb65ea466be3268b67t1'    # Creadential key
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
  
  Avgvalue_Cal()
  readtime()
  if(data_set["Hour"]>7 and data_set["Hour"]<23):
    # 預測模型
    if(data_set['Course'][data_set['Weekday']][data_set["Hour"]-7]==1 and data_set["Min"]>50):
      data_set['ACfunc']=2      
      data_set['flag']=2
    else:
      # 開冷氣
      if(data_set["Avg"][0]>data_set["Co2thre"] and data_set["Avg"][1]>data_set["Tempthre"]):
        data_set['Course'][data_set['Weekday']][data_set["Hour"]-8]=1
        data_set['ACfunc']=1
      # 開除溼
      elif(data_set["Avg"][0]>data_set["Co2thre"] and data_set["Avg"][2]>data_set["Humithre"]):
        data_set['ACfunc']=2
        data_set['flag']=1
      else:
        data_set['Course'][data_set['Weekday']][data_set["Hour"]-8]=0
        data_set['ACfunc']=0
        data_set['flag']=1
  coding()
  line_notify(data_set["CourseTime"])
  data=generateData()
  result = edgeAgent.sendData(data)
  time.sleep(0.1)
  edgeAgent.uploadConfig(action = constant.ActionType['Delete'], edgeConfig = config)
  time.sleep(0.1)
  print(data_set)
