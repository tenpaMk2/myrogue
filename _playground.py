#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

from abc import ABCMeta, abstractmethod


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
        print(name * time)


hoge = MultiInhe("unko", 3)

print("------------------------------------")


class TesutoBase(metaclass=ABCMeta):
    @abstractmethod
    def do_hoge(self):
        print('abstract')


class ConcreteHoge(TesutoBase):
    def do_wawa(self):
        print('wawa')


class ConcreteHogePerfect(ConcreteHoge):
    def do_hoge(self):
        super().do_hoge()
        print('concrete')

# aaa = TesutoBase() # TypeError
# aaa.do_hoge()

# bbb = ConcreteHoge()
# bbb.do_wawa()
# bbb.do_hoge()

ccc = ConcreteHogePerfect()
ccc.do_wawa()
ccc.do_hoge()

print("--------------------------------------")


class Tpeople(object):
    def run(self):
        print("run")
        self._end_turn()

    @abstractmethod
    def _end_turn(self):
        print("end_turn")


class Thero(Tpeople):
    def _end_turn(self):
        print("Hero_end_turn")


class Tvillager(Tpeople):
    pass


th = Thero()
th.run()
tv = Tvillager()
tv.run()

print("-----------------")


class SuperClass(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def print_name_multiple_times(self):
        print(self.name * self.value)


class TTpeople(SuperClass, metaclass=ABCMeta):
    def __init__(self, name: str="I'm TTpeople"):
        super(TTpeople, self).__init__(name, 3)
        self.name = name

    def run(self):
        print("{0} run".format(self.name))
        self._end_turn()

    @abstractmethod
    def _end_turn(self):
        print("end_turn")


class TThero(TTpeople):
    def _end_turn(self):
        print("Hero_end_turn")


class TTvillager(TTpeople):
    def _end_turn(self):
        print("Villager_end_turn")


class NoImplementer(TTpeople):
    pass


tth = TThero("HEROOOOO")
tth.run()
ttv = TTvillager("私が村長です。")
ttv.run()
# nip = NoImplementer()  # TypeError: Can't instantiate abstract class TTvillager with abstract methods _end__turn
tth.print_name_multiple_times()


print("--------------------------------")

class MetaclassTesuto(metaclass=ABCMeta):
    def __init__(self):
        print("metaclass=ABCMeta だけでは、インスタンスが生成できてしまう。")

    def metaclass_ga_arudake(self):
        print("まあでも別にいいかなぁー?")

metaclasstesuto = MetaclassTesuto()
metaclasstesuto.metaclass_ga_arudake()
