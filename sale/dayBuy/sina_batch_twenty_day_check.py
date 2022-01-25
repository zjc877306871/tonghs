
import json
import pandas as pd
from threading import Timer
import time
import tonghs
import timeApi
import stringApi
from redisSelf import redisSelf
from logger.logger import Logger
from concurrent.futures import ThreadPoolExecutor
from entity.StockSelf import Stock
import httpClientSina
def Time_threading(inc):

    times = ['10:02','10:32','11:02','13:02','13:32','14:02','14:32']
    time_last = '15:17'

    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = timeApi.get_hource()
    if time_now == time_last:
        print(time_now)
        try:
            df = batch_stock_data('26',60,80,8,1)
        except BaseException:
            df = batch_stock_data('26',60,80,8,1)
        # 获取最后满足的20日线条件
        key = 'twenty:'+ timeApi.formart_date('','%Y%m%d')+':1500'
        conn = redisSelf.getRedisConnection()
        # if(len(df) > 2):
        conn.set(key,df)
    i = 2
    for time in times:
        if time_now == time:
            log.logger.info(time)
            try:
                df = batch_stock_data('26',60,(76+int((i-i%2)/2+i%2)),i,0)
            except BaseException:
                df = batch_stock_data('26',60,(76+int((i-i%2)/2+i%2)),i,0)
            if i == 8:
                # 汇集了3:00之前的满足条件的数据
                key = 'next:twenty:'+ timeApi.formart_date('','%Y%m%d:')+ stringApi.changeStr(time_now,'0')
            else:
                # 分别记录各个时间的数据
                key = 'record:twenty:'+ timeApi.formart_date('','%Y%m%d:')+ stringApi.changeStr(time_now,'0')
            conn = redisSelf.getRedisConnection()
            print(len(df))
            # if(len(df) > 2):
            conn.set(key,df)
        i = i+1


#         批量处理数据
def batch_stock_data(id,scale,data_len,index,flage):
    symsols = tonghs.get_ths_data(id)
    log.logger.info('二十日选择总量'+ str(len(symsols)))
    bar_list = []
    for symsol in symsols:
        # 异步多线程
        executor = ThreadPoolExecutor(10)
        future =  executor.submit(asnyDealData,symsol,scale,data_len,index,flage)
        stock = future.result()
        if stock:
            dict = stock.stock2dict()
            bar_list.append(dict)

    df = pd.DataFrame(data=bar_list)
    print(df)
    df = json.dumps(bar_list)
    log.logger.info('二十日选出结果'+df)
    return df

def asnyDealData(symsol,scale,data_len,index,flage):

    sum_list = get_stock_data_60(symsol,scale,data_len)
    stock = get_stock_data_30(symsol,30,index,sum_list,flage)
    return stock
#测试
def batch_stock_data_test(id,scale,data_len,index,flage):
    symsols = {'sz000408'}
    bar_list = []
    for symsol in symsols:
        sum_list = get_stock_data_60(symsol,scale,data_len)
        get_stock_data_30(symsol,30,index,sum_list,bar_list,flage)

    df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
    print(df)

def get_stock_data_30(id,scale,data_len,sum_list,flage):

    res_json = httpClientSina.http_stock_data(id,scale,data_len)
    # print(res_json)
    stock = select_now_gp(res_json,id,data_len,sum_list,flage)
    return stock
    # print('历史的数据：',sum_list)

def get_stock_data_60(id,scale,data_len):
    # bar_list = []
    res_json = httpClientSina.http_stock_data(id,scale,data_len)
    # print(res_json)
    sum_list = select_his_gp(res_json,id,data_len)
    return sum_list

def select_his_gp(res_json,symsol,data_len):
    newCloseRice = float(0.00)
    lastFourVolume = 0
    lastFourPrice = float(0.00)
    lastDayClosePrice = float(0.00)
    i = 0
    sum_list = []
    for dict in res_json:
        day = dict['day'][:10]
        hour = dict['day'][11:]
        nowDay = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10]
        # 获取当天的数据，成交量/开盘价/收盘价/最高价
        if (hour == '15:00:00') & (i != 0):
            #获取历史的收盘价，收盘价
            newCloseRice = newCloseRice + float(dict['close'])

        if 0==data_len%4:
            # 处理当日最后一次跑数
            if (i < (data_len%4+20)) & (i >= (data_len%4)) & (hour == '15:00:00') & (i != 0):
                #     获取最近4天的收盘价
                lastFourPrice = lastFourPrice + float(dict['close'])

            if (i < (data_len%4)+20) & (i > 3):
                #     获取最近4天的历史成交量
                lastFourVolume = lastFourVolume + int(dict['volume'])
                # print(i)
                # print(lastFourVolume)
            if (i== 4):
                #     获取前一日的收盘价
                lastDayClosePrice = float(dict['close'])
        else:
            if (i < (data_len%4+16)) & (i >= (data_len%4)) & (hour == '15:00:00') & (i != 0):
                #     获取最近4天的收盘价
                lastFourPrice = lastFourPrice + float(dict['close'])

            if (i < (data_len%4+20)) & (i > (data_len%4 -1)):
                #     获取最近4天的历史成交量
                lastFourVolume = lastFourVolume + int(dict['volume'])

            if (i== (data_len%4)):
                #     获取前一日的收盘价
                lastDayClosePrice = float(dict['close'])
        i += 1
        # print(i)
    bar = {}
    bar['newCloseRice'] = newCloseRice
    bar['lastFourVolume'] = lastFourVolume
    bar['lastFourPrice'] = lastFourPrice
    bar['lastDayClosePrice'] = lastDayClosePrice
    sum_list.append(bar)
    return sum_list


def select_now_gp(res_json,symsol,data_len,sum_list,flage):
    nowCloseRice = float(0.00)
    nowOpenRice = float(0.00)
    nowMaxPrice = {float(0.00)}
    lastVolume = 0
    i = 0
    for dict in res_json:
        # 汇集最高价
        nowMaxPrice.add(float(dict['high']))
        # 获取当天的数据，成交量/开盘价/收盘价/最高价
        #获取历史的收盘价，收盘价/成交量
        if i == 0:
            # 获取最新收盘
            nowCloseRice = float(dict['close'])
        if i == data_len-1:
            #获取当日开盘
            nowOpenRice = float(dict['open'])
        # if i != 0:
        lastVolume = lastVolume + int(dict['volume'])

        i += 1

    # 进行决策判断
    bar = sum_list[0]
    newCloseRice = bar['newCloseRice']
    lastFourVolume = bar['lastFourVolume']
    lastFourPrice = bar['lastFourPrice']
    lastDayClosePrice = bar['lastDayClosePrice']
    newCloseRice = round(newCloseRice + nowCloseRice, 2)
    fivePriceSum = round(lastFourPrice + nowCloseRice,2)
    lastFourVolume = lastFourVolume+lastVolume
    # 20日均价
    twentyPrice = round(newCloseRice/20,2)
    # 5日均量
    fiveVolume = lastFourVolume/5
    #5日均价
    fivePrice = round(fivePriceSum/5, 2)
    dayMax = compare(nowMaxPrice)
    shangYingPrice =  round(dayMax-nowCloseRice, 2)
    shiTiPrice =  round(nowCloseRice-nowOpenRice, 2)
    dayZhangFu =  round(nowCloseRice-lastDayClosePrice, 2)
    scale = round(dayZhangFu/lastDayClosePrice*100, 2)
    if 0==flage:
        if (nowOpenRice<fivePrice) & (nowCloseRice>fivePrice) & (lastVolume>fiveVolume)& (scale >7):
            stock = Stock(symsol,nowCloseRice)
            print("选到了",symsol)
            return stock
    else:
        if (nowOpenRice<fivePrice) & (nowCloseRice>fivePrice) & (lastVolume>fiveVolume) & (shiTiPrice>shangYingPrice) &(scale<6):
            stock = Stock(symsol,nowCloseRice)
            print("选到了",symsol)
            return stock
#函数调用 60标识一分钟
# Time_threading(60)
# get_stock_data('sz000681',60,80)


def compare(setInts):
    maxInt = float(0.00)
    for setInt in setInts:
        if setInt>maxInt:
            maxInt = setInt
    return maxInt
log = Logger("D:\logs\长期日\info.txt")
Time_threading(60)
# batch_stock_data_test('26',60,80,8,0)
# batch_stock_data_test('26',60,80,7,0)