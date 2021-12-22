

from matplotlib import font_manager
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer


def Time_threading(inc):
    print(datetime.now())
    t = Timer(inc,Time_threading,(inc,))
    t.start()
    df = get_stock_data('sz002354',30,6)
    #导入到excel
    # df.to_csv("~/Downloads/000829_stock.csv", encoding="gbk", index=False)
    print(df)
    df.head()


def get_stock_data(id,scale,data_len):
    symsol = '股票代码'
    scale = scale
    data_len = data_len
    url = 'http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}'.format(id, scale, data_len)
    req = request.Request(url)
    rsp = request.urlopen(req)
    res = rsp.read()
    res_json = json.loads(res)
    bar_list = []
    res_json.reverse()
    # print(res_json)
    select_gp(res_json,bar_list,symsol,data_len)

    df = pd.DataFrame(data=bar_list)
    # show_k_line(bar_list,bar_list2,high_list,high_list2)
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
        print(dict)
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
        print(i)
#函数调用 60标识一分钟
# Time_threading(60)
get_stock_data('sh605337',30,6)