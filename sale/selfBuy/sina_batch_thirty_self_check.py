

from logger.logger import Logger
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import tonghs
import timeApi


def Time_threading(inc):
    times = ['10:01']
    time_last = '16:21'

    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = get_hource()
    for time in times:
        if time_now == time_last:
            print(time_now)
            df = get_stock_data('EE',30,20)
            log.logger.info("结束时间: " + timeApi.formart_date('','%Y-%m-%d %H:%M:%S'))
            log.logger.info("选到了: " +df)
            break
        else:
            if time_now == time:
                log.logger.info(time_now)
                df = get_stock_data('EE',30,22)
                log.logger.info("结束时间: " + timeApi.formart_date('','%Y-%m-%d %H:%M:%S'))
                log.logger.info("选到了: " +df)
    # df.head()
def get_stock_data_check(id,scale,data_len):
    symsols = tonghs.get_self_data()
    print(symsols)
    scale = scale
    data_len = data_len
    bar_list = []
    for symsol in symsols:
        res_json = http_stock_data(symsol,scale,data_len)
        # 具体的筛选逻辑
        select_gp_check(res_json,bar_list,symsol,data_len)
    df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
    print("选到了: " ,df)

def get_stock_data(id,scale,data_len):
    symsols = tonghs.get_self_data()
    log.logger.info('自选总量{}'+str(len(symsols)))
    scale = scale
    data_len = data_len
    bar_list = []
    for symsol in symsols:
        res_json = http_stock_data(symsol,scale,data_len)
        # 具体的筛选逻辑
        select_gp(res_json,bar_list,symsol,data_len)
    # df = pd.DataFrame(data=bar_list)
    df = json.dumps(bar_list)
    return df
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
def select_gp(res_json,bar_list,symsol,data_len):
    fivePriceSum = float(0.00)
    lastDayClosePrice = float(0.00)
    newCloseRice = float(0.00)
    newOpenRice = float(0.00)
    newFiveVolume = 0
    newVolume = 0
    newScale = float(0.00)
    newShangYing = float(0.00)
    newShiTi = float(0.00)
    i = 0
    for dict in res_json:
        # 获取10点前20个的收盘价
        if (0 != i):
            close = float(dict['close'])
            fivePriceSum = fivePriceSum + close
        #获取9：30-10：00的数据的
        if 1== i:
            newCloseRice = float(dict['close'])
            newOpenRice = float(dict['open'])
            newFiveVolume = int(dict['ma_volume5'])
            newVolume = int(dict['volume'])
            newMaxPrice = float(dict['high'])
            newMinPrice = float(dict['low'])
            newShangYing = newMaxPrice-newCloseRice;
            newShiTi = newCloseRice-newOpenRice

        # 获取前一日的收盘价
        if 2== i:
            lastDayClosePrice = float(dict['close'])
        # 计算9：30-10：00的30分钟的5均线
        if (i == 5):
            fivePrice = fivePriceSum/5
        i += 1
    newScale = (newCloseRice-lastDayClosePrice)/lastDayClosePrice*100
    if (newOpenRice < fivePrice) & (newCloseRice > fivePrice) & (newVolume > newFiveVolume) &(newShiTi > newShangYing) & (newScale < 4 ):
        bar_list.append(symsol)
        # print("选到了",bar_list)


def select_gp_check(res_json,bar_list,symsol,data_len):
    fivePriceSum = float(0.00)
    lastDayClosePrice = float(0.00)
    newCloseRice = float(0.00)
    newOpenRice = float(0.00)
    newFiveVolume = 0
    newVolume = 0
    newScale = float(0.00)
    newShangYing = float(0.00)
    newShiTi = float(0.00)
    i = 0
    for dict in res_json:
        # 获取10点前20个的收盘价
        if (0 != i) & (1 != i) &(2 != i) &(3 != i)&(4 != i):
            close = float(dict['close'])
            print(close)
            fivePriceSum = fivePriceSum + close
        #获取9：30-10：00的数据的
        if 5== i:
            newCloseRice = float(dict['close'])
            newOpenRice = float(dict['open'])
            newFiveVolume = int(dict['ma_volume5'])
            newVolume = int(dict['volume'])
            newMaxPrice = float(dict['high'])
            newMinPrice = float(dict['low'])
            newShangYing = newMaxPrice-newCloseRice;
            newShiTi = newCloseRice-newOpenRice

        # 获取前一日的收盘价
        if 6== i:
            lastDayClosePrice = float(dict['close'])
        # 计算9：30-10：00的30分钟的5均线
        if (i == 9):
            fivePrice = fivePriceSum/5
        i += 1
    newScale = (newCloseRice-lastDayClosePrice)/lastDayClosePrice*100
    if (newOpenRice < fivePrice) & (newCloseRice > fivePrice) & (newVolume > newFiveVolume) &(newShiTi > newShangYing) & (newScale < 4 ):
        bar_list.append(symsol)
        # print("选到了",bar_list)
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
#函数调用 60标识一分钟
log = Logger("D:\logs\自选\info.txt")
Time_threading(60)
# get_stock_data_check(1,30,10)