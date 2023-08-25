import requests
import json

def get_session_and_login(username,password):
    url="http://portal-datahub-trainingapps-eks004.sa.wise-paas.com/api/v1/Auth"
    payload = json.dumps({
        "username": username,
        "password": password
        })
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        }
    s = requests.Session() 
    response = s.request("POST", url, headers=headers, data=payload)
    if response.status_code==200 :
        res=json.loads(response.text)
        return res['status'] == 'passed' , s
    else:
        return False,s
def api_post(path,session,payload):
    baseUrl="http://portal-datahub-trainingapps-eks004.sa.wise-paas.com/api"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    url=baseUrl+path
    response = session.request("POST", url, headers=headers, data=payload)
    return response

def catch_datahub_data(session):
  path = "/v1/HistData/raw"
  payload = json.dumps({
  "tags": [
    {
      "nodeId": "63803223-ff59-4deb-ad10-05632aff9612",
      "deviceId": "Tr202",
      "tagName": "TTag"
    }
  ],
  "startTs": "2023-07-05T13:39:39.832Z",
  "endTs": "2023-07-05T21:33:40.832Z",
  "desc": False,
  "count": 10
  })
  
  response = api_post(path,session,payload)
  return response

# 取得登入狀態，以及request session

is_login , s = get_session_and_login( "jason611130@gmail.com","Jason910228!")
print("Login :",is_login)

response = catch_datahub_data(s)
print(response.text)
res=json.loads(response.text)
# print(res[0]['values'][0]['value'])