#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

# FOV calculation for roguelike

import curses

FOV_RADIUS = 10

dungeon = ["###########################################################",
           "#...........#.............................................#",
           "#...........#........#....................................#",
           "#.....................#...................................#",
           "#....####..............#..................................#",
           "#.......#.......................#####################.....#",
           "#.......#...........................................#.....#",
           "#.......#...........##..............................#.....#",
           "#####........#......##..........##################..#.....#",
           "#...#...........................#................#..#.....#",
           "#...#............#..............#................#..#.....#",
           "#...............................#..###############..#.....#",
           "#...............................#...................#.....#",
           "#...............................#...................#.....#",
           "#...............................#####################.....#",
           "#.........................................................#",
           "#.........................................................#",
           "###########################################################"]


# 座標は下向き正の右向き生。
# octantは左上の部分を基準に考える。それゆえに、扱う座標が常に負の値を取ってしまいムズムズする。

class FOVMap(object):
    # Multipliers for transforming coordinates to other octants:
    mult = [
        [1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]
    ]

    def __init__(self, parsed_map):
        self.parsed_map = parsed_map
        self.width, self.height = len(parsed_map[0]), len(parsed_map)
        self.light = []
        for i in range(self.height):
            self.light.append([0] * self.width)
        self.flag = 0

    def get_map_cell(self, x, y):
        return self.parsed_map[y][x]

    def is_blocked(self, x, y):
        return (x < 0 or y < 0
                or x >= self.width or y >= self.height
                or self.parsed_map[y][x] == "#")

    def is_litted(self, x, y):
        return self.light[y][x] == self.flag

    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = self.flag

    def _cast_light(self, cx, cy, row, start_slope, end_slope, radius, xx, xy, yx, yy, oct_id):
        """Recursive lightcasting function"""
        if start_slope < end_slope:
            return

        radius_squared = radius * radius
        for j in range(row, radius + 1):
            # dxとdyはslopeの計算用。dx = x1 - x2 を示す。
            dx, dy = -j - 1, -j
            is_previous_cell_blocked_flag = False
            new_start_slope = start_slope
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if r_slope > start_slope:
                    continue
                elif end_slope > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.set_lit(X, Y)

                    if is_previous_cell_blocked_flag:
                        # we're scanning a row of blocked squares:
                        if self.is_blocked(X, Y):
                            new_start_slope = r_slope
                            continue
                        else:
                            is_previous_cell_blocked_flag = False
                            start_slope = new_start_slope
                    else:
                        if self.is_blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            is_previous_cell_blocked_flag = True
                            self._cast_light(cx, cy, j + 1, start_slope, l_slope,
                                             radius, xx, xy, yx, yy, oct_id + 1)
                            new_start_slope = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if is_previous_cell_blocked_flag:
                break

    def do_fov(self, cx, cy, radius):
        """Calculate lit squares from the given location and radius"""
        self.flag += 1
        for octant in range(8):
            self._cast_light(cx, cy, 1, 1.0, 0.0, radius,
                             self.mult[0][octant], self.mult[1][octant],
                             self.mult[2][octant], self.mult[3][octant], 0)

    def display(self, curses_scr, current_x, current_y):
        """Display the map on the given curses screen (utterly unoptimized)"""
        dark_color, lit_color = curses.color_pair(8), curses.color_pair(7) | curses.A_BOLD
        for x in range(self.width):
            for y in range(self.height):
                if self.is_litted(x, y):
                    attr = lit_color
                else:
                    attr = dark_color

                if x == current_x and y == current_y:
                    ch = '@'
                    attr = lit_color
                else:
                    ch = self.get_map_cell(x, y)
                curses_scr.addstr(y, x, ch, attr)
        curses_scr.refresh()


def color_pairs():
    c = []
    for i in range(1, 16):
        curses.init_pair(i, i % 8, 0)
        if i < 8:
            c.append(curses.color_pair(i))
        else:
            c.append(curses.color_pair(i) | curses.A_BOLD)
    return c


if __name__ == '__main__':
    try:
        s = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        color_pairs()
        s.keypad(1)

        d_current_x, d_current_y = 36, 13
        d_fov_map = FOVMap(dungeon)
        while True:
            d_fov_map.do_fov(d_current_x, d_current_y, FOV_RADIUS)
            d_fov_map.display(s, d_current_x, d_current_y)

            key = s.getch()
            if key == 27:
                break
            elif key == 259:
                d_current_y -= 1
            elif key == 258:
                d_current_y += 1
            elif key == 260:
                d_current_x -= 1
            elif key == 261:
                d_current_x += 1
    finally:
        s.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        print("Normal termination.")
