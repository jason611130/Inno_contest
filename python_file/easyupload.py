import datetime
import time
import tkinter 
from tkinter import ttk
from tkinter import messagebox
import string
import random
import threading


from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer

import serial

def read_sensor():  
  SerialIn = serial.Serial("COM6",115200)
  sensor_all_data=[0,0,0]
  data_in = SerialIn.readline() 
  data_raw = data_in.decode('utf-8') 

  Co2=int(float(data_raw[27:30]))
  temperature=int(float(data_raw[6:8]))
  humidity=int(float(data_raw[19:21]))
  
  sensor_all_data[0]=Co2
  sensor_all_data[1]=temperature
  sensor_all_data[2]=humidity
  return sensor_all_data

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

        
      # discrete = DiscreteTagConfig(name = 'DTag',
      # description = 'DTag ',
      # readOnly = False,
      # arraySize = 0,
      # state0 = '0',
      # state1 = '1')
      # deviceConfig.discreteTagList.append(discrete)
      
        
      # text = TextTagConfig(name = 'TTag',
      # description = 'TTag ',
      # readOnly = False,
      # arraySize = 0)
      # deviceConfig.textTagList.append(text)
      # config.node.deviceList.append(deviceConfig)
      return config

def generateData():
      edgeData = EdgeData()
  
      deviceId = 'Dorm_323'
      tagName = 'Co2'
      read_data=read_sensor()
      value = read_data[0]
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      deviceId = 'Dorm_323'
      tagName = 'Temperature'
      read_data=read_sensor()
      value = read_data[1]
      tag = EdgeTag(deviceId, tagName, value)
      edgeData.tagList.append(tag)

      deviceId = 'Dorm_323'
      tagName = 'Humidity'
      read_data=read_sensor()
      value = float(read_data[2])
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

# node id 7d9d1053-3d48-4f05-8889-337ac679ea7e
# cerdential 11c500c9f08ffe5f45c0bb47270f4bwp
# DCCS API URL =https://api-dccs-ensaas.sa.wise-paas.com

# default_nodeId=a8f95c34-cc5c-4e7c-a6d2-32e736adff8f
# Credential Key=dd579f280505c0162b1f7f945177a9w0
# DCCS API URL =https://api-dccs-ensaas.sa.wise-paas.com
options = EdgeAgentOptions(
  nodeId = '290b5e7d-2e89-4ac4-bf20-91efc5f7dc8a',        
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
    credentialKey = '8b9c89b7c8cbac2160b4fe10ee9cd0fo'    # Creadential key
  )
)

edgeAgent = EdgeAgent( options = options )
edgeAgent.connect()

config=generateConfig()
edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)

# read_sensor()
while(1):
  config=generateConfig()
  # edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)
  # data=generateData()
  # result = edgeAgent.sendData(data)
  # print("sendData")
  # time.sleep(1)
  # edgeAgent.uploadConfig(action = constant.ActionType['Delete'], edgeConfig = config)
  # time.sleep(1)
  # print("delete_Data")