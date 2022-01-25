from concurrent.futures import ThreadPoolExecutor
from entity.StockSelf import Stock
def test():
    executor = ThreadPoolExecutor(10)
    future =  executor.submit(check,'1',float(2.00))
    ansy_list = future.result()
    print(ansy_list)

def check(i,j):
    stock = Stock(i, j)
    return stock


# test()
check('2',float(4.6))