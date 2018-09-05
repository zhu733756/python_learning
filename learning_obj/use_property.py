# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
# @property装饰器:属性方法的作用就是通过@property把一个方法变成一个静态属性
# 功能：设置私有属性，限定访问，
# 将属性命名以单下划线开头，通过这种方式来暗示属性是受保护的
# 访问属性可以通过属性的getter（访问器）和setter（修改器）方法进行对应的操作。

# class Person(object):
#
#     def __init__(self,name,age):
#         self._name=name
#         self._age=age
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def age(self):
#         return self._age
#
#     @age.setter
#     def age(self,age):
#         if not isinstance(age,int):
#             raise TypeError("Needed an int type,not a {} type".format(type(age)))
#         if age not in range(0,199):
#             raise ValueError("Got a wrong age value:{}".format(age))
#         self._age=age
#
# person=Person("zhu733756",18)
# print(person.name)
# print(person.age)
# person.age=1
# print(person.age)
# # person.age=-1
# # print(person.age)
# person.age="18"
# print(person.age)

#子类中扩展property

# class Person(object):
#
#     def __init__(self,name):
#         self._name=name
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self,value):
#         if not isinstance(value,str):
#             raise TypeError("Expected a str type!")
#         self._name=value
#
#     @name.deleter
#     def name(self):
#         raise AttributeError("Can't delete attribute")
#
# p=Person("zhu733756")
# print(p.name)
# p.name="zhu756733"
# print(p.name)
# print("-----")
#
# class subPerson(Person):
#
#     @property
#     def name(self):
#         print("getting name")
#         return super().name
#
#     @name.setter
#     def name(self,value):
#         print('setting name')
#         super(subPerson, subPerson).name.__set__(self,value)
#
#     @name.deleter
#     def name(self):
#         print('deleting name')
#         super(subPerson, subPerson).name.__delete__(self)
#
# p2=subPerson("zhu733756")
# print(p2)
# print(p2.name)
# p2.name="zhu756733"
# print(p2.name)
# # p2.name=18
# # print(p2.name)


class String(object):

    def __init__(self,name):
        self.name=name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value,str):
            raise TypeError("Excepted a str type!")
        instance.__dict__[self.name]=value

class Person(object):
    name=String("name")

    def __init__(self, name):
        self.name = name


class SubPerson(Person):

    @property
    def name(self):
        print("getting name")
        return super().name

    @name.setter
    def name(self, value):
        print('setting name')
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

    def __str__(self):
        return "<SubPerson('%s')>"%self.name

p3=SubPerson("zhu733756")
print(p3)
print(p3.name)
p3.name="zhu756733"
print(p3.name)
p3.name=18
print(p3.name)


