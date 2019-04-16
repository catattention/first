#!/usr/bin/env python
# coding:utf-8
from selenium import webdriver
import urllib.request
import socket
import urllib.error

from PIL import Image
import datetime
import time
import random

import vcode as vc

def propertiesToArray(path):    
    f = open(path,"r")
    data = f.readlines()
    f.close()
    for i in range(len(data)):
        data[i] = data[i].replace("\n","")
    
    return data

def arrayToProperties(data,path):    
    f = open(path,"w")
    content = ""
    for i in range(len(data)):
        content = content + str(data[i])+"\n"
    f.write(content)
    f.close()

def dk():
    data = propertiesToArray("data.txt")
    randS = int(data[2])
    randE = int(data[3])
    sleepSecond = random.randint(randS,randE) #52,597
    print(sleepSecond)
    time.sleep(sleepSecond)
    
    #获取失败尝试参数
    paraTryGroups = int(data[9])
    paraTryTimes = int(data[10])
    paraIntervalTimes = int(data[11])

    tryGroups = 0
    tryTimes = 0

    while True:
        try:
            response = urllib.request.urlopen('http://kq.neusoft.com/index.jsp', timeout=1)
            
            wbe = webdriver.Chrome()
            wbe.get("http://kq.neusoft.com/index.jsp")
            tryTimes = 0
            tryGroups = 0
            break
        
        except urllib.error.URLError as e:
            print(e.reason)
            if isinstance(e.reason, socket.timeout):
                print('连接超时')
            time.sleep(3)
            tryTimes += 1
            if tryTimes == paraTryTimes:
                tryGroups += 1
                if tryGroups == paraTryGroups:
                    print("连接失败次数已经超过最大限制。")
                    return
                tryTimes = 0
                time.sleep(paraIntervalTimes)

    while True:
        time.sleep(2)
        element = wbe.find_element_by_id('imgRandom')
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']
        wbe.save_screenshot("yanzhengma/homepage.png")
        codeImage = Image.open(r'yanzhengma/homepage.png')
        codeImage = codeImage.crop((left, top, right, bottom))

        #TEST:查看生成的彩色四位验证码    
        #codeImage = codeImage.convert("RGB")
        #codeImage.save('yanzhengma/yzm.jpg')
        #time.sleep(2)
        
        vcode = vc.getCode(codeImage)
        print(vcode)
        if vcode.find('X') > 0:
            print("o╥﹏╥o")
            wbe.find_element_by_id('imgRandom').click()
            tryTimes += 1
            time.sleep(3)
            if tryTimes == paraTryTimes:
                tryGroups += 1
                if tryGroups == paraTryGroups:
                    print("验证码读取错误次数已经超过最大限制，验证码读取算法不够严谨，可能需要检修了~~o╥﹏╥o")
                    break
                tryTimes = 0
                time.sleep(paraIntervalTimes)
        else:
            elements = wbe.find_elements_by_class_name('textfield')
            wbe.execute_script("arguments[0].value = '" + data[0].replace("\n","") + "';", elements[0])
            wbe.execute_script("arguments[0].value = '" + data[1].replace("\n","") + "';", elements[1])
            element = wbe.find_element_by_class_name('a')
            wbe.execute_script("arguments[0].value = '" + vcode + "';", element)
            
            wbe.find_element_by_id('loginButton').click()
            time.sleep(4)
            if 'http://kq.neusoft.com/index.jsp?error=1' == wbe.current_url:
                print('用户名或密码错误。')
                break
            if 'attendance' in wbe.current_url:
                wbe.find_element_by_class_name('mr36').click()
                # 更新上次打卡时间
                now = datetime.datetime.now()                
                data = [str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second)]
                arrayToProperties(data,"lastcut.txt")
                break
    wbe.close()

if __name__ == '__main__':
    dk()
