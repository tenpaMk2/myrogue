#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

import enum


@enum.unique
class DIRECTION(enum.Enum):
    north = 0
    northeast = 1
    east = 2
    southeast = 3
    south = 4
    southwest = 5
    west = 6
    northwest = 7


def print_nested_list(nested_list: list):
    formatted_str = "\n".join(["".join(row) for row in nested_list])
    print(formatted_str)


class Node(object):
    """
    f(n) ... startからgoalまでの最短距離
    g(n) ... startからnノードまでの最短距離
    h(n) ... nノードからgoalまでの最短距離
    f(n) = g(n) + h(n)

    関数を推定値にすることにより最短距離を予測する
    h*(n)をnからgoalまでの直線距離と仮定する。

    f*(n) = g*(n) + h*(n)
    :type gs: float

    :type start_pos: (int, int)
    :type goal_pos: (int, int)

    :type owner_list: NodeList
    :type parent_node: Node
    """
    start_pos = None  # start位置(x,y)
    goal_pos = None  # goal位置(x,y)

    def __init__(self, y: int, x: int, gs: float=0):
        self.pos = (y, x)
        self.gs = gs
        self.hs = ((x - self.goal_pos[0]) ** 2 + (y - self.goal_pos[1]) ** 2) ** 0.5
        # self.hs = (x - self.goal[0]) ** 2 + (y - self.goal[1]) ** 2
        # self.hs = abs(x - self.goal[0]) + abs(y - self.goal[1])
        self.owner_list = None
        self.parent_node = None

    # Node.fsはプロパティで表現することに。
    @property
    def fs(self):
        return self.gs + self.hs

    @fs.setter
    def fs(self, value):
        raise Exception("fs is not settable")

    def is_goal(self) -> bool:
        return self.goal_pos == self.pos


class NodeList(list):
    def find(self, y: int, x: int) -> Node:
        nodes = [t for t in self if t.pos == (y, x)]
        # listが空ならFalseであることを利用したpythonicな書き方。
        return nodes[0] if nodes else None

        # removeはlistが持ってるメソッドで十分。よってコメントアウト
        # def remove(self, node):
        #     del self[self.index(node)]

    def get_minimum_fs_node(self):
        return min(self, key=lambda node: node.fs)


class SearchingMap(object):
    """
    :type parsed_map: list
    :type obstacles_map: list

    :type start_pos: (int, int)
    :type goal_pos: (int, int)
    """

    def __init__(self, matrix_map: list):
        self.height = len(matrix_map)
        self.width = max([len(row) for row in matrix_map])

        self.parsed_map = self._make_empty_map(self.height, self.width)
        self.obstacles_map = self._make_empty_map(self.height, self.width)

        self.start_pos = None
        self.goal_pos = None

        for y, row in enumerate(matrix_map):
            for x, chara in enumerate(row):
                if chara == '#':
                    self.parsed_map[y][x] = '#'
                    self.obstacles_map[y][x] = True
                elif chara == 'S':
                    if not self.start_pos:
                        self.parsed_map[y][x] = 'S'
                        self.start_pos = (y, x)
                    else:
                        raise Exception("There are multiple Starts!!")
                elif chara == 'G':
                    if not self.goal_pos:
                        self.parsed_map[y][x] = 'G'
                        self.goal_pos = (y, x)
                    else:
                        raise Exception("There are multiply Goals!!")
                elif chara == ' ':
                    self.parsed_map[y][x] = ' '
                    self.obstacles_map[y][x] = False
                else:
                    raise Exception("invalid map object!!!!")

        # TODO これいるかなあ? 別の場所でやった方が良い気がする。
        Node.start_pos = self.start_pos
        Node.goal_pos = self.goal_pos

    def is_obstacle_at(self, y: int, x: int):
        return self.obstacles_map[y][x]

    def is_outside_of_map(self, y: int, x: int):
        return False if (0 < y < self.height and 0 < x < self.width) else False

    def print_parsed_map(self):
        print_nested_list(self.parsed_map)

    def print_obstacles_map(self):
        parsed_obstacles_map = self._make_empty_map(self.height, self.width)
        for y, row in enumerate(self.obstacles_map):
            for x, element in enumerate(row):
                if element:
                    parsed_obstacles_map[y][x] = '1'
                else:
                    parsed_obstacles_map[y][x] = '0'

        print_nested_list(parsed_obstacles_map)

    @staticmethod
    def _make_empty_map(height: int, width: int, padding_type=None):
        return [[padding_type for _ in range(width)] for _ in range(height)]

    @staticmethod
    def return_deep_copy_of_nested_list(nested_list):
        return [[chara for chara in row] for row in nested_list]


class Astar(object):
    def __init__(self, searching_map: "SearchingMap"):
        self.searching_map = searching_map
        self.open_list = NodeList()
        self.close_list = NodeList()

        self.start_node = Node(*Node.start_pos, gs=0)
        self.end_node = None

        # スタート地点のノードをオープンリストに加える
        self.open_list.append(self.start_node)

        # オープンリストが空になるまで続ける
        while self.open_list:
            print("----------------------------------------")
            self.print_open_close_list()

            # Openリストからf*が最少のノードnを取得
            current_node = self.open_list.get_minimum_fs_node()
            print("current_node : {0} : fs : {1}".format(current_node.pos, current_node.fs))

            # 最小ノードがゴールだったら終了
            if current_node.is_goal():
                print("goal!")
                self.end_node = current_node
                break

            # ノードnの移動可能方向のノードを調べる
            for v in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                y = current_node.pos[0] + v[0]
                x = current_node.pos[1] + v[1]
                dist_from_n = ((current_node.pos[0] - y) ** 2 + (current_node.pos[1] - x) ** 2) ** 0.5
                print("(y, x) : {0} : dist_from_n : {1}".format((y, x), dist_from_n))

                # マップが範囲外または壁(#)の場合はcontinue
                if self.searching_map.is_outside_of_map(y, x) \
                        or self.searching_map.is_obstacle_at(y, x):
                    print("outside map or at obstacle.")
                    continue

                # 移動先のノードがOpen,Closeのどちらのリストに
                # 格納されているか、または新規ノードなのかを調べる
                selecting_open_node = self.open_list.find(y, x)

                if selecting_open_node:
                    # 移動先のノードがOpenリストに格納されていた場合、
                    # より小さいf*ならばノードmのf*を更新し、親を書き換え
                    new_gs = current_node.gs + dist_from_n
                    new_fs = selecting_open_node.hs + new_gs
                    if selecting_open_node.fs > new_fs:
                        selecting_open_node.gs = new_gs
                        selecting_open_node.parent_node = current_node

                        print("selecting_open_node is in OpenList")
                else:
                    # 移動先のノードがOpenリストに無かった場合。

                    selecting_close_node = self.close_list.find(y, x)
                    if selecting_close_node:
                        # 移動先のノードがCloseリストに格納されていた場合、
                        # より小さいf*ならばノードmのf*を更新し、親を書き換え
                        # かつ、Openリストに移動する

                        new_gs = current_node.gs + dist_from_n
                        new_fs = selecting_close_node.hs + new_gs
                        if selecting_close_node.fs > new_fs:
                            selecting_close_node.gs = new_gs
                            selecting_close_node.parent_node = current_node

                            self.close_list.remove(selecting_close_node)
                            self.open_list.append(selecting_close_node)

                            print("selecting_close_node is in CloseList")
                        else:
                            print("selecting_close_node better than new.")
                    else:
                        # 新規ノードならばOpenリストにノードに追加
                        selecting_close_node = Node(y, x, current_node.gs + dist_from_n)
                        selecting_close_node.parent_node = current_node
                        self.open_list.append(selecting_close_node)

                        print("selecting_close_node is New node")

            # 周りのノードを全てOpenし終えたので、クローズする。
            self.open_list.remove(current_node)
            self.close_list.append(current_node)

        else:
            # Openリストが空になったら解なし
            if not self.end_node:
                raise Exception("There is no route until reaching a goal.")

    def print_map(self, end_node: "Node"):
        # endノードから親を辿っていくと、最短ルートを示す
        n = end_node.parent_node
        map_buffer = self.searching_map.return_deep_copy_of_nested_list(self.searching_map.parsed_map)

        while True:
            if n.parent_node is None:
                break
            map_buffer[n.pos[0]][n.pos[1]] = '+'
            n = n.parent_node

        print("n's fs : {0}".format(n.fs))
        print_nested_list(map_buffer)

    def print_open_close_list(self):
        map_buffer = self.searching_map.return_deep_copy_of_nested_list(self.searching_map.parsed_map)

        for open_node in self.open_list:
            y = open_node.pos[0]
            x = open_node.pos[1]
            map_buffer[y][x] = 'o'

        for close_node in self.close_list:
            y = close_node.pos[0]
            x = close_node.pos[1]
            map_buffer[y][x] = 'c'

        print_nested_list(map_buffer)

    def has_route_to_goal(self):
        return True if not self.end_node else False


if __name__ == '__main__':
    map_data = [
        '######################################',
        '#G  #     #     #         #          #',
        '#   #  #  #  #  #         #    #### S#',
        '#      #     #  #   ####  #    #  ####',
        '## ###############  #     #    #     #',
        '#                #  #     #          #',
        '#        ###     #  #     #########  #',
        '#  ##    #    ####  #     #      ##  #',
        '#   #    #          #     #  #   #   #',
        '#   ###  #          #        #   #   #',
        '#        #          #        #       #',
        '######################################',
    ]

    s_map = SearchingMap(map_data)
    print("print parsed_map")
    s_map.print_parsed_map()
    print("print obstacles_map")
    s_map.print_obstacles_map()

    astar = Astar(s_map)

    astar.print_map(astar.end_node)
