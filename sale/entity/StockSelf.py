class Stock:
    # # #定义基本属性
    name = ''
    # # #定义私有属性,私有属性在类外部无法直接进行访问
    __price = float(0.00)
    time = ''

    #定义构造方法
    def __init__(self,n,p,t):
        self.name = n
        self.__price = p
        self.time = t


    # def speak(self):
    #     print(self.__price)

    def stock2dict(self):
        return {
            'name': self.name,
            'price': self.__price,
            'time': self.time
        }
# s = Stock('w',float(33))
# s.speak()