import redis

# pool = redis.ConnectionPool(host='127.0.0.1')
# r = redis.Redis(connection_pool=pool)#实现一个连接池
# r.set('foo','bar')
# print(r.get('foo').decode('utf8'))


def getRedisConnection():
    pool = redis.ConnectionPool(host='127.0.0.1')
    r = redis.Redis(connection_pool=pool)#实现一个连接池
    return r

