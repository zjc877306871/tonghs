

from matplotlib import font_manager
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import time
import tonghs
import iniFile.iniWrite


def Time_threading(inc):

    times = {}
    time_last = '15:10'

    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = get_hource()


    if time_now == time_last:
        print(time_now)
        df = batch_stock_data('ef',60,80)

def batch_stock_data(id,scale,data_len):
    symsols = tonghs.get_ths_data(id)
    print('二十日总量',len(symsols))
    bar_list = set()
    for symsol in symsols:
        get_stock_data_60(symsol,scale,data_len,bar_list)
        # get_stock_data_30(symsol,30,index,sum_list,bar_list,flage)
    # iniFile.iniWrite.get_ths_data(id,iniFile.iniWrite.tranName(bar_list))
    # df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
    print(bar_list)
def http_stock_data(id,scale,data_len):
    id = id
    scale = scale
    data_len = data_len
    url = 'http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}'.format(id, scale, data_len)
    req = request.Request(url)
    rsp = request.urlopen(req)
    res = rsp.read()
    res_json = json.loads(res)
    res_json.reverse()
    return  res_json




def get_stock_data_60(id,scale,data_len,bar_list):
    # bar_list = []
    res_json = http_stock_data(id,scale,data_len)
    # print(res_json)
    select_his_gp(res_json,id,data_len,bar_list)

def select_his_gp(res_json,symsol,data_len,bar_list):
    newCloseRice = float(0.00)
    lastThreeDayClosePrices = []
    i = 0
    sum_list = []
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
        # print(i)
    twentyDayPrice = round(newCloseRice/20,2)
    j = 0
    for lastThreeDayClosePrice in lastThreeDayClosePrices:
        if lastThreeDayClosePrice>twentyDayPrice:
            j = 1
    if 0==j:
        print(symsol[2:])
        bar_list.add(symsol[2:])

#函数调用 60标识一分钟
# Time_threading(60)
# get_stock_data('sz000681',60,80)

#获取当前时间分钟
def get_hource():
    hour = datetime.now().hour
    minute = datetime.now().minute
    # print(datetime.now())
    h = str(hour)
    m = str(minute)
    if 1 == len(m):
        m = '0'+ m
    mm = h + ':' + m
    return mm

def compare(setInts):
    maxInt = float(0.00)
    for setInt in setInts:
        if setInt>maxInt:
            maxInt = setInt
    return maxInt

# Time_threading(60)
batch_stock_data('26',60,80)