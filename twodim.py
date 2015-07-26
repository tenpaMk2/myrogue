#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")


# TODO listを継承させてもいいか。
class Made(object):
    def __init__(self, nested_list: list):
        self.data = nested_list

        self.height = len(self.data)
        self.width = len(self.data[0])

    def get_value_at(self, y: int, x: int):
        return self.data[y][x]

    def set_value_at(self, y: int, x: int, value):
        self.data[y][x] = value

    def print(self):
        formatted_str = self._make_formatted_str()
        print(formatted_str)

    def logging(self):
        formatted_str = self._make_formatted_str()
        logging.debug('\n' + formatted_str)

    def _make_formatted_str(self):
        chara_list = [[str(value) for value in row] for row in self.data]
        return self._return_formatted_str(chara_list)

    @staticmethod
    def _return_formatted_str(chara_list: list):
        return "\n".join(["".join(row) for row in chara_list])

    def return_copy_of_nested_list(self):
        return [[value for value in row] for row in self.data]


class Plane(Made):
    def __init__(self, height: int, width: int, padding_value=None):
        nested_list = [[padding_value for _ in range(width)] for _ in range(height)]
        super(Plane, self).__init__(nested_list)


class Chara(Plane):
    """文字に変換する手間を省いたクラス。print関連が高速なはず。__main__で測定してるけど、2倍くらい高速。"""

    def __init__(self, height: int, width: int, padding_chara: str=' '):
        super(Chara, self).__init__(height, width, padding_chara)

    def _make_formatted_str(self):
        return self._return_formatted_str(self.data)


if __name__ == '__main__':
    import time

    hoge = [[y + x for x in range(5)] for y in range(5)]

    made_hoge = Made(hoge)
    made_hoge.print()

    start_t = time.clock()
    plane = Plane(10, 20, '@')
    plane.print()
    plane.logging()
    end_t = time.clock()
    print("processing time is {0}".format(end_t - start_t))

    start_t = time.clock()
    chara = Chara(10, 20, '#')
    chara.print()
    chara.logging()
    end_t = time.clock()
    print("processing time is {0}".format(end_t - start_t))

    print(chara.height)
    print(chara.width)

    print("deep copyのテスト")
    hage = chara.return_copy_of_nested_list()
    hage[0][0] = '*'
    print(hage)

    chara.print()
