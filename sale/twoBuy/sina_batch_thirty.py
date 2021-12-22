

from matplotlib import font_manager
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import tonghs


def Time_threading(inc):
    times = {'10:30','11:00','13:00','13:30','14:04','14:30'}
    time_last = '13:29'

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
                df = get_stock_data('EE',30,21)
            # df.to_csv("D:\finance\gp\数据\1111_stock.csv", encoding="gbk", index=False)
            # else:
                # print('围在时间内： ',datetime.now())
            # df.to_csv("D:\finance\gp\数据\1111_stock.csv", encoding="gbk", index=False)
        # else:
            # print('围在时间内： ',datetime.now())
    #导入到excel

    # print(df)
    # df.head()
def get_stock_data(id,scale,data_len):
    symsols = tonghs.get_ths_data(id)
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
    print("结束时间: " ,datetime.now())
    print("选到了: " ,df)
    return df

def select_gp(res_json,bar_list,symsol,data_len):
    rwoRiceSum = float(0.00)
    newCloseRice = float(0.00)
    newOpenRice = float(0.00)
    newFiveVolume = 0
    newVolume = 0
    i = 0
    for dict in res_json:

        if 20 == data_len:
            if 0 == i:
                newCloseRice = float(dict['close'])
                newOpenRice = float(dict['open'])
                newFiveVolume = int(dict['ma_volume5'])
                newVolume = int(dict['volume'])
                day = dict['day']
            close = float(dict['close'])
            rwoRiceSum = rwoRiceSum + close

            if (20 == data_len) & (i == 19):
                twoRice = rwoRiceSum/20
                if (newOpenRice < twoRice) & (newCloseRice > twoRice) & (newVolume > newFiveVolume):
                    bar = {}
                    bar['symsol'] = symsol
                    bar['day'] = datetime.now()
                    bar_list.append(bar)
        elif  21 == data_len:
            if 0 != i:
                close = float(dict['close'])
                rwoRiceSum = rwoRiceSum + close
            if 1 == i:
                newCloseRice = float(dict['close'])
                newOpenRice = float(dict['open'])
                newFiveVolume = int(dict['ma_volume5'])
                newVolume = int(dict['volume'])
                day = dict['day']
            if (21 == data_len) & (i == 20):
                twoRice = rwoRiceSum/20
                if (newOpenRice < twoRice) & (newCloseRice > twoRice) & (newVolume > newFiveVolume):
                    bar = {}
                    bar['symsol'] = symsol
                    bar['day'] = datetime.now()
                    bar_list.append(bar)
                    # print("选到了",bar_list)
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