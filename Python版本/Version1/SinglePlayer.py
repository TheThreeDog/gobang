# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtGui import QCloseEvent,QPixmap,QMouseEvent
from PyQt5.QtCore import pyqtSignal,QPoint
import pygame

from Base import BasePlayer,Chessman,is_win,trans_pos
import Base
chessboard = Base.chessboard
# 列表记录走棋坐标，用于悔棋操作
history = []
pygame.mixer.init()
pygame.mixer.music.load("source/luozisheng.wav")


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
        self.chess_pos.hide()  # 这个位置标识隐藏起来

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
        if a0.x() >= 50 and a0.x() <= 50 + 30 * 18 + 14 and a0.y() >= 50 and a0.y() <= 50 + 30 * 18 + 14:

            # 讲像素坐标转化成棋盘坐标，判断棋盘此位置是否为空
            pos = trans_pos(a0)
            if chessboard[pos[1]][pos[0]] is not None:
                return  # 如果对应位置不为空，说明有棋子，则直接返回

            # 不为空，则生成棋子并显示
            self.chess = Chessman(self.color, self)
            self.chess.move(a0.pos())
            self.logo_move()
            self.chess.show()
            self.change_color()
            pygame.mixer.music.play()

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
        self.chess_pos.hide()  # 这个位置标识隐藏起来

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
        # self.change_color()
        chess = history.pop(-1)
        chessboard[chess[0]][chess[1]].close()
        chessboard[chess[0]][chess[1]] = None
        # self.change_color()
        self.chess_pos.hide()  # 这个位置标识隐藏起来

    def lose(self):
        '''
        认输按钮
        '''
        if self.is_over:
            return None  # 如果游戏已经结束了
        self.change_color()
        self.win(self.color)

    def auto_run(self):
        '''
        电脑自动执行落子操作
        :return: 自动落子
        '''
        # 找到能下棋的空位置中，假设电脑和人下在此处，得到分数中最大值

        score_c = [[0 for i in range(0,19)] for i in range(0,19)]
        score_p = [[0 for i in range(0,19)] for i in range(0,19)]

        # 计算所有的分数
        for j in range(0,19):
            for i in range(0,19):
                if chessboard[i][j] is None:
                    # 如果此处为空 , 计算此处分数,分别记下落黑子和落白子不同的分数
                    chessboard[i][j] = Chessman('b',parent=self)
                    score_c[i][j] += self.score(i, j, 'b')
                    chessboard[i][j] = Chessman('w',parent=self)
                    score_p[i][j] += self.score(i, j, 'w')
                    chessboard[i][j].close()
                    chessboard[i][j] = None

        # 为便于计算，将两个二维数组，转换成两个一位数组
        r_score_c = []
        for item in score_c:
            r_score_c.extend(item)

        r_score_p = []
        for item in score_p:
            r_score_p.extend(item)

        # 最终分数，取两个数组中的最大值合并成一个数组
        result = [max(a,b) for a,b in zip(r_score_c,r_score_p)]

        # 取最大值点的下标
        chess_index = result.index(max(result))
        # 通过下标计算出位置并落子
        x = chess_index // 19
        y = chess_index % 19

        self.chess = Chessman(self.color, self)
        self.chess.move(QPoint(y*30+50,x*30+50))
        self.chess.show()
        self.logo_move()
        self.change_color()
        pygame.mixer.music.play()
        chessboard[x][y] = self.chess
        history.append((x, y, self.chess.color))

        # 每次落子后，都判断一下胜负
        res = is_win(chessboard)
        if res:
            self.win(res)  # 通过颜色，显示胜利的图片
            return None

    def score(self,x,y,color):
        '''
        计分函数
        :return:，返回(x,y)坐标点落color颜色的子所得的分数。
        可以得到的分数
        '''
        blank_score = [0,0,0,0] # 四个方向空白点分数
        chess_score = [0,0,0,0] # 四个方向同色点分数

        # 右方向
        for i in range(x,x+5):
            if i >= 19:
                break
            if chessboard[i][y] is not None:
                if chessboard[i][y].color == color:# 如果是同色点，同色点分数加一
                    chess_score[0] += 1
                    # 朝一个方向执行，每次遇到相同颜色的都加1分
                else :
                    break
            else:
                # 目标点附近的点为空的，记录空白点数量
                blank_score[0] += 1
                break

        # 左方向
        for i in range(x-1,x-5,-1):
            if i <= 0 :
                break
            if chessboard[i][y] is not None:
                if chessboard[i][y].color == color:
                    chess_score[0] += 1
                else:
                    break
            else:
                blank_score[0] += 1
                break

        # 下方向
        for j in range(y,y+5):
            if j >= 19 :
                break
            if chessboard[x][j] is not None:
                if chessboard[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else :
                blank_score[1] += 1
                break

        # 上方向
        for j in range(y-1,y-5,-1):
            if j <= 0:
                break
            if chessboard[x][j] is not None:
                if chessboard[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else:
                blank_score[1] += 1
                break

        # 右下
        j = y
        for i in range(x,x+5):
            if i >= 19 or j >= 19:
                break
            if chessboard[i][j] is not None:
                if chessboard[i][j].color == color:
                    chess_score[2] += 1
                else:
                    break
            else:
                blank_score[2] += 1
                break
            j += 1

        # 左上
        j = y - 1
        for i in range(x-1, x-5, -1):
            if i <= 0 or j <= 0 :
                break
            if chessboard[i][j] is not None:
                if chessboard[i][j].color == color:
                    chess_score[2] += 1
                else:
                    break
            else:
                blank_score[2] += 1
                break
            j -= 1

        # 左下
        j = y
        for i in range(x,x-5,-1):
            if i <= 0 or j >= 19:
                break
            if chessboard[i][j] is not None:
                if chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else :
                blank_score[3] += 1
                break
            j += 1

        # 右上
        j = y - 1
        for i in range(x+1,x+5):
            if i >= 19 or j <= 0:
                break
            if chessboard[i][j] is not None:
                if chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else:
                blank_score[3] += 1
                break
            j -= 1

        # 计算总分
        for score in chess_score:
            if score > 4: # 如果有某个方向超过4，则在此处落子形成五子连珠
                return 100 # 直接返回100分的最高分

        for i in range(0,len(blank_score)):
            if blank_score[i] == 0:
                # b[]等于零说明在这空白点的附近的空白点的附近同样没有同色棋子，故分数减20
                blank_score[i] -= 20
        # 结果，将两个列表依次相加。
        result = [a+b for a,b in zip(chess_score,blank_score)]
        # 返回最高分值
        return max(result)

    def logo_move(self):
        self.chess_pos.show()
        self.chess_pos.move(self.chess.pos())
        self.chess_pos.raise_()
