# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
# 写一个描述类来描述点

class Integer(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected an int type value")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Point(object):
    x = Integer("x")
    y = Integer("y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({},{})".format(self.x, self.y)

# p = Point(3, 4)
# print(p)
# print(p.x)
# print(p.y)
# p.x = 5
# print(p)


class lazyproperty(object):

    def __init__(self,func,name):
        self.func=func
        self.name=name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value =self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

class A(object):

    def __init__(self):
        self.count=0

    @lazyproperty
    def go(self,name=None):
        print("gogogo")
        if name is None:
            return self.count
        return 1

a=A()
print(a.go)
print(a.go)
print(A.go)