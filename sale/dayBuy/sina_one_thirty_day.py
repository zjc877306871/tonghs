#
#
# from matplotlib import font_manager
# from urllib import request
# import json
# import pandas as pd
# from datetime import datetime
# from threading import Timer
# import time
#
# def Time_threading(inc):
#     print(datetime.now())
#     t = Timer(inc,Time_threading,(inc,))
#     t.start()
#     # 获取历史数据
#     sum_list = get_stock_data_60('sz002354',60,76)
#     df = get_stock_data_30('sz002354',30,8,sum_list)
#     #导入到excel
#     # df.to_csv("~/Downloads/000829_stock.csv", encoding="gbk", index=False)
#     print(df)
#     df.head()
#
#
# def get_stock_data(id,scale,data_len):
#     sum_list = get_stock_data_60(id,scale,data_len)
#     get_stock_data_30(id,30,8,sum_list)
#
# def http_stock_data(id,scale,data_len):
#     id = id
#     scale = scale
#     data_len = data_len
#     url = 'http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}'.format(id, scale, data_len)
#     req = request.Request(url)
#     rsp = request.urlopen(req)
#     res = rsp.read()
#     res_json = json.loads(res)
#     res_json.reverse()
#     return  res_json
# def get_stock_data_30(id,scale,data_len,sum_list):
#     bar_list = []
#     res_json = http_stock_data(id,scale,data_len)
#     print(res_json)
#     select_now_gp(res_json,bar_list,id,data_len,sum_list)
#     print('历史的数据：',sum_list)
#
#     df = pd.DataFrame(data=bar_list)
#     # show_k_line(bar_list,bar_list2,high_list,high_list2)
#     return df
#
# def get_stock_data_60(id,scale,data_len):
#     bar_list = []
#     res_json = http_stock_data(id,scale,data_len)
#     # print(res_json)
#     sum_list = select_his_gp(res_json,bar_list,id,data_len)
#     return sum_list
#
# def select_his_gp(res_json,bar_list,symsol,data_len):
#     newCloseRice = float(0.00)
#     lastFourVolume = 0
#     lastFourPrice = float(0.00)
#     i = 0
#     sum_list = []
#     for dict in res_json:
#         day = dict['day'][:10]
#         hour = dict['day'][11:]
#         nowDay = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10]
#         # 获取当天的数据，成交量/开盘价/收盘价/最高价
#         #获取历史的收盘价，收盘价/成交量
#         if (hour == '15:00:00') & (i != 0):
#             newCloseRice = newCloseRice + float(dict['close'])
#
#         if 0==data_len%4:
#             # 处理当日最后一次跑数
#             if (i < (data_len%4)+20) & (i >= (data_len%4)) & (hour == '15:00:00') & (i != 0):
#                 #     获取最近4天的收盘价
#                 lastFourPrice = lastFourPrice + float(dict['close'])
#         else:
#             if (i < (data_len%4)+16) & (i >= (data_len%4)) & (hour == '15:00:00') & (i != 0):
#                 #     获取最近4天的收盘价
#                 lastFourPrice = lastFourPrice + float(dict['close'])
#
#         if (i < (data_len -(data_len%4))+16) & (i >= (data_len%4)):
#             #     获取最近4天的历史成交量
#             lastFourVolume = lastFourVolume + int(dict['volume'])
#         i += 1
#     # print(i)
#     bar = {}
#     bar['newCloseRice'] = newCloseRice
#     bar['lastFourVolume'] = lastFourVolume
#     bar['lastFourPrice'] = lastFourPrice
#
#     sum_list.append(bar)
#     return sum_list
#
#
# def select_now_gp(res_json,bar_list,symsol,data_len,sum_list):
#     nowCloseRice = float(0.00)
#     nowOpenRice = float(0.00)
#     lastVolume = 0
#     i = 0
#     for dict in res_json:
#         # day = dict['day'][:10]
#         # hour = dict['day'][11:]
#         # nowDay = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10]
#         # 获取当天的数据，成交量/开盘价/收盘价/最高价
#         #获取历史的收盘价，收盘价/成交量
#         if i == 0:
#             # 获取最新收盘
#             nowCloseRice = float(dict['close'])
#         elif i == data_len-1:
#             #获取当日开盘
#             nowOpenRice = float(dict['open'])
#         lastVolume = lastVolume + int(dict['volume'])
#         i += 1
#         print(i)
#         print(int(dict['volume']))
#
#     # 进行决策判断
#     bar = sum_list[0]
#     newCloseRice = bar['newCloseRice']
#     lastFourVolume = bar['lastFourVolume']
#     lastFourPrice = bar['lastFourPrice']
#     newCloseRice = newCloseRice + nowCloseRice
#     fivePriceSum = lastFourPrice + nowCloseRice
#     lastFourVolume = lastFourVolume+lastVolume
#     # 20日均价
#     twentyPrice = newCloseRice/20
#     # 5日均量
#     fiveVolume = lastFourVolume/5
#     #5日均价
#     fivePrice = fivePriceSum/5
#     if (nowOpenRice<fivePrice) & (nowCloseRice>fivePrice) & (fiveVolume>lastVolume) & (fivePrice>twentyPrice):
#         bar_list.append(symsol)
#         print("选到了",bar_list)
# #函数调用 60标识一分钟
# # Time_threading(60)
# get_stock_data('sz000607',60,80)