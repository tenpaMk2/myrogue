#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'


class SuperBase(object):
    def __init__(self):
        print("I'm super maaaaaaaaaaaaaaan.")

class BaseA(SuperBase):
    def __init__(self, name: str):
        super(BaseA, self).__init__()
        print("name is : {0}".format(name))

class BaseB(object):
    def __init__(self, time: int):
        print("time is : {0}".format(time))

class MultiInhe(BaseA, BaseB):
    def __init__(self, name:str, time:int):
        BaseA.__init__(self, name)
        # super(MultiInhe, self).__init__(name)
        print(name*time)


hoge = MultiInhe("unko", 3)