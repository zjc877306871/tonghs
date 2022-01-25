
import json
from datetime import datetime
from threading import Timer
import time
import tonghs
from logger.logger import Logger
from concurrent.futures import ThreadPoolExecutor
import httpClientSina
import timeApi

def Time_threading(inc):
    time_last = '15:10'

    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = timeApi.get_hource()

    if time_now == time_last:
        print(time_now)
        df = batch_stock_data('ef',60,80)

def batch_stock_data(id,scale,data_len):
    symsols = []
    symsols.append(id)
    print('检查的代码'+symsols)
    bar_list = []
    for symsol in symsols:
        executor = ThreadPoolExecutor(10)
        future =  executor.submit(get_stock_data_60,symsol,scale,data_len)
        ansy_list = future.result()
        if ansy_list:
            bar_list.append(ansy_list)
    bar_list.sort()
    log.logger.info('result:'+json.dumps(bar_list))

def get_stock_data_60(id,scale,data_len):
    res_json = httpClientSina.http_stock_data(id,scale,data_len)
    bar_list = select_his_gp(res_json,id)
    return bar_list


def select_his_gp(res_json,symsol):
    newCloseRice = float(0.00)
    lastThreeDayClosePrices = []
    i = 0
    for dict in res_json:
        day = dict['day'][:10]
        hour = dict['day'][11:]
        nowDay = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10]
        # 获取当天的数据，成交量/开盘价/收盘价/最高价
        if (hour == '15:00:00') & (i == 0):
            nowClosePrice = float(dict['close'])
            lastThreeDayClosePrices.append(nowClosePrice)
        if (hour == '15:00:00') & (i == 4):
            nowClosePrice = float(dict['close'])
            lastThreeDayClosePrices.append(nowClosePrice)
        if (hour == '15:00:00') & (i == 8):
            nowClosePrice = float(dict['close'])
            lastThreeDayClosePrices.append(nowClosePrice)

        if (hour == '15:00:00') :
            #获取历史的收盘价，收盘价
            newCloseRice = round(newCloseRice + float(dict['close']),2)
        i += 1
    twentyDayPrice = round(newCloseRice/20,2)
    j = 0
    for lastThreeDayClosePrice in lastThreeDayClosePrices:
        if lastThreeDayClosePrice>twentyDayPrice:
            j = 1
    if 0==j:
        print(symsol[2:])
        return symsol[2:]

def compare(setInts):
    maxInt = float(0.00)
    for setInt in setInts:
        if setInt>maxInt:
            maxInt = setInt
    return maxInt

# Time_threading(60)
log = Logger("D:\logs\长期日\delete.txt")
batch_stock_data('26',60,80)
