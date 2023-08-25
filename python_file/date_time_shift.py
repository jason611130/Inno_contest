from datetime import datetime, timedelta

def shift_time(current_time, shift):
    # 將字串轉換為datetime物件
    current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    
    # 增加或減少時間間隔
    shifted_time = current_time + timedelta(**shift)
    
    # 將結果轉換為字串並回傳
    return shifted_time.strftime('%Y-%m-%d %H:%M:%S')

# 測試程式碼
current_time = str(datetime.now())[0:19]
shift = {'days': 0, 'hours': -8, 'minutes': 0, 'seconds': -45}

shifted_time = shift_time(current_time, shift)
print(type(shifted_time))