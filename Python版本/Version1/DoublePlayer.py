# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCloseEvent,QMouseEvent

from Base import BasePlayer,Chessman

class DoublePlayer(BasePlayer):
    # 双人对战窗体
    def __init__(self,parent=None):
        super().__init__(parent)

    def mouseReleaseEvent(self, a0: QMouseEvent):
        self.chess = Chessman('w',self)
        self.chess.move(a0.pos())
        self.chess.show()
        print("new chess")



