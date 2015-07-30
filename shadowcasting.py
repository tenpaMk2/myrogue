#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import logging
import logging.config

logging.config.fileConfig("config/logging.conf")

import twodim

FOV_RADIUS = 10


# 座標は下向き正の右向き生。
# octantは左上の部分を基準に考える。それゆえに、扱う座標が常に負の値を取ってしまいムズムズする。

class MAP(object):
    wall = '#'
    in_fov = '.'
    out_fov = ' '
    player = '@'
    nothing = ' '


class MAPParser(object):
    """
    :type parsed_map: twodim.Made

    """

    def __init__(self, formatted_map: "twodim.Made"):
        self.height = formatted_map.height
        self.width = formatted_map.width

        self.parsed_map = self.make_empty_map(self.height, self.width, padding_type=None)

        for y in range(self.height):
            for x in range(self.width):
                chara = formatted_map.get_value_at(y, x)

                if chara == MAP.wall:
                    self.parsed_map.set_value_at(y, x, MAP.wall)

                elif chara == MAP.nothing:
                    self.parsed_map.set_value_at(y, x, MAP.in_fov)

                else:
                    raise Exception("invalid map object!!!!")

    def is_outside_of_map(self, y: int, x: int):
        return False if (0 < y < self.height and 0 < x < self.width) else False

    def print_parsed_map(self):
        self.parsed_map.logging()

    @staticmethod
    def make_empty_map(height: int, width: int, padding_type=None):
        return twodim.Chara(height, width, padding_type)

    def get_value_at(self, y: int, x: int):
        return self.parsed_map.get_value_at(y, x)


class FOVMap(object):
    # Multipliers for transforming coordinates to other octants:
    transformation_coefficient = [
        [1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]
    ]

    def __init__(self, parsed_map: "MAPParser"):
        self.parsed_map = parsed_map
        self.height = parsed_map.height
        self.width = parsed_map.width

        self.is_in_fov_flags = self.make_is_in_fov_flags()

    def clear_is_in_fov_flags(self):
        self.is_in_fov_flags = self.make_is_in_fov_flags()

    def make_is_in_fov_flags(self):
        return [[False for _ in range(self.width)] for _ in range(self.height)]

    def get_map_cell(self, y: int, x: int):
        return self.parsed_map.get_value_at(y, x)

    def is_blocked(self, y: int, x: int):
        return (x < 0 or y < 0
                or x >= self.width or y >= self.height
                or self.parsed_map.get_value_at(y, x) == MAP.wall)

    def is_in_fov(self, y: int, x: int):
        return self.is_in_fov_flags[y][x]

    def set_in_fov(self, y: int, x: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.is_in_fov_flags[y][x] = True

    def _cast_light(self, cy, cx, start_row, start_slope, end_slope, radius, xx, xy, yx, yy, oct_id):
        """Recursive lightcasting function"""

        logging.info("start_slope : %r", start_slope)
        logging.info("end_slope : %r", end_slope)

        if start_slope < end_slope:
            logging.info("start_slope < end_slope")
            return

        # 後で比較するだけなので、radius_squaredは平方根を取らなくていい。
        radius_squared = radius * radius

        for row in range(start_row, radius + 1):
            # dxとdyはslopeの計算用。dx = x1 - x2 を示す。
            # dxが-2から始まるのは、whileで最初に+1するため。
            dy = -row
            dx = -row - 1

            is_previous_cell_blocked_flag = False

            # x座標を移動する代わりに、dxを増やす。
            while dx <= 0:
                dx += 1

                # Translate the dx, dy coordinates into map coordinates:
                trans_x = cx + dx * xx + dy * xy
                trans_y = cy + dx * yx + dy * yy

                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)

                # 俺が追加したslope。一個前の操作のときのr_slope。
                previous_r_slope = (dx - 0.5) / (dy - 0.5)

                if r_slope > start_slope:
                    continue

                elif end_slope > l_slope:
                    break

                else:
                    # Our light beam is touching this square; light it:
                    # つまり、start_slopeからend_slopeの間の勾配であり、radius以内であれば視界に入ったと見なす。
                    if (dx ** 2) + (dy ** 2) < radius_squared:
                        self.set_in_fov(trans_y, trans_x)

                    if is_previous_cell_blocked_flag:
                        # 一個前の捜査のとき、ブロックであった場合
                        # we're scanning a row of blocked squares:
                        if self.is_blocked(trans_y, trans_x):
                            # ブロックが続いている場合
                            continue
                        else:
                            # ブロックが途切れた場合、start_slopeを設定。
                            is_previous_cell_blocked_flag = False
                            start_slope = previous_r_slope
                    else:
                        # 一個前の捜査のとき、ブロックではなかった場合
                        if self.is_blocked(trans_y, trans_x) and row < radius:
                            # ブロックだった場合、新たなスキャンを開始（新たなスキャンを先に計算する。）
                            # This is a blocking square, start a child scan:
                            is_previous_cell_blocked_flag = True
                            self._cast_light(cy, cx, row + 1, start_slope, l_slope, radius, xx, xy, yx, yy, oct_id + 1)

            # Row is scanned; do next row unless last square was blocked:
            if is_previous_cell_blocked_flag:
                # 行のスキャンの最後がブロックで終わった場合、スキャン全体を終了する。
                logging.info("block end")
                break

    def do_fov(self, cy, cx, radius):
        """FOVの計算"""

        # 視界のクリア。忘れると視界がオンになりっぱなしな部分ができる。
        self.clear_is_in_fov_flags()

        # 8つの3角形に分けて計算。wiki参照。
        for octant in range(len(self.transformation_coefficient[0])):
            logging.info("----------start octant : %r----------", octant)
            self._cast_light(cy, cx, 1, 1.0, 0.0, radius, self.transformation_coefficient[0][octant],
                             self.transformation_coefficient[1][octant], self.transformation_coefficient[2][octant],
                             self.transformation_coefficient[3][octant], 0)

    def display(self, current_x, current_y):
        """マップの表示"""

        map_list = [
            [
                MAP.player if (x == current_x and y == current_y) else
                MAP.wall if self.is_in_fov(y, x) and self.get_map_cell(y, x) == MAP.wall else
                MAP.in_fov if self.is_in_fov(y, x) else
                MAP.out_fov
                for x in range(self.width)] for y in range(self.height)]

        map_buffer = twodim.Made(map_list)
        map_buffer.logging()


if __name__ == '__main__':
    map_data = [
        "###########################################################",
        "#           #                                             #",
        "#           #        #                                    #",
        "#                     #                                   #",
        "#    ####              #                                  #",
        "#       #                       #####################     #",
        "#       #                                           #     #",
        "#       #           ##                              #     #",
        "#####        #      ##          ##################  #     #",
        "#   #                           #                #  #     #",
        "#   #            #              #                #  #     #",
        "#                               #  ###############  #     #",
        "#                               #                   #     #",
        "#                               #                   #     #",
        "#                               #####################     #",
        "#                                                         #",
        "#                                                         #",
        "###########################################################"
    ]
    nested_map_data = [[ch for ch in row] for row in map_data]
    formatted_map_data = twodim.Made(nested_map_data)

    d_parsed_map = MAPParser(formatted_map_data)

    d_current_x, d_current_y = 36, 13
    d_fov_map = FOVMap(d_parsed_map)

    while True:
        d_fov_map.do_fov(d_current_y, d_current_x, FOV_RADIUS)
        d_fov_map.display(d_current_x, d_current_y)

        key = input()

        if key == 'n':
            d_current_y -= 1
        elif key == 's':
            d_current_y += 1
        elif key == 'e':
            d_current_x += 1
        elif key == 'w':
            d_current_x -= 1
        else:
            raise Exception("Invalid input.")

        logging.debug("key : %r", key)
