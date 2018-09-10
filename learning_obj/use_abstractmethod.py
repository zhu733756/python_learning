# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
from abc import ABCMeta,abstractmethod
import random

class Fighter(object,metaclass=ABCMeta):

    __slots__ = ('_name','_hp')
    def __init__(self,name,hp):
        self._name=name
        self._hp=hp

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self,health_power):
        if not isinstance(health_power,int):
            raise TypeError("Expected a int type!")
        self._hp=health_power

    @property
    def is_alive(self):
        return self._hp>0

    @abstractmethod
    def attack(self,other):
        pass

class Ultraman(Fighter):

    __slots__ = ('_name', '_hp',"_magic")
    def __init__(self,name,hp,magic):
        super().__init__(name,hp)
        self._magic=magic

    def attack(self,other):
        self._hp-=random.randint(50,75)

    def huge_attack(self,other):
        self._magic-=5
        self._hp -= random.randint(100, 150)

    @property
    def magic_full(self):
        return self._magic==100

    def magic_attack(self,others):
        self._magic-=30
        for other in others:
            if other.is_alive:
                other._hp -= int(0.5 * other._hp) \
                    if int(0.5 * other._hp) > 100 else 100

    def resume(self):
        incr_magic=random.randint(10,15)
        self._magic+=incr_magic
        if self._magic>100:
            self._magic=100
        return incr_magic

    def __str__(self):
        return "====%s奥特曼====\n" \
               "生命值：%s，魔法值：%s"\
               %(self._name,self._hp,self._magic)

class Monter(Fighter):

    __slots__ = ('_name', '_hp')
    def __int__(self,name,hp):
        super().__init__(name,hp)

    def attack(self,other):
        other._hp -= random.randint(20,30)

    def __str__(self):
        return "===%s小怪兽====\n" \
               "生命值：%s"\
               %(self._name,self._hp)

def is_any_monter_alive(ms):
    m1,m2,m3=ms
    return True if m1.is_alive or m2.is_alive or m3.is_alive \
        else False

def select_alive_to_attack(ms):
    alive_list=[m for m in ms if m.is_alive]
    return alive_list

def display(u,ms):
    print(u)
    for m in ms:
        if m.is_alive:
            print(m)
        else:
            print("%s已经挂了" % m.name)

def main():
    u=Ultraman("zhu733756",2000,100)
    m1=Monter("zhangsan",500)
    m2=Monter("lisi",250)
    m3=Monter("wangwu",750)
    ms=(m1,m2,m3)
    fight_round=1
    while is_any_monter_alive(ms) and u.is_alive:
        print("\n====第%2d回合====="%fight_round)
        m_alive=select_alive_to_attack(ms)
        m=random.choice(m_alive)
        number = random.randint(1, 10)
        if u.magic_full:
            if number<2:
                u.attack(m)
                print("%s使用普通攻击打了%s"%(u.name,m.name))
            elif number<4:
                u.huge_attack(m)
                print("%s使用技能[巨力打击]虐了%s" % (u.name, m.name))
            else:
                u.magic_attack(m_alive)
                [print("%s使用魔法虐了%s" % (u.name, m.name))
                 for m in m_alive]
        else:
            if number<6:
                u.attack(m)
                print("%s使用普通攻击打了%s"%(u.name,m.name))
            else:
                u.huge_attack(m)
                print("%s使用技能 [巨力打击] 虐了%s" % (u.name, m.name))
        for m in m_alive:
            m.attack(u)
            print("%s反击了%s"%(m.name,u.name))
        if not u.magic_full:
            print("奥特曼%s恢复了%s魔法"%(u.name,u.resume()))
        print("===第%2d回合结束===="%fight_round)
        display(u,ms)
        fight_round += 1
    else:
        print("游戏结束！")
        if u.is_alive:
            print("奥特曼胜利，剩余hp：",u.hp)
        else:
            print("小怪兽赢了！")

main()

