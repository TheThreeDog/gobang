# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/31 16:33'

from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtGui import QCloseEvent,QIcon,QPalette,QBrush,QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

from TDWidgets import TDPushButton
from TDWidgets import InvailidArguementsException


'''
棋盘信息：
    棋盘左上角坐标：（50,50）
    棋盘格子大小：（30*30）
    棋盘线数量：（19*19）
'''

chessboard = [[None for i in range(0,19)] for j in range(0,19)]
# 生成19*19的二维数组，全部初始化为None，表示没有棋子
# 注意不能使用 chessboard = [[None]*19]*19 来生成，会产生浅拷贝的问题


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

        # 落棋标志
        self.chess_pos = QLabel(self)
        pic = QPixmap("source/标识.png")
        self.chess_pos.setPixmap(pic)
        self.chess_pos.setFixedSize(pic.size())
        self.chess_pos.show()


    def closeEvent(self, a0: QCloseEvent):
        if self.is_exit: # 默认情况下，关闭窗体，退出游戏。如果点击返回按钮，则is_exit被设置为False，不触发此信号。
            self.exitSignal.emit()
        else:
            self.backSignal.emit()

    def back(self):
        self.is_exit = False
        self.close()

    def logo_move(self):
        pass


class Chessman(QLabel):
    '''
    棋子类
    '''
    def __init__(self,color,parent = None):
        super().__init__(parent=parent)
        self.pic = None
        self.color = color
        if color == 'w': # 白棋
            self.pic = QPixmap("source/白子.png")
        elif color == 'b': # 黑棋
            self.pic = QPixmap("source/黑子.png")
        else :
            raise InvailidArguementsException("构造棋子时的参数错误，请传入'b'（黑棋）或者'w'（白棋）")
        self.setFixedSize(self.pic.size())
        self.setPixmap(self.pic)

    def move(self, a0: QtCore.QPoint):
        # 通过点击点的位置，定位到棋盘的相交点上
        x = a0.x()
        y = a0.y()
        if (x - 50) % 30 <= 15:# 对三十求余小于等于15，落子在左半边的交线上
            x = (x - 50)//30*30 # 整除三十再乘以三十，目的是过滤掉除以三十的余数，使其正好落在标线上
        else :
            x = (x - 50)//30*30 + 30  # 对三十求余大于15，落子在右半边的交线上
        if (y - 50) % 30 <= 15: # 对三十求余小于等于15，落子在上半边的交线上
            y = (y - 50) // 30 * 30 # 整除三十再乘以三十，目的是过滤掉除以三十的余数，使其正好落在标线上
        else :
            y = (y - 50)//30 * 30 + 30 # 对三十求余大于15，落子在下半边的交线上

        #最后横纵坐标各减去图片的一般，并且各加上50恢复原来的坐标
        x = x - self.pic.width()/2 + 50
        y = y - self.pic.height()/2 +50
        super().move(x,y)


def trans_pos(a0: QtCore.QPoint):
    # 转化坐标，将像素坐标转化为棋盘坐标
    x = a0.x()
    y = a0.y()
    if (x - 50) % 30 <= 15:
        x = (x - 50) // 30
    else:
        x = (x - 50) // 30 + 1
    if (y - 50) % 30 <= 15:
        y = (y - 50) // 30
    else:
        y = (y - 50) // 30 + 1

    return (x,y)


def is_win(chessboard):
    '''
    判断是否已经有人胜出
    :return: 黑子胜返回'b'，白子胜返回'w',没人胜出返回False
    '''
    for j in range(0,19): # 注意这里会出现数组越界的情况，我们在代码中直接pass掉
        for i in range(0,19):
            if chessboard[i][j] is not None:
                c = chessboard[i][j].color
                # 判断右、右下、下、左下四个方向是否构成五子连珠，如果构成了，就可以。
                # 右
                try:
                    if chessboard[i+1][j] is not None:
                        if chessboard[i+1][j].color == c:
                            if chessboard[i+2][j] is not None:
                                if chessboard[i+2][j].color == c:
                                    if chessboard[i+3][j] is not None:
                                        if chessboard[i+3][j].color == c:
                                            if chessboard[i+4][j] is not None:
                                                if chessboard[i+4][j].color == c:
                                                    return c
                except IndexError:
                    pass
                # 右下
                try:
                    if chessboard[i+1][j+1] is not None:
                        if chessboard[i+1][j+1].color == c:
                            if chessboard[i+2][j+2] is not None:
                                if chessboard[i+2][j+2].color == c:
                                    if chessboard[i+3][j+3] is not None:
                                        if chessboard[i+3][j+3].color == c:
                                            if chessboard[i+4][j+4] is not None:
                                                if chessboard[i+4][j+4].color == c:
                                                    return c
                except IndexError:
                    pass
                # 下
                try:
                    if chessboard[i][j+1] is not None:
                        if chessboard[i][j+1].color == c:
                            if chessboard[i][j+2] is not None:
                                if chessboard[i][j+2].color == c:
                                    if chessboard[i][j+3] is not None:
                                        if chessboard[i][j+3].color == c:
                                            if chessboard[i][j+4] is not None:
                                                if chessboard[i][j+4].color == c:
                                                    return c
                except IndexError:
                    pass
                # 左下
                try:
                    if chessboard[i-1][j+1] is not None:
                        if chessboard[i-1][j+1].color == c:
                            if chessboard[i-2][j+2] is not None:
                                if chessboard[i-2][j+2].color == c:
                                    if chessboard[i-3][j+3] is not None:
                                        if chessboard[i-3][j+3].color == c:
                                            if chessboard[i-4][j+4] is not None:
                                                if chessboard[i-4][j+4].color == c:
                                                    return c
                except IndexError:
                    pass

    # 所有的都不成立，返回False
    return False

