import requests
login_url = 'http://portal-datahub-trainingapps-eks004.sa.wise-paas.com/#/'
data = {
    'username': 'Jason611130@gmail.com',
    'password': 'Jason910228!'
}
response = requests.post(login_url, json=data)
if response.status_code == 200:
    token = response.json()['access_token']
    print("登录成功！")
    print("访问令牌：", token)
else:
    print("登录失败。错误代码：", response.status_code)