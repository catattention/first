#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import time
import cut  # TEST


# 方法定义
def addHour(timestamp, addValue):
    timestamp = timestamp + datetime.timedelta(hours=addValue)
    return timestamp


def addDay(timestamp, addValue):
    timestamp = timestamp + datetime.timedelta(days=addValue)
    return timestamp


def arrayToDate(arr):
    timestamp = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]))
    return timestamp


def propertiesToArray(path):
    f = open(path, "r")
    data = f.readlines()
    f.close()
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")

    return data


def arrayToProperties(data, path):
    f = open(path, "w")
    content = ""
    for i in range(len(data)):
        content = content + str(data[i]) + "\n"
    f.write(content)
    f.close()


def todayWorkday(curDate):
    curDateStr = curDate.strftime('%Y%m%d')
    # 首先判断是否是工作日，如果是再判断是否包含在排除列表中，如果在，调用nextWorkday获取下一个打卡日，否则今天
    if (curDate.weekday() < 5):
        if (exDate.find(curDateStr) >= 0):
            return nextWorkday(curDate)
        else:
            return curDate
    # 如果是周末，判断是否包含在包含列表中，如果包含返回今天，否则获取下一个打卡日
    else:
        if (inDate.find(curDateStr) >= 0):
            return curDate
        else:
            return nextWorkday(curDate)

def nextWorkday(curDate):
    nextDate = addDay(curDate, 1)
    nextDateStr = nextDate.strftime('%Y%m%d')
    # 首先判断是否是工作日，如果是再判断是否包含在排除列表中，如果在递归，否则返回
    if (nextDate.weekday() < 5):
        if (exDate.find(nextDateStr) >= 0):
            return nextWorkday(nextDate)
        else:
            return nextDate
    # 如果是周末，判断是否包含在包含列表中，如果包含返回，否则递归
    else:
        if (inDate.find(nextDateStr) >= 0):
            return nextDate
        else:
            return nextWorkday(nextDate)


# 参数准备
data = propertiesToArray("data.txt")

firstHour = int(data[4])
secondHour = int(data[6])
firstMinute = int(data[5])
secondMinute = int(data[7])
couldDelay = int(data[8])
inDate = data[12].replace("in:[", "").replace("]", "")
exDate = data[13].replace("ex:[", "").replace("]", "")

while True:
    now = datetime.datetime.now()
    #now = datetime.datetime(2019,4,12,18,52,17)   #TEST
    print("现在：%s" % now)

    lastcut = propertiesToArray("lastcut.txt")
    last = arrayToDate(lastcut)
    print("上次：%s" % last)

    # 正常区间包括
    firstEarliest = datetime.datetime(now.year, now.month, now.day, firstHour, firstMinute, 0)
    firstLatest = firstEarliest + datetime.timedelta(seconds=couldDelay)
    secondEarliest = datetime.datetime(now.year, now.month, now.day, secondHour, secondMinute, 0)
    secondLatest = secondEarliest + datetime.timedelta(seconds=couldDelay)

    # 先定义下一次打卡时间
    tmpDate = todayWorkday(now)
    tmpDateStr = tmpDate.strftime('%Y%m%d')
    nowStr = now.strftime('%Y%m%d')
    nextYear = tmpDate.year
    nextMonth = tmpDate.month
    nextDay = tmpDate.day
    nextHour = firstHour
    nextMinute = firstMinute

    # 当前时间在早上打卡时间区间内
    if (now >= firstEarliest) & (now <= firstLatest):
        # 判断上次打卡时间早于早上打卡时间，开始打卡
        if last <= firstEarliest:
            print("早上打卡")
            cut.dk()  # TEST
        # 计算下次打卡时间
        if (tmpDateStr == nowStr):
            nextHour = secondHour
            nextMinute = secondMinute
    # 不在正常打卡时间内，晚于上午打卡，早于晚上打卡时间，将最近一次打卡时间设置为晚上正常打卡时间
    elif (now >= firstLatest) & (now <= secondEarliest):
        if (tmpDateStr == nowStr):
            nextHour = secondHour
            nextMinute = secondMinute
    # 当前时间在晚上打卡时间区间内，晚上正常打卡开始时间~24点
    elif (now >= secondEarliest):
        # 晚上已经打过卡，设置下次打卡时间为下个工作日早上打卡时间
        if last >= secondEarliest:
            nextDate = nextWorkday(now)
            nextYear = nextDate.year
            nextMonth = nextDate.month
            nextDay = nextDate.day
            nextHour = firstHour
            nextMinute = firstMinute
        # 晚上还没有打卡
        else:
            nineHourLater = addHour(last, 9.5)
            # 现在时间距离上次（可能今天/或以前）打卡超过9小时，打卡，并设置下次打卡时间为下个工作日早上打卡时间
            if now >= nineHourLater:
                print("晚上打卡")
                cut.dk()  # TEST
                nextDate = nextWorkday(now)
                nextYear = nextDate.year
                nextMonth = nextDate.month
                nextDay = nextDate.day
                nextHour = firstHour
                nextMinute = firstMinute
            else:
                # 现在时间距离早上打卡尚未超过9小时，设置下次打卡时间为早上打卡时间+9小时
                nextDay = nineHourLater.day
                nextHour = nineHourLater.hour
                nextMinute = nineHourLater.minute
    # 不在正常打卡时间内，0点~早上正常打卡开始时间，将最近一次打卡时间设置为当日早上正常打卡时间
    else:
        if (tmpDateStr == nowStr):
            nextHour = firstHour
            nextMinute = firstMinute

    next = datetime.datetime(nextYear, nextMonth, nextDay, nextHour, nextMinute, 0)
    diff = next - now
    diffSeconds = diff.days * 24 * 60 * 60 + diff.seconds + 1
    print("下次：%s" % next)
    print("还剩：%s 秒" % (diffSeconds))

    time.sleep(diffSeconds)
    # TEST:time.sleep(10)