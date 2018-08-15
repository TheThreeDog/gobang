# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 14:50'

# 自定义按钮类，继承自QPushButton，实现传入图片的效果。
from PyQt5.QtWidgets import QPushButton,QWidget,QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import pyqtSignal


class InvailidArguementsException(Exception):
  '''自定义的异常类'''
  def __init__(self,msg):
      super().__init__()
      self.__msg = msg
  def __str__(self):
      return self.__msg


class TDPushButton(QLabel):
    '''
    自定义按钮，通过图片参数切换显示，支持信号和槽的回调机制
    '''
    click_signal = pyqtSignal()
    def __init__(self,*args,parent=None):
        super().__init__(parent)
        if len(args) != 4:
            raise InvailidArguementsException('构造按钮的参数错误，请按照'
                '(self,常规显示图片路径,鼠标悬停图片路径,鼠标按下图片路径)传递参数\n '
                '参数个数：{}'.format(len(args)))
        self.pic_normal = QPixmap(args[1]) # args[0]是self
        self.pic_hover = QPixmap(args[2])
        self.pic_press = QPixmap(args[3])
        self.resize(self.pic_normal.size())
        self.is_press = False
        self.setPixmap(self.pic_normal)
        self.setMask(self.pic_hover.mask())

    def enterEvent(self, a0: QtCore.QEvent):
        '''
        鼠标经过进入到控件的事件
        '''
        self.setPixmap(self.pic_hover)

    def leaveEvent(self, a0: QtCore.QEvent):
        '''
        鼠标离开控件时触发事件
        '''
        self.setPixmap(self.pic_normal)

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        '''
        鼠标按下时执行的操作
        '''
        if ev.buttons() == QtCore.Qt.LeftButton:
            self.is_press = True
            self.setPixmap(self.pic_press)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        '''
        鼠标抬起时执行的操作
        '''
        if self.is_press == True:
            self.is_press = False
            self.setPixmap(self.pic_hover)
            # 发射点击信号
            self.click_signal.emit()


