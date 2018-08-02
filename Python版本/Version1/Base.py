# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/31 16:33'

from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtGui import QCloseEvent,QIcon,QPalette,QBrush,QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

from TDWidgets import TDPushButton
from TDWidgets import InvailidArguementsException


class BasePlayer(QWidget):
    '''
    游戏对战窗体的基类，单人游戏，双人游戏和网络对战都是继承自这个类，这个类中实现并加载了了所有公共的控件
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

        self.back_button = TDPushButton(self,'source/返回按钮_normal.png','source/返回按钮_hover.png','source/返回按钮_press.png',parent=self)
        self.back_button.click_signal.connect(self.back)
        self.back_button.move(680,10)
        self.restart_button = TDPushButton(self,'source/开始按钮_normal.png','source/开始按钮_hover.png','source/开始按钮_press.png',parent=self)
        self.restart_button.move(640,240)
        self.huiqi_button = TDPushButton(self, 'source/悔棋按钮_normal.png', 'source/悔棋按钮_hover.png','source/悔棋按钮_press.png', parent=self)
        self.huiqi_button.move(640,310)
        self.renshu_button = TDPushButton(self, 'source/认输按钮_normal.png', 'source/认输按钮_hover.png','source/认输按钮_press.png', parent=self)
        self.renshu_button.move(640,380)


    def closeEvent(self, a0: QCloseEvent):
        if self.is_exit: # 默认情况下，关闭窗体，退出游戏。如果点击返回按钮，则is_exit被设置为False，不触发此信号。
            self.exitSignal.emit()
        else:
            self.backSignal.emit()

    def back(self):
        self.is_exit = False
        self.close()


class Chessman(QLabel):
    def __init__(self,color,parent = None):
        super().__init__(parent=parent)
        self.pic = None
        self.color = color
        if color == 'w': # 白棋
            self.pic = QPixmap("source/白子.png")
        elif color == 'b': # 黑棋
            self.pic = QPixmap("source/黑子.jpg")
        else :
            raise InvailidArguementsException("构造棋子时的参数错误，请传入'b'（黑棋）或者'w'（白棋）")
        print(self.pic.size().width())
        self.setFixedSize(self.pic.size())
        self.setPixmap(self.pic)

    def move(self, a0: QtCore.QPoint):
        # 这个操作相当于修改了棋子的锚点，将棋子的中心移动到相应位置
        super().move(a0.x()-self.pic.width()/2,a0.y()-self.pic.height()/2)
