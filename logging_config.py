#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'tenpaMk2'

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)-5s:%(funcName)-20s:%(message)s")

# ch = logging.StreamHandler(sys.stderr)
ch = logging.StreamHandler(sys.stdout)  # 主にastarでのloggingを白字で表示する用の設定。
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

root.addHandler(ch)
