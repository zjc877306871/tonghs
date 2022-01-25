
from logger.logger import Logger
from urllib import request
import json
import pandas as pd
from threading import Timer
import tonghs
import timeApi
import stringApi
from redisSelf import redisSelf
from concurrent.futures import ThreadPoolExecutor
from entity.StockSelf import Stock
import httpClientSina

def Time_threading(inc):
    times = ['10:38','11:01','13:01','13:31','14:01','14:31']
    time_last = '17:31'
    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = timeApi.get_hource()
    for time in times:
        i = 3
        if time_now == time_last:
            print(time_now)
            df = ''
            try:
                df = get_stock_data('EE',30,20)
            except BaseException:
                df = get_stock_data('EE',30,20)
            log.logger.info("结束时间: " + timeApi.formart_date('','%Y-%m-%d %H:%M:%S'))
            log.logger.info("选到了: " +df)
            # if(len(df) > 2):
            key = 'two:'+ timeApi.formart_date('','%Y%m%d')+':1500'
            conn = redisSelf.getRedisConnection()
            conn.set(key,df)
            break
        else:
            if time_now == time:
                log.logger.info(time_now)
                df = ''
                try:
                    df = get_stock_data('EE',30,21)
                except BaseException:
                    df = get_stock_data('EE',30,21)
                log.logger.info("结束时间: " + timeApi.formart_date('','%Y-%m-%d %H:%M:%S'))
                log.logger.info("选到了: " +df)
                # if(len(df) > 2):
                key = 'two:'+ timeApi.formart_date('','%Y%m%d:')+ stringApi.changeStr(time_now,'0')
                conn = redisSelf.getRedisConnection()
                conn.set(key,df)
        i = i+1
    # df.head()
def get_stock_data(id,scale,data_len):

    symsols = tonghs.get_ths_data(id)
    log.logger.info('三十分钟二买总量'+str(len(symsols)))
    scale = scale
    data_len = data_len
    bar_list = []

    for symsol in symsols:

        executor = ThreadPoolExecutor(5)
        future =  executor.submit(asnyDealData,symsol,scale,data_len)
        ansy_list = future.result()

    df = pd.DataFrame(data=bar_list)
    if ansy_list:
        bar_list.append(ansy_list)
    df = json.dumps(bar_list)
    return df
# 异步任务封装
def asnyDealData(symsol,scale,data_len):
    res_json = httpClientSina.http_stock_data(symsol,scale,data_len)
    # 具体的筛选逻辑
    stock = select_gp(res_json,symsol,data_len)
    return stock


def select_gp(res_json,symsol,data_len):
    twentyPriceSum = float(0.00)
    nowCloseRice = float(0.00)
    nowOpenRice = float(0.00)
    nowMaxRice = float(0.00)
    nowFiveVolume = 0
    nowVolume = 0
    i = 0
    for dict in res_json:
        # 处理当日最后一个30分钟的筛选
        if 20 == data_len:
            if 0 == i:
                nowCloseRice = float(dict['close'])
                nowOpenRice = float(dict['open'])
                nowFiveVolume = int(dict['ma_volume5'])
                nowVolume = int(dict['volume'])
                nowMaxRice = float(dict['high'])
                day = dict['day']
            close = float(dict['close'])
            twentyPriceSum = round(twentyPriceSum + close, 2)
            #获取前一个的收盘价
            if 1== i:
                lasteClosePrice =  float(dict['close'])
            if (20 == data_len) & (i == 19):
                stock = get_result_gp(twentyPriceSum,nowCloseRice,nowOpenRice,nowMaxRice,lasteClosePrice,nowVolume,nowFiveVolume,symsol,day)
                return stock
        elif  21 == data_len:
            if 0 != i:
                close = float(dict['close'])
                twentyPriceSum = round(twentyPriceSum + close,2)
            if 1 == i:
                nowCloseRice = float(dict['close'])
                nowOpenRice = float(dict['open'])
                nowFiveVolume = int(dict['ma_volume5'])
                nowVolume = int(dict['volume'])
                nowMaxRice = float(dict['high'])
                day = dict['day']
            if 2==i:
                lasteClosePrice =  float(dict['close'])
            if (21 == data_len) & (i == 20):
                stock = get_result_gp(twentyPriceSum,nowCloseRice,nowOpenRice,nowMaxRice,lasteClosePrice,nowVolume,nowFiveVolume,symsol,day)
                return stock
        i += 1


def get_result_gp(twentyPriceSum,nowCloseRice,nowOpenRice,nowMaxRice,lasteClosePrice,nowVolume,nowFiveVolume,symsol,day):
    twentyPrice = round(twentyPriceSum/20,2)
    shiTiPrice = round(nowCloseRice-nowOpenRice,2)
    shangYingPrice = round(nowMaxRice-nowCloseRice,2)
    shangZhangPrice = round(nowCloseRice-lasteClosePrice,2)
    scale = round((shangZhangPrice/lasteClosePrice)*100,2)
    if (nowOpenRice<twentyPrice) & (nowCloseRice>twentyPrice) & (nowVolume>nowFiveVolume) &(shiTiPrice>shangYingPrice)&(scale<3):
        stock = Stock(symsol, nowCloseRice,day)
        return stock


# def get_stock_data_check(id,scale,data_len):
#
#     symsols = {'sh600775'}
#     scale = scale
#     data_len = data_len
#     bar_list = []
#
#     for symsol in symsols:
#         # print("开始",symsol)
#         res_json = http_stock_data(symsol,scale,data_len)
#         # 具体的筛选逻辑
#         stock = select_gp(res_json,symsol,data_len)
#         bar_list.append(stock)
#     df = pd.DataFrame(data=bar_list)
#
#     return df
#函数调用 60标识一分钟
log = Logger("D:\logs\二买\info.txt")
Time_threading(60)
# get_stock_data_check('EE',30,21)