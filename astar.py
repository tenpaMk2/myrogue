#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpa'

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
map_width = max([len(x) for x in map_data])
map_height = len(map_data)


class Node(object):
    """
    f(n) ... startからgoalまでの最短距離
    g(n) ... startからnノードまでの最短距離
    h(n) ... nノードからgoalまでの最短距離
    f(n) = g(n) + h(n)

    関数を推定値にすることにより最短距離を予測する
    h*(n)をnからgoalまでの直線距離と仮定する。

    f*(n) = g*(n) + h*(n)
    """
    start = None  # start位置(x,y)
    goal = None  # goal位置(x,y)

    def __init__(self, x, y):
        self.pos = (x, y)
        self.hs = ((x - self.goal[0]) ** 2 + (y - self.goal[1]) ** 2) ** 0.5
        # self.hs = (x - self.goal[0]) ** 2 + (y - self.goal[1]) ** 2
        self.hs = abs(x - self.goal[0]) + abs(y - self.goal[1])
        self.fs = 0
        self.owner_list = None
        self.parent_node = None

    def is_goal(self):
        return self.goal == self.pos


class NodeList(list):
    def find(self, x, y):
        l = [t for t in self if t.pos == (x, y)]
        return l[0] if l != [] else None

    def remove(self, node):
        del self[self.index(node)]


def print_map(end_node):
    # endノードから親を辿っていくと、最短ルートを示す
    n = end_node.parent_node
    map_buffer = [[x for x in line] for line in map_data]

    while True:
        if n.parent_node == None:
            break
        map_buffer[n.pos[1]][n.pos[0]] = '+'
        n = n.parent_node

    print("n's fs : {0}".format(m.fs))
    print("\n".join(["".join(x) for x in map_buffer]))

# スタート位置とゴール位置を設定
for (i, x) in enumerate(map_data):
    if 'S' in x:
        Node.start = (x.index('S'), i)
    elif 'G' in x:
        Node.goal = (x.index('G'), i)

# OpenリストとCloseリストを設定
open_list = NodeList()
close_list = NodeList()
start_node = Node(*Node.start)
start_node.fs = start_node.hs
open_list.append(start_node)

while True:
    # Openリストが空になったら解なし
    if open_list == []:
        print("There is no route until reaching a goal.")
        exit(1)

    # Openリストからf*が最少のノードnを取得
    n = min(open_list, key=lambda x: x.fs)
    open_list.remove(n)
    close_list.append(n)

    # 最小ノードがゴールだったら終了
    if n.is_goal():
        end_node = n
        break

    # f*() = g*() + h*() -> g*() = f*() - h*()
    n_gs = n.fs - n.hs

    # ノードnの移動可能方向のノードを調べる
    for v in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        x = n.pos[0] + v[0]
        y = n.pos[1] + v[1]

        # マップが範囲外または壁(#)の場合はcontinue
        if not (0 < y < map_height and
                            0 < x < map_width and
                        map_data[y][x] != '#'):
            continue

        # 移動先のノードがOpen,Closeのどちらのリストに
        # 格納されているか、または新規ノードなのかを調べる
        m = open_list.find(x, y)
        dist = ((n.pos[0] - x) ** 2 + (n.pos[1] - y) ** 2) ** 0.5
        if m:
            # 移動先のノードがOpenリストに格納されていた場合、
            # より小さいf*ならばノードmのf*を更新し、親を書き換え
            if m.fs > n_gs + m.hs + dist:
                m.fs = n_gs + m.hs + dist
                m.parent_node = n

                print("m is in OpenList")
                print_map(m)
        else:
            m = close_list.find(x, y)
            if m:
                # 移動先のノードがCloseリストに格納されていた場合、
                # より小さいf*ならばノードmのf*を更新し、親を書き換え
                # かつ、Openリストに移動する
                if m.fs > n_gs + m.hs + dist:
                    m.fs = n_gs + m.hs + dist
                    m.parent_node = n
                    open_list.append(m)
                    close_list.remove(m)

                    print("m is in CloseList")
                    print_map(m)
            else:
                # 新規ノードならばOpenリストにノードに追加
                m = Node(x, y)
                m.fs = n_gs + m.hs + dist
                m.parent_node = n
                open_list.append(m)

                print("m is New node")
                print_map(m)

print_map(end_node)
