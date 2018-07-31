# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/31 16:33'

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCloseEvent,QIcon,QPalette,QBrush,QPixmap
from PyQt5.QtCore import pyqtSignal

from TDWidgets import TDPushButton

class BasePlayer(QWidget):
    '''
    游戏对战窗体的基类，单人游戏，双人游戏和网络对战都是继承自这个类
    '''
    backSignal = pyqtSignal() # 点击后退按钮触发的信号
    exitSignal = pyqtSignal() # 如果程序退出，触发的信号

    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        self.is_exit = True

    def initUI(self):
        self.setFixedSize(760, 650)  # 设置固定大小
        self.move(200, 10)
        self.setWindowTitle('五子棋-三级狗')
        self.setWindowIcon(QIcon('source/icon.ico'))
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('source/游戏界面.png')))  # 设置背景图片
        self.setPalette(palette1)

        self.network_button = TDPushButton(self, 'source/联机对战_normal.png', 'source/联机对战_hover.png',
                                           'source/联机对战_press.png', parent=self)
        self.network_button.move(250, 500)
        self.network_button.show()
        self.network_button.click_signal.connect(self.back)

    def closeEvent(self, a0: QCloseEvent):
        if self.is_exit: # 默认情况下，关闭窗体，退出游戏。如果点击返回按钮，则is_exit被设置为False，不触发此信号。
            self.exitSignal.emit()
        else:
            self.backSignal.emit()

    def back(self):
        self.is_exit = False
        self.close()


