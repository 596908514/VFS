import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as c_Options
from selenium.webdriver.firefox.options import Options as f_Options
from selenium.webdriver.chrome.service import Service as c_Service
from selenium.webdriver.firefox.service import Service as f_Service

from utils import log_msg, get_data_array, update, getrandom, csv_to_html, get_mail_list
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np
import random

# 随机ip池
# proxy_arr = [
#     '--proxy-server=180.121.151.62:30001',
# ]   

mail_list = get_mail_list()
data_path = 'data\data.csv'
def mail(to, message):
    mail_host = args.mail_host
    mail_sender = args.mail_id
    mail_license = args.token
    mail_receivers = to
    smtp_port = args.port
    msg = MIMEMultipart('alternative')
    # 邮件主题
    subject_content = message
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    msg["From"] = Header(mail_sender)
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    # msg["To"] = Header(mail_receivers)
    # 设置邮件主题
    msg["Subject"] = Header(subject_content,'utf-8')

    # 邮件正文内容
    body_content = message
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_content,"plain","utf-8")
    # 向MIMEMultipart对象中添加文本对象
    msg.attach(message_text)

    mail_body = open(csv_to_html(), 'r').read()
    message_html = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(message_html)


    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, smtp_port)  
    stp.login(mail_sender,mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, msg.as_string())
    log_msg(log, message)
    # 关闭SMTP对象
    stp.quit()


def login(log, browser, wait):
    # Login Page
    browser.get('https://visa.vfsglobal.com/chn/zh/ita/login')
    time.sleep(getrandom()+3)

    # 点击接受cookie
    browser.find_element(By.ID, "onetrust-accept-btn-handler").click()

    time.sleep(3)
    # 输入账号密码
    browser.find_element(By.ID, "mat-input-0").send_keys(args.vfs_account)
    time.sleep(getrandom()-2)
    browser.find_element(By.ID, "mat-input-1").send_keys(args.vfs_pw)
    time.sleep(getrandom()-2)
    browser.find_element(By.XPATH, "//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base ng-star-inserted']").click()
    time.sleep(getrandom())
    # browser.save_screenshot('2.png')

    # 检测是否 输入有误 或者 账户锁定
    if '遇到错误' in browser.page_source:
        mail(to=args.sendtoerror, message="web failed!")
        return False
    elif '请输入有效邮箱地址和密码' in browser.page_source:
        mail(to=args.sendtoerror, message='Logged failed!')
        return False
    elif '锁定' in browser.page_source:
        mail(to=args.sendtoerror, message='your account is locked!')
        return False

    time.sleep(getrandom()+5)
    return True


def appointment(log, browser, wait):
    if login(log, browser, wait):
        log_msg(log, 'id:{}, pw:{} : logged in!'.format(args.vfs_account, args.vfs_pw))
    else:
        return []
    
    # 点击 新的预约
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mat-focus-indicator btn mat-btn-lg btn-brand-orange d-none d-lg-inline-block position-absolute top-n3 right-0 z-index-999 mat-raised-button mat-button-base']"))).click()
    time.sleep(getrandom())
    
    data_np = get_data_array(data_path)
    while True:
        for rowindex in np.arange(data_np.shape[0]):
            # 选择第一个选项
            if browser.find_element(By.ID, 'mat-select-value-1').text != data_np[rowindex][0]:
                browser.find_element(By.XPATH, "//mat-select[@id='mat-select-0']").click()
                # wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select[@id='mat-select-0']"))).click()
                time.sleep(1)
                options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
                for element in options:
                    my_str = element.text
                    if data_np[rowindex][0] == my_str:
                        element.click()
                        break           
                time.sleep(getrandom())
            time.sleep(0.5)
            # 选择第二个选项
            if browser.find_element(By.ID, 'mat-select-value-3').text != data_np[rowindex][1]:
                browser.find_element(By.XPATH, "//mat-select[@id='mat-select-2']").click()
                # wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select[@id='mat-select-2']"))).click() 
                time.sleep(1)
                options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
                for element in options:
                    my_str = element.text
                    if data_np[rowindex][1] == my_str:
                        element.click()
                        break           
                time.sleep(getrandom())
            time.sleep(0.5)
            # 选择第三个选项
            if browser.find_element(By.ID, 'mat-select-value-5').text != data_np[rowindex][2]:
                browser.find_element(By.XPATH, "//mat-select[@id='mat-select-4']").click()
                # wait.until(EC.element_to_be_clickable((By.XPATH, "//mat-select[@id='mat-select-4']"))).click()
                time.sleep(1)
                options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
                for element in options:
                    my_str = element.text
                    if data_np[rowindex][2] == my_str:
                        element.click()
                        break
                time.sleep(getrandom())  
            time.sleep(0.5)
            # 判断有无可以预约时间，没有则继续循环
            text = browser.find_element(By.XPATH, "//div[@class='alert alert-info border-0 rounded-0']").text
            if text != data_np[rowindex][3]:
                update(rowindex, text)
                data_np[rowindex][3] = text
                if "最早可预约的时间" in text:
                    mail(args.sendto, 'Found Appointment! \n签证申请中心: {}\n预约类型: {}\n签证类型: {}\n{}'.format(data_np[rowindex][0], data_np[rowindex][1], data_np[rowindex][2], text))
        log_msg(log, 'No Appointment Available!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', type=str, default='firefox') # 游览器
    parser.add_argument('--vfs_account', type=str, default='1340330258@qq.com') # vfs登陆账号
    parser.add_argument('--vfs_pw', type=str, default='Panyixi0824@') # vfs 登陆密码
    parser.add_argument('--mail_id', type=str, default='596908514@qq.com') # stmp邮箱
    parser.add_argument('--token', type=str, default='kgtfmommembqbfai') # stmp 密钥
    parser.add_argument('--sendto', type=list, default=mail_list)
    parser.add_argument('--sendtoerror', type=str, default='596908514@qq.com')
    parser.add_argument('--mail_host', type=str, default='smtp.qq.com')
    parser.add_argument('--port', type=int, default=587)
    
    args = parser.parse_args()
    
    # 初始化 log
    log = open('vfslog.txt', 'w+')

    # browser 初始化
    if args.browser == 'chrome':
        options = c_Options()
        # 设置随机ip
        # proxy = random.choice(proxy_arr)
        # print(proxy)
        # options.add_argument(proxy)
        # options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080") # 窗口大小设置
        options.add_argument("--start-maximized") # 窗口最大化
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # 添加 useragent
        chrome_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'  
        options.add_argument(f'user-agent={chrome_ua}')
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        browser = webdriver.Chrome(service=c_Service(r'C:\Users\潘克豪\Desktop\vfs_appointment\driver\chromedriver.exe'), options=options)
    elif args.browser == 'firefox':
        options = f_Options()
        # options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080") # 窗口大小设置
        options.add_argument("--start-maximized") # 窗口最大化
        # 添加 useragent
        firefox_ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'
        options.add_argument(f'user-agent={firefox_ua}')
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        browser = webdriver.Firefox(service=f_Service(r'C:\Users\潘克豪\Desktop\vfs_appointment\driver\geckodriver.exe'), options=options) # 生成 browser
    
    wait = WebDriverWait(browser, 10)
    
    results = appointment(log, browser, wait)
    if len(results):
        mail(args.sendto, 'Found Appointment! \n签证申请中心: {}\n预约类型: {}\n签证类型: {}'.format(results[0], results[1], results[2]))
        
    