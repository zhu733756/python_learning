# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
#classmethod类方法:类方法只能访问类变量，不能访问实例变量
# 类方法的第一个参数约定名为cls，
# 它代表的是当前类相关的信息的对象（类本身也是一个对象，有的地方也称之为类的元数据对象），
# 通过这个参数我们可以获取和类相关的信息并且可以创建出类的对象。

#static:静态方法是不能访问实例变量和类变量的　
# 静态方法:这个方法并不是类的对象方法，一个不能访问实例变量和类变量的方法，
# 其实相当于跟类本身已经没什么关系了，它与类唯一的关联就是需要通过类名来调用这个方法。
# 例如我们定义一个“三角形”类，
# 通过传入三条边长来构造三角形，并提供计算周长和面积的方法，
# 但是传入的三条边长未必能构造出三角形对象，
# 因此我们可以先写一个方法来验证三条边长是否可以构成三角形，
# 这个方法很显然就不是对象方法，因为在调用这个方法时三角形对象尚未创建出来（因为都不知道三条边能不能构成三角形），
# 所以这个方法是属于三角形类而并不属于三角形对象的。

# 静态方法是不可以访问实例变量或类变量的
# 类方法和普通方法的区别是， 类方法只能访问类变量，不能访问实例变量
# 属性方法将一个方法变为类的属性，调用时不需要加()。有@property 、@属性方法名.setter、@属性方法名.deleter 三种装饰方法

from math import sqrt

class Triangle(object):

    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c

    @staticmethod
    def is_valid(a, b, c):
        return a + b > c and b + c > a and a + c > b

    def perimeter(self):
        return self._a + self._b + self._c

    def area(self):
        half = self.perimeter() / 2
        return sqrt(half * (half - self._a) *
                    (half - self._b) * (half - self._c))

a, b, c = 3, 4, 5
if Triangle.is_valid(a, b, c):
    t = Triangle(a, b, c)
    print(t.perimeter())
    print(t.area())
else:
    print('无法构成三角形.')


from time import time, localtime, sleep

class Clock(object):

    def __init__(self,hour,minute,second):
        self._hour=hour
        self._minute=minute
        self._second=second

    @classmethod
    def get_localtime(cls):
        local=localtime(time())
        return cls(hour=local.tm_hour,
                   minute=local.tm_min,
                   second=local.tm_sec)

    def run(self):
        self._second+=1
        if self._second==60:
            self._minute+=1
            self._second=0
            if self._minute==60:
                self._hour+=1
                self._minute=0
                if self._hour==24:
                    self._hour=0

    def show(self):
        print("%02d:%02d:%02d"%(self._hour,self._minute,self._second))

clock=Clock.get_localtime()
while 1:
    clock.show()
    sleep(1)
    clock.run()