from redisSelf import redisSelf
from urllib import request
import json
import pandas as pd
from datetime import datetime
from threading import Timer
import time
import tonghs
import timeApi
import stringApi
# 循环获取最近三天的redis的数据
# 解析redis数据中未操作的
#计算30分钟的10和5死叉。获取卖的价格然后计算收益

def Time_threading(inc):
    times = ['10:31','11:01','13:01','13:31','14:01','14:31']
    time_last = '11:15'
    t = Timer(inc,Time_threading,(inc,))
    t.start()
    time_now = timeApi.get_hource()
    for time in times:
        i = 3
        if time_now == time_last:
            print(time_now)
            try:
                df = batch_stock_data('two*',30,20)
            except BaseException:
                df = batch_stock_data('two*',30,20)

            if(len(df) > 2):
                key = 'two:'+ timeApi.formart_date('','%Y%m%d')+':1500'
                conn = redisSelf.getRedisConnection()
                conn.set(key,df)
            break
        else:
            if time_now == time:
                print(time_now)
                try:
                    df = batch_stock_data('EE',30,21)
                except BaseException:
                    df = batch_stock_data('EE',30,21)
                if(len(df) > 2):
                    key = 'two:'+ timeApi.formart_date('','%Y%m%d:')+ stringApi.changeStr(time_now,'0')
                    conn = redisSelf.getRedisConnection()
                    conn.set(key,df)
        i = i+1

def batch_stock_data(key,scale,data_len):
    connect = redisSelf.getRedisConnection()
    keys = get_need_redis_key(key,connect,24)
    for key in keys:
        value = connect.get(key).decode()
        print(value)
        symsols = json.loads(value)
        print('三十分钟二买总量',len(symsols))
        for symsol in symsols:
            # print("开始",symsol)
            res_json = http_stock_data(symsol['symsol'],scale,data_len)
            count_thirty_data(res_json)
    scale = scale
    data_len = data_len
    bar_list = []
    return json.dumps(bar_list)

def count_thirty_data(symsol):
    return symsol

# 获取指定数量的redis缓存数据
def get_need_redis_key(key,connect,num):
    newkeys = [];
#   获取redis的keys进行排序。
    keys = connect.keys(key)
    keys.sort(reverse=True)
    print(keys)
#     获取近三天24条的数据
    i = 0
    for key in keys:
        if  len(keys)<num:
            return keys
        else:
            if i<num:
                newkeys.append(key)
                i = i+1
    newkeys.sort(reverse=True)
    return newkeys

def http_stock_data(id,scale,data_len):
    id = id
    scale = scale
    data_len = data_len
    url = 'http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}'.format(id, scale, data_len)
    req = request.Request(url)
    rsp = request.urlopen(req,timeout=1)
    res = rsp.read()
    res_json = json.loads(res)
    res_json.reverse()
    return  res_json

Time_threading(60)