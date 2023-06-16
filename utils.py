import pandas as pd
import csv
from datetime import datetime
import random

def create_data():
    # 使用 Python open 方法打开文件进行写入，
    with open('data.csv', mode='w', encoding='utf-8') as example_file:
        writer = csv.writer(example_file, delimiter=',', quotechar='"', quoting =csv.QUOTE_MINIMAL)
        # 用 writerow 方法写入表头行
        writer.writerow(['visa_center', 'appointment_type', 'visa_type', 'Earliest_booking_time'])
        # 用 writerow 方法写入数据行
        writer.writerow( ['Italy Visa Application Center, Jinan', '意大利签证申请', 'NORMAL JINAN'])
        writer.writerow( ['Italy Visa Application Center, Jinan', '意大利签证申请', 'VIP JINAN'])
        writer.writerow(['南京意大利签证申请中心', 'STANDARD NANJING', 'NANJING STANDARD'])
        writer.writerow(['成都意大利签证申请中心', '意大利签证申请', '成都普通'])
        writer.writerow(['成都意大利签证申请中心', '意大利签证申请', '成都贵宾'])
        writer.writerow(['昆明意大利签证申请中心', '意大利签证申请', 'VIP 1'])
        writer.writerow(['昆明意大利签证申请中心', '意大利签证申请', '昆明普通'])
        writer.writerow(['武汉意大利签证申请中心', '意大利签证申请', 'VIP WUHAN'])
        writer.writerow(['福州意大利签证申请中心', 'Schengen visa', 'C visa / Schengen visa'])
        writer.writerow(['西安意大利签证申请中心', '意大利签证申请', 'NORMAL XIAN'])
        writer.writerow(['西安意大利签证申请中心', '意大利签证申请', 'VIP XIAN'])
        writer.writerow(['重庆意大利签证申请中心', 'CHONGQING APPOINTMENTS', 'CHONGQING VIP'])
        writer.writerow(['重庆意大利签证申请中心', 'CHONGQING APPOINTMENTS', 'STANDARD'])
        writer.writerow(['长沙意大利签证申请中心', 'Schengen visa', 'C visa / Schengen visa'])


def get_data_array(input_path):
    data_df = pd.read_csv(input_path)
    data_np = data_df.values
    # data = np.column_stack((data_np, np.repeat(None, data_np.shape[0])))
    return data_np

def log_msg(log, message):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    log.write(date_time + "  ::  " + message + "\n")
    print(message)

def update(rowindex, time):
    df = pd.read_csv('data.csv', encoding='utf-8')
    df['Earliest_booking_time'].loc[rowindex] = time
    df.to_csv('data.csv', index=False, encoding='utf-8')
    

def getrandom():
    return random.randint(3, 6)



def csv_to_html():
    upload_path = 'data\data.csv'
    df = pd.read_csv(upload_path, encoding="utf-8")
    filename = "data.html"
    with open(filename, 'w') as file_object:
        file_object.write(df.to_html())
    return "data.html"

def get_mail_list():
    mail_list=[] 
    with open("data\data_mail.txt", 'r') as f:
        for line in f:
            mail_list.append(list(line.strip('\n').split(',')))
    return mail_list

# 更新选择内容
mail_list = ['596908514@qq.com', '1340330258@qq.com', 'xuxiaolei2017@126.com', '873163327@qq.com',
             'mm328@qq.com', '421175261@qq.com']
a = 1