import json
from concurrent.futures import ThreadPoolExecutor
from entity.StockSelf import Stock
import httpClientSina

def get_stock_data_check(id,scale,data_len):
    symsols = id
    print(symsols)
    scale = scale
    data_len = data_len
    bar_list = []
    for symsol in symsols:
        # 异步多线程
        executor = ThreadPoolExecutor(5)
        future =  executor.submit(asnyDealData,symsol,scale,data_len)
        stock = future.result()
        if stock:
            dict = stock.stock2dict()
            bar_list.append(dict)
    # df = pd.DataFrame(data=bar_list)
    df = json.dumps(bar_list)
    return df

def asnyDealData(symsol,scale,data_len):
    res_json = httpClientSina.http_stock_data(symsol,scale,data_len)
    # 具体的筛选逻辑
    stock = select_gp(res_json,symsol)
    return stock
def select_gp(res_json,symsol):
    fivePriceSum = float(0.00)
    lastDayClosePrice = float(0.00)
    newCloseRice = float(0.00)
    newOpenRice = float(0.00)
    newFiveVolume = 0
    newVolume = 0
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
        # bar_list.append(symsol)
        stock = Stock(symsol,newCloseRice)
        return stock

get_stock_data_check('sz002707',30,20)