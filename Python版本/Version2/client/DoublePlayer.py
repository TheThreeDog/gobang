# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent,QPixmap
import pygame

from Base import BasePlayer,Chessman,is_win,trans_pos
import Base
chessboard = Base.chessboard
# 列表记录走棋坐标，用于悔棋操作
history = []
# 加载声音
pygame.mixer.init()
pygame.mixer.music.load("source/luozisheng.wav")


class DoublePlayer(BasePlayer):
    # 双人对战窗体
    def __init__(self,parent=None):
        super().__init__(parent)
        # 清空棋盘
        global chessboard
        chessboard = [[None for i in range(0,19)] for i in range(0,19)]
        self.is_over = False
        # 标识黑旗白旗
        self.color = 'w'
        # 三个按钮点击触发的函数
        self.restart_button.click_signal.connect(self.restart)
        self.huiqi_button.click_signal.connect(self.goback)
        self.renshu_button.click_signal.connect(self.lose)
        self.win_label = None
        self.chess_pos.hide()  # 这个位置标识隐藏起来

    def win(self,color):
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
        if self.is_over: # 如果游戏已经结束，点击失效
            return
        # 如果点击在棋盘区域
        if a0.x() >= 50 and a0.x() <= 50+30*18+14 and a0.y() >= 50 and a0.y() <= 50+30*18+14:
            # 讲像素坐标转化成棋盘坐标，判断棋盘此位置是否为空
            pos = trans_pos(a0)
            if chessboard[pos[1]][pos[0]] is not None:
                return # 如果对应位置不为空，说明有棋子，则直接返回

            # 不为空，则生成棋子并显示
            self.chess = Chessman(self.color,self)
            self.chess.move(a0.pos())
            self.logo_move()
            self.chess.show()
            self.change_color()
            pygame.mixer.music.play()

            # 在棋盘的对应位置放上棋子
            chessboard[pos[1]][pos[0]] = self.chess
            # 并且在列表中记录坐标
            history.append((pos[1], pos[0],self.chess.color))

            # 每次落子后，都判断一下胜负
            res = is_win(chessboard)
            if res:
                self.win(res) # 通过颜色，显示胜利的图片

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
        for j in range(0,19):
            for i in range(0,19):
                if chessboard[i][j] is not None:
                    chessboard[i][j].close()
                    chessboard[i][j] = None
        history.clear() #清空历史数组
        if self.is_over: # 如果游戏已经结束
            self.win_label.close()
            self.win_label = None
            self.is_over = False
        self.chess_pos.hide() # 这个位置标识隐藏起来

    def goback(self):
        '''
        悔棋按钮
        '''
        if self.is_over:
            return None # 如果游戏已经结束了
        if len(history) == 0:
            return None # 没有落子，不能悔棋
        chess = history.pop(-1)
        chessboard[chess[0]][chess[1]].close()
        chessboard[chess[0]][chess[1]] = None
        self.change_color()
        self.chess_pos.hide()  # 这个位置标识隐藏起来

    def lose(self):
        '''
        认输按钮
        '''
        if self.is_over:
            return None # 如果游戏已经结束了
        self.win(self.color)

    def logo_move(self):
        self.chess_pos.show()
        self.chess_pos.move(self.chess.pos())
        self.chess_pos.raise_()