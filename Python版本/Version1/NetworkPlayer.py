# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCloseEvent

from BasePlayer import BasePlayer


class NetworkPlayer(BasePlayer):
    # 网络对战窗体
    def __init__(self,parent=None):
        super().__init__(parent)
