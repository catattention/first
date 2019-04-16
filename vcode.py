#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from PIL import Image
import numpy as np
from numpy import linalg as la
import os

import datetime
import time

def getNowMilliTime():
    return int(time.time() * 1000)

def arrayToDate(arr):
    timestamp = datetime.datetime(int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5]))
    return timestamp

def ecludSim(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))

def goThroughFolder(path):   
    list = os.listdir(path) #列出文件夹下所有的目录与文件
    return list

def imgTo2Value(data):   
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if data[y,x] < 175:
                data[y,x] = 0
            else:
                data[y,x] = 255
    
    return data

def imageToArrayByPath(path):    
    im = Image.open(path)
    width = im.width
    height = im.height
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data)
    # 变换成数组
    data = np.reshape(data,(height,width))    
    return data

def imageToArrayByObject(im):
    width = im.width
    height = im.height
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data)
    # 变换成数组
    data = np.reshape(data,(height,width))    
    return data

def arrayToImage(data,path):
    im = Image.fromarray(data).convert("RGB")
    im.save(path)
    return im

##
#对比基准图片存储在0~9文件夹中
#获取各个文件夹中对应的基准图片，转成矩阵，形成10个数组备用
##
def baseCompareData():
    compareArr = []
    # 基准数据
    for i in range(10):
        path = "yanzhengma/"+str(i)+"/"
        list = goThroughFolder(path)
        wbArr = []
        for i in range(0,len(list)):
            mat = imageToArrayByPath(path + list[i])
            #print(path + list[i]) #TEST
            wbArr.append(mat)
        compareArr.append(wbArr)
    return compareArr
##
# 分析二值图片，计算各个数字边界
##
def calcBorderline(ashImage):
    arr = []
    charWidth = 7
    data = imageToArrayByObject(ashImage)
    #循环每列，获取每列黑色像素个数
    for c in range(data.shape[1]):
        lieArr = data[:,c]
        arr.append(np.sum(lieArr == 0))
    #获取最小黑色像素个数
    minNum = np.min(arr)
    #每列黑色像素个数减掉最小个数（排除顶端黑条）
    arr1 = [c - minNum for c in arr]

    charBoxs = []
    #循环列，前一列是黑像素个数为0，后一列黑像素个数大于1，则将其作为一个字符的开始
    for i in range(len(arr1)-1):
        if (arr1[i] == 0) & (arr1[i+1] > 1):
            box = tuple(eval("("+str(i+1)+",1,"+str(i+1+charWidth)+","+str(ashImage.height)+")"))
            charBoxs.append(box)
    return charBoxs

##
#拿截取到的单个字符图片矩阵与所有基准矩阵对比
#取相似度最大的情况作为返回值；如果相似度小于0.001，将该图片保存到待学习文件夹
##
def identifyNumber(aMat,matArray):
    maxMatchDegree = 0
    resultValue = "X"
    resultArr = []
    for i in range(len(matArray)):
        for j in range(len(matArray[i])):
            #arrayToImage(matArray[i][j],"yanzhengma/compareMat.png")
            #arrayToImage(aMat,"yanzhengma/codeMat.png")
            matchDegree = ecludSim(aMat,matArray[i][j])
            if matchDegree > maxMatchDegree :
                maxMatchDegree = matchDegree
                resultValue = str(i)
    resultArr.append(resultValue)
    if maxMatchDegree < 0.01:
        resultArr.append(0)   #图片要进行学习
    else:
        resultArr.append(1)   #图片无需处理
    #print(resultArr) #TEST
    return resultArr

##
# 切割图片
# 验证码图片读取，切割成4个小图片，分别转成矩阵
# 调用identifyNumber方法，返回数字，同时根据匹配度判断是否需要将该图片作为对比基准
##
def getCode(codeImage):
    compareArr = baseCompareData()
    #获取图片对象，二值化并保存为二值图片
    codeData = imageToArrayByObject(codeImage)
    codeData = imgTo2Value(codeData)
    ashImage = arrayToImage(codeData,"yanzhengma/ashCode.png")
    
    vcode = ""
    #分析二值图片，计算各个数字边界，进行切割
    charBoxs = calcBorderline(ashImage)
    for i in range(len(charBoxs)):
        char = ashImage.crop(charBoxs[i])
        char.convert("RGB").save("yanzhengma/char"+str(i)+".png")
        mat_yzm = imageToArrayByObject(char)
        resultArr = identifyNumber(mat_yzm,compareArr)        
        vcode = vcode + resultArr[0]
        if resultArr[1] == 0:
            imageName = str(getNowMilliTime())
            arrayToImage(mat_yzm,"yanzhengma/needToLearn/"+imageName+".png")
    return vcode
