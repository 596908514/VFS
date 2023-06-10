from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import smtplib, ssl
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

## VFS login email
email_str = '1340330258@qq.com'
## VFS password
pwd_str = 'Panyixi0824@'
## Sender Email
sender = "596908514@qq.com"
## App Password
app_password = "kgtfmommembqbfai"
# Make a list of emails, where you wanna send mail
to = ['220222184@seu.edu.cn']
to_error = ['596908514@qq.com']

# 选择签证中心
visa_center = "重庆意大利签证申请中心"
# 选择预约类型
appointment_type = "SUNDAY VIP"
# 选择签证类型
visa_type = "SUNDAY VIP NANJING"

def message(subject="Python Notification",
            text=""):
    # build message contents
    msg = MIMEMultipart()

    # Add Subject
    msg['From'] = Header(sender)
    msg['Subject'] = subject

    # Add text contents
    msg.attach(MIMEText(text))
    return msg


def log_msg(log, message):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    log.write(date_time + "  ::  " + message + "\n")


def choose_center(browser, log, wait):
    browser.execute_script("window.scrollTo(0,0)")

    wait.until(EC.element_to_be_clickable((By.XPATH,
                                           "//mat-select[@id='mat-select-0']"))).click()  # clicked on main drop down thus the option could be visible

    options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
    for element in options:
        my_str = element.text
        if visa_center in my_str:
            element.click()
            break

    time.sleep(5)

    wait.until(EC.element_to_be_clickable((By.XPATH,
                                           "//mat-select[@id='mat-select-2']"))).click()  # clicked on main drop down thus the option could be visible

    options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
    for element in options:
        my_str = element.text
        if appointment_type in my_str:
            element.click()
            break

    time.sleep(5)

    wait.until(EC.element_to_be_clickable((By.XPATH,
                                           "//mat-select[@id='mat-select-4']"))).click()  # clicked on main drop down thus the option could be visible

    options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
    for element in options:
        my_str = element.text
        if visa_type in my_str:
            element.click()
            break

    time.sleep(4)
    # browser.find_element(By.XPATH,
    #                      "//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base']").click()


    # browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    # browser.implicitly_wait(3)

    # wait.until(EC.element_to_be_clickable((By.XPATH,
    #                                        "//mat-select[@id='mat-select-4']"))).click()  # clicked on main drop down thus the option could be visible

    # options = browser.find_elements(By.CSS_SELECTOR, "mat-option")
    # for element in options:
    #     my_str = element.text
    #     if "Tourism" in my_str:
    #         element.click()
    #         break

    # time.sleep(5)

    if "最早可预约的时间" in browser.page_source:
        return True
    return False


def login(browser, log, wait):
    # Login Page
    browser.get('https://visa.vfsglobal.com/chn/zh/ita/login')
    # browser.maximize_window()
    time.sleep(5)
    browser.find_element(By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
    time.sleep(2)
    browser.find_element(By.ID, "mat-input-0").send_keys(email_str)
    browser.find_element(By.ID, "mat-input-1").send_keys(pwd_str)
    time.sleep(2)
    browser.find_element(By.XPATH,
                         "//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base ng-star-inserted']").click()
    log_msg(log, "Logged in ") 
    time.sleep(8)

    wait.until(EC.element_to_be_clickable((By.XPATH,
                                           "//button[@class='mat-focus-indicator btn mat-btn-lg btn-brand-orange d-none d-lg-inline-block position-absolute top-n3 right-0 z-index-999 mat-raised-button mat-button-base']"))).click()

    time.sleep(4)


def check_session_expired(browser, log):
    if 'timeout' in browser.page_source:
        log_msg(log, "Session expired.")
        return True
    return False


def monitor_appointments():
    log = open('vfslog.txt', 'w+')
    while True:
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        browser = webdriver.Firefox(service=Service(r'C:\Users\潘克豪\Desktop\VFS-Appointment-Bot\geckodriver.exe'), options=options)
        wait = WebDriverWait(browser, 20)
        try:
            login(browser, log, wait)
        except:
            # context = ssl.create_default_context()
            # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            #     server.login(sender, app_password)
            #     server.sendmail(sender, to_error, "Login Failed")
            break
        count = 0
        while True:
            try:
                found = choose_center(browser, log, wait)
            except:
                log_msg(log, "Error Occurred")
                break
            if found:
                print("Appointment Found !!!")
                log_msg(log, "Appointment Found !!!")
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as server:
                    server.login(sender, app_password)
                    server.sendmail(sender, to, "Appointment Found !!!")
                # break
            else:
                log_msg(log, "No Appointments Available")
            count += 1
            if count == 10:
                break
            # 5 min
            time.sleep(60)
        browser.close()
        # 15 min
        time.sleep(30)


def monitor_appointments2():
    log = open('vfslog.txt', 'w+')
    while True:
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        browser = webdriver.Firefox(service=Service(r'C:\Users\潘克豪\Desktop\VFS-Appointment-Bot\geckodriver.exe'), options=options)
        wait = WebDriverWait(browser, 20)
        try:
            login(browser, log, wait)
        except:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.qq.com", 587, context=context) as server:
                server.login(sender, app_password)
                server.sendmail(sender, to_error, "Login Failed")
            break
        found = choose_center(browser, log, wait)
        if found:
            print("Appointment Found !!!")
            log_msg(log, "Appointment Found !!!")
            # email
            smtp = smtplib.SMTP('smtp.qq.com', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender, app_password)
            # Provide some data to the sendmail function!
            smtp.sendmail(from_addr=sender,
                          to_addrs=to, msg=msg.as_string())

            # Finally, don't forget to close the connection
            smtp.quit()
            # break
        browser.close()
        # 15 min
        time.sleep(900)


msg = message("VFS ", "Appointment Found!")
error1 = message("Login Failed", "Restart Application")
error2 = message("Error Occurred", "Restart Application")

# monitor_appointments2()
monitor_appointments2()
