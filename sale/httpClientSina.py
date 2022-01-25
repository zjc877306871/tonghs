from urllib import request
import json

def http_stock_data(id,scale,data_len):
    id = id
    scale = scale
    data_len = data_len
    url = 'http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}'.format(id, scale, data_len)
    req = request.Request(url)
    # 超时单位是s
    try:
        rsp = request.urlopen(req,timeout=10)
    except BaseException:
        rsp = request.urlopen(req,timeout=10)
    res = rsp.read()
    res_json = json.loads(res)
    res_json.reverse()
    return  res_json