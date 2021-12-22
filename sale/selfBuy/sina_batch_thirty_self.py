

from matplotlib import font_manager
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import tonghs


def Time_threading(inc):
    times = {'10:03'}
    time_last = '16:53'

    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = get_hource()
    for time in times:
        if time_now == time_last:
            print(time_now)
            df = get_stock_data('EE',30,20)
            break
        else:
            if time_now == time:
                print(time_now)
                df = get_stock_data('EE',30,22)
            # df.to_csv("D:\finance\gp\数据\1111_stock.csv", encoding="gbk", index=False)
            else:
                print('围在时间内： ',datetime.now())
            # df.to_csv("D:\finance\gp\数据\1111_stock.csv", encoding="gbk", index=False)
        # else:
            # print('围在时间内： ',datetime.now())
    #导入到excel

    # print(df)
    # df.head()
def get_stock_data(id,scale,data_len):
    symsols = tonghs.get_self_data()
    print(symsols)
    scale = scale
    data_len = data_len
    bar_list = []

    for symsol in symsols:
        url = 'http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}'.format(symsol, scale, data_len)
        req = request.Request(url)
        rsp = request.urlopen(req)
        res = rsp.read()
        res_json = json.loads(res)
        res_json.reverse()
        # 具体的筛选逻辑
        select_gp(res_json,bar_list,symsol,data_len)
    df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
    print("选到了: " ,df)
    return df

def select_gp(res_json,bar_list,symsol,data_len):
    rwoRiceSum = float(0.00)
    newCloseRice = float(0.00)
    newOpenRice = float(0.00)
    newFiveVolume = 0
    newVolume = 0
    newScale = float(0.00)
    newShangYing = float(0.00)
    newShiTi = float(0.00)
    i = 0
    for dict in res_json:

        if 0 != i:
            close = float(dict['close'])
            rwoRiceSum = rwoRiceSum + close
        if 1 == i:
            newCloseRice = float(dict['close'])
            newOpenRice = float(dict['open'])
            newFiveVolume = int(dict['ma_volume5'])
            newVolume = int(dict['volume'])
            newMaxPrice = float(dict['high'])
            newMinPrice = float(dict['low'])
            newShangYing = newMaxPrice-newCloseRice;
            newShiTi = newCloseRice-newOpenRice
            newScale = (newCloseRice-newOpenRice)/newOpenRice*100


        if (i == 5):
            twoRice = rwoRiceSum/5
            if (newOpenRice < twoRice) & (newCloseRice > twoRice) & (newVolume > newFiveVolume) &(newShiTi > newShangYing) & (newScale < 4 ):
                bar_list.append(symsol)
                print("选到了",bar_list)
        i += 1

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
Time_threading(60)