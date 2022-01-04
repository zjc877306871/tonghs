

from matplotlib import font_manager
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import tonghs


def Time_threading(inc):
    times = ['10:31','11:01','13:01','13:31','14:01','14:31']
    time_last = '14:53'

    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = get_hource()
    for time in times:
        i = 3
        if time_now == time_last:
            print(time_now)
            df = get_stock_data('EE',30,20)
            break
        else:
            if time_now == time:
                print(time_now)
                df = get_stock_data('EE',30,21)
            # df.to_csv("D:\finance\gp\数据\1111_stock.csv", encoding="gbk", index=False)
            # else:
                # print('围在时间内： ',datetime.now())
            # df.to_csv("D:\finance\gp\数据\1111_stock.csv", encoding="gbk", index=False)
        # else:
            # print('围在时间内： ',datetime.now())
        i = i+1
    #导入到excel

    # print(df)
    # df.head()
def get_stock_data(id,scale,data_len):

    symsols = tonghs.get_ths_data(id)
    print('三十分钟二买总量',len(symsols))
    scale = scale
    data_len = data_len
    bar_list = []

    for symsol in symsols:
        # print("开始",symsol)
        res_json = http_stock_data(symsol,scale,data_len)
        # 具体的筛选逻辑
        select_gp(res_json,bar_list,symsol,data_len)
    df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
    print("结束时间: " ,datetime.now())
    print("选到了: " ,df)
    return df
def get_stock_data_check(id,scale,data_len):

    symsols = {'sh600775'}
    scale = scale
    data_len = data_len
    bar_list = []

    for symsol in symsols:
        # print("开始",symsol)
        res_json = http_stock_data(symsol,scale,data_len)
        # 具体的筛选逻辑
        select_gp(res_json,bar_list,symsol,data_len)
    df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
    print("结束时间: " ,datetime.now())
    print("选到了: " ,df)
    return df
def select_gp(res_json,bar_list,symsol,data_len):
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
                get_result_gp(twentyPriceSum,nowCloseRice,nowOpenRice,nowMaxRice,lasteClosePrice,nowVolume,nowFiveVolume,bar_list,symsol)
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
            if 2==i:
                lasteClosePrice =  float(dict['close'])
            if (21 == data_len) & (i == 20):
                get_result_gp(twentyPriceSum,nowCloseRice,nowOpenRice,nowMaxRice,lasteClosePrice,nowVolume,nowFiveVolume,bar_list,symsol)

        i += 1
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

def get_result_gp(twentyPriceSum,nowCloseRice,nowOpenRice,nowMaxRice,lasteClosePrice,nowVolume,nowFiveVolume,bar_list,symsol):
    twentyPrice = round(twentyPriceSum/20,2)
    shiTiPrice = round(nowCloseRice-nowOpenRice,2)
    shangYingPrice = round(nowMaxRice-nowCloseRice,2)
    shangZhangPrice = round(nowCloseRice-lasteClosePrice,2)
    scale = round((shangZhangPrice/lasteClosePrice)*100,2)
    if (nowOpenRice<twentyPrice) & (nowCloseRice>twentyPrice) & (nowVolume>nowFiveVolume) &(shiTiPrice>shangYingPrice)&(scale<3):
        bar = {}
        bar['symsol'] = symsol
        bar['day'] = datetime.now()
        bar_list.append(bar)
#函数调用 60标识一分钟
Time_threading(60)
# get_stock_data_check('EE',30,21)