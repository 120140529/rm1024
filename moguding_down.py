#! /usr/bin/python3
#-*-coding:utf-8 -*-
import requests
import json
from tkinter import *
import logging
import time
import smtplib
import random
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
# from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)#去掉ssl烦人的警告

filename = '/var/log/' + time.strftime('%Y-%m-%d') + '_蘑菇钉.log'

def log():
    phone='18634622349' #你的账号*
    password='Jjj38381838'#密码*
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 6 Build/OPR1.170623.027) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Authorization": "",
        "roleKey": "",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": "85",
        "Host": "api.moguding.net:9000",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "no-cache",
        }
    url="https://api.moguding.net:9000/session/user/v1/login"
    pyload={"password":password,"phone":phone,"loginType":"android","uuid":""}
 
    response = requests.post(url,data=json.dumps(pyload),headers=headers,verify=False).text
    response = json.loads(response)
    Authorization = response["data"]["token"]
    logging.basicConfig(
        level = logging.INFO, #设置日志级别，默认warning
        format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt = '%a,%d %b %Y %H:%M:%S',
        filename = filename,
        filemode = 'a',   ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
        #encoding = 'utf-8'  ## 编码格式
        #a是追加模式，默认如果不写的话，就是追加模式
    )
    logging.info('token:'+ Authorization)
    return Authorization

def planId(Authorization):
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 6 Build/OPR1.170623.027) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Authorization":Authorization,
        "roleKey": "student",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": "500",
        "Host": "api.moguding.net:9000",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "no-cache",
    }
    url = "https://api.moguding.net:9000/practice/plan/v1/getPlanByStu"
    data={"state":""}
    response = requests.post(url,data=json.dumps(data),headers=headers,verify=False).text
    response = json.loads(response)
    logging.info('planID:' + response['data'][0]['planId'])
    return response['data'][0]['planId']
     
def sin(Authorization,planId):
    iption = ['加油每一天','追踪着鹿的猎人是看不见山的','谁不向前看，谁就会面临许多困难','有志始知蓬莱近，无为总觉咫尺远','雄心壮志是茫茫黑夜中的北斗星']
    country='中国' #国家*
    address='中国河北省保定市莲池区东金庄乡' #地址 *
    province='中国河北省保定市莲池区东金庄乡'#地址 *
    city='中国河北省保定市莲池区东金庄乡'#地址 *
    type='END' #保存两个文件一个写END 一个写START * #START  上班  END 下班
    description=iption[random.randint(0,6)]
 
    url2="https://api.moguding.net:9000/attendence/clock/v1/save"
    headers2 = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 6 Build/OPR1.170623.027) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Authorization":Authorization,
        "roleKey": "student",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": "500",
        "Host": "api.moguding.net:9000",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "no-cache",
        }
    #下面改改就能达到你想在什么地方就在什么地方，经纬度蘑菇钉会根据地理位置识别
    data={"country":country,     
        "address":address,  
        "province":province, 
        "city":city,     
        "latitude":"38.870324" ,#纬度 *
        "description":description,
        "planId":planId,
        "type":type, 
        "device":"Android",
        "longitude":"115.524775"#经度 * 
    }
    response2 = requests.post(url2,data=json.dumps(data),headers=headers2,verify=False).text
    response2 = json.loads(response2)
    logging.info('返回值:' + str(response2))
    return response2,description

def file_operation(filename):
    f = open(filename,"a")
    print('-'*100,file=f)
    f.close

def send_out_mail(responses,description):
    # SMTP服务器,这里使用qq邮箱
    mail_host = "smtp.qq.com"
    # 发件人邮箱
    mail_sender = "120140529@qq.com"
    # 邮箱授权码,注意这里不是邮箱密码
    mail_license = "khlimrlueuoqbhic"
    # 收件人邮箱，可以为多个收件人
    mail_receivers = ["120140529@qq.com"]
    #构建MIMEMultipart对象代表邮件本身，可以往里面添加文本、图片、附件等
    mm = MIMEMultipart('related')

    # 邮件主题
    if responses['code'] == 200:
        subject_content = f"""
        {time.strftime('%Y-%m-%d %H:%M:%S')} 下班签到成功!!!
        """
    else:
        subject_content = f"""
        {time.strftime('%Y-%m-%d %H:%M:%S')} 下班签到失败!!!
        """
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    mm["From"] = "单身狗网络<120140529@qq.com>"
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    mm["To"] = "rm404<120140529@qq.com>"
    # 设置邮件主题
    mm["Subject"] = Header(subject_content, 'utf-8')
    # 邮件正文内容
    if responses['code'] == 200:
        body_content = f"""
        {time.strftime('%Y-%m-%d %H:%M:%S')}签到成功!!!
        返回值:{responses}
        寄语:{description}
        """
    else:
        body_content = f"""
        {time.strftime('%Y-%m-%d %H:%M:%S')}签到失败!!!
        失败原因:{responses}
        """
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_content, "plain", "utf-8")
    # 向MIMEMultipart对象中添加文本对象
    mm.attach(message_text)

    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    stp.set_debuglevel(1)
    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender, mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    # print("邮件发送成功")
    # 关闭SMTP对象
    stp.quit()

if __name__=='__main__':
    Authorization=log()
    planId = planId(Authorization)
    responses,description = sin(Authorization,planId)
    file_operation(filename)
    send_out_mail(responses,description)

