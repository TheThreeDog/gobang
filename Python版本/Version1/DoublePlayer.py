# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCloseEvent

from BasePlayer import BasePlayer


class DoublePlayer(BasePlayer):
    # 双人对战窗体
    def __init__(self,parent=None):
        super().__init__(parent)


