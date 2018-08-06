# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

from Base import BasePlayer
from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtGui import QCloseEvent,QPixmap,QMouseEvent
from PyQt5.QtCore import pyqtSignal

from Base import BasePlayer,Chessman,is_win,trans_pos
import Base
chessboard = Base.chessboard
# 列表记录走棋坐标，用于悔棋操作
history = []


class SinglePlayer(BasePlayer):
    '''
    单人游戏窗体
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        # 清空棋盘
        global chessboard
        chessboard = [[None for i in range(0, 19)] for i in range(0, 19)]
        self.is_over = False
        # 标识黑旗白旗
        self.color = 'w'
        # 三个按钮点击触发的函数
        self.restart_button.click_signal.connect(self.restart)
        self.huiqi_button.click_signal.connect(self.goback)
        self.renshu_button.click_signal.connect(self.lose)
        self.win_label = None

    def win(self, color):
        '''
        黑旗胜利或者白棋胜利了
        '''
        if color == 'b':
            win_pic = QPixmap('source/黑棋胜利.png')
        else:
            win_pic = QPixmap('source/白棋胜利.png')
        self.win_label = QLabel(parent=self)
        self.win_label.setPixmap(win_pic)
        self.win_label.resize(win_pic.size())
        self.win_label.move(50, 50)  # 显示游戏结束的图片
        self.win_label.show()
        self.is_over = True  # 游戏结束

    def mouseReleaseEvent(self, a0: QMouseEvent):
        if self.is_over:  # 如果游戏已经结束，点击失效
            return
        # 如果点击在棋盘区域
        if a0.x() >= 50 and a0.x() <= 50 + 30 * 19 and a0.y() >= 50 and a0.y() <= 50 + 30 * 19:

            # 讲像素坐标转化成棋盘坐标，判断棋盘此位置是否为空
            pos = trans_pos(a0)
            if chessboard[pos[1]][pos[0]] is not None:
                return  # 如果对应位置不为空，说明有棋子，则直接返回

            # 不为空，则生成棋子并显示
            self.chess = Chessman(self.color, self)
            self.chess.move(a0.pos())
            self.chess.show()
            self.change_color()

            # 在棋盘的对应位置放上棋子
            chessboard[pos[1]][pos[0]] = self.chess
            # 并且在列表中记录坐标
            history.append((pos[1], pos[0], self.chess.color))

            # 每次落子后，都判断一下胜负
            res = is_win(chessboard)
            if res:
                self.win(res)  # 通过颜色，显示胜利的图片
                return None
            # 如果没有胜利，电脑落子
            self.auto_run()

    def change_color(self):
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'

    def restart(self):
        '''
        重新开始游戏
        '''
        # 清空所有棋子
        for j in range(0, 19):
            for i in range(0, 19):
                if chessboard[i][j] is not None:
                    chessboard[i][j].close()
                    chessboard[i][j] = None
        history.clear()  # 清空历史数组
        if self.is_over:  # 如果游戏已经结束
            self.win_label.close()
            self.win_label = None
            self.is_over = False

    def goback(self):
        '''
        悔棋按钮
        '''
        if self.is_over:
            return None  # 如果游戏已经结束了
        if len(history) == 0:
            return None  # 没有落子，不能悔棋
        chess = history.pop(-1)
        chessboard[chess[0]][chess[1]].close()
        chessboard[chess[0]][chess[1]] = None
        self.change_color()

    def lose(self):
        '''
        认输按钮
        '''
        if self.is_over:
            return None  # 如果游戏已经结束了
        self.win(self.color)

    def auto_run(self):
        '''
        电脑自动执行落子操作
        :return: 自动落子
        '''
        score_c = [[0 for i in range(0,19)] for i in range(0,19)]
        score_p = [[0 for i in range(0,19)] for i in range(0,19)]

    def score(self,x,y,color):
        '''
        计分函数
        :return:，返回此坐标点落子所得的分数。
        可以得到的分数
        '''
        for i in range(x,x+5):
            if i >= 19:
                break
            if chessboard[i][y] is not None:
                if chessboard[i][y].color == color:
                    pass


