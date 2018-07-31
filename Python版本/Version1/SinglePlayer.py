# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

from BasePlayer import BasePlayer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import pyqtSignal


class SinglePlayer(BasePlayer):
    '''
    单人游戏窗体
    '''
    def __init__(self,parent=None):
        super().__init__(parent)
