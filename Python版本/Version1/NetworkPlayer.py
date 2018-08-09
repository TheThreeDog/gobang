# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

import socket
import threading
import json

from PyQt5.QtWidgets import QLabel,QMessageBox,QWidget,QLineEdit,QVBoxLayout,QHBoxLayout,QPushButton
from PyQt5.QtGui import QMouseEvent,QPixmap,QIcon
from PyQt5.QtCore import QPoint

from Base import Chessman,is_win,trans_pos
from Base import BasePlayer

from TDWidgets import TDPushButton
import Base
chessboard = Base.chessboard
# 列表记录走棋坐标，用于悔棋操作
history = []


def recv_sockdata(the_socket):
    '''从网络接收数据'''
    total_data = ""
    while True:
        data = the_socket.recv(1024).decode()
        if "END" in data:
            total_data += data[:data.index("END")]
            break
        total_data += data
    # print(total_data)
    # print("-----------------")
    return total_data


class NetworkConfig(QWidget):
    '''
    配置网络信息的窗体
    '''

    def __init__(self,main_window,parent=None):
        super().__init__(parent)
        self.setWindowTitle('网络配置')
        self.setWindowIcon(QIcon('source/icon.ico'))
        self.main_window = main_window
        # 输入对方IP进行连接， 或者选择自己是主机
        self.layout_h1 = QHBoxLayout() # 水平布局1
        self.label_ip = QLabel("主机IP：",self)
        self.line_edit = QLineEdit(self)
        self.layout_h1.addWidget(self.label_ip,1)
        self.layout_h1.addWidget(self.line_edit,3)

        self.layout_h2 = QHBoxLayout() # 水平布局2
        self.connect_btn = QPushButton("连接主机",self)
        self.connect_btn.clicked.connect(self.connect_to_host)
        self.listen_btn = QPushButton("我是主机",self)
        self.listen_btn.clicked.connect(self.waiting_for_client)
        self.layout_h2.addWidget(self.connect_btn)
        self.layout_h2.addWidget(self.listen_btn)

        self.layout_main = QVBoxLayout() # 整体垂直布局
        self.layout_main.addLayout(self.layout_h1)
        self.layout_main.addLayout(self.layout_h2)
        self.setLayout(self.layout_main)
        self.game_window = None

    def connect_to_host(self):
        '''连接主机'''
        self.game_window = NetworkPlayer(ip = self.line_edit.text())
        self.game_window.exitSignal.connect(self.main_window.game_over) # 游戏结束
        self.game_window.backSignal.connect(self.main_window.show) # 返回
        self.game_window.show()
        self.close()

    def waiting_for_client(self):
        '''等待客户端'''
        self.game_window = NetworkPlayer()
        self.game_window.exitSignal.connect(self.main_window.game_over) # 游戏结束
        self.game_window.backSignal.connect(self.main_window.show) # 返回
        self.game_window.show()
        self.close()


class NetworkPlayer(BasePlayer):
    # 网络对战窗体
    def __init__(self,ip = None,parent=None):
        super().__init__(parent)
        self.ip = ip
        # 清空棋盘
        global chessboard
        chessboard = [[None for i in range(0,19)] for i in range(0,19)]
        # 默认情况下游戏是结束状态， 通过开始按钮才可以触发
        self.is_over = True
        # 标识黑旗白旗
        self.color = 'w'
        # 是否是我的回合
        self.my_turn = False
        # 三个按钮点击触发的函数
        self.restart_button.click_signal.connect(self.restart)
        self.huiqi_button.click_signal.connect(self.goback)
        self.renshu_button.click_signal.connect(self.lose)
        self.win_label = None

        self.cuicu_button = TDPushButton(self,"source/催促按钮_normal.png","source/催促按钮_hover.png","source/催促按钮_press.png",parent=self)
        self.cuicu_button.move(640,450)
        self.cuicu_button.click_signal.connect(self.cuicu)
        self.chess_pos.hide()  # 这个位置标识隐藏起来

        # 网络模块启动
        self.is_connected = False # 默认情况下没有连接
        self.is_listening = False # 默认情况下没有监听
        if self.ip is None:
            # 我是主机
            print('我是主机')
            # 创建Socket
            self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 绑定地址
            self.tcpSocket.bind(('0.0.0.0', 3003))
            # 监听端口，传入的参数指定等待连接的最大数量
            self.tcpSocket.listen(1)
            # 线程监听，等待连接
            threading.Thread(target=self.start_listen).start()

        else:
            # 连接主机
            print('连接主机')
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_addr = (ip, 3003)
            try:
                self.tcp_client.connect(server_addr)
                self.is_connected = True # 连接成功
                print("连接成功")
                threading.Thread(target=self.recv_data,args=(self.tcp_client,'')).start()
            except (ConnectionRefusedError,OSError):
                QMessageBox.information(self,"错误","网络连接失败，请点击开始按钮重试")

    def start_listen(self):
        print("accepting!")
        self.is_listening = True
        # 接受一个新连接:
        sock, addr = self.tcpSocket.accept()
        self.tcp_server = sock

        # 启动线程处理数据
        threading.Thread(target=self.recv_data,args=(sock,addr)).start()

    def recv_data(self,sock,addr):
        self.is_connected = True  # 连接状态
        print("start receiving data ...")
        while True:
            try:
                res_data = recv_sockdata(sock)
            except (ConnectionAbortedError,ConnectionResetError):
                # 连接断开
                break
            try:
                data = json.loads(res_data,encoding="utf-8")
            except json.decoder.JSONDecodeError as e:
                print("error data:\n"+res_data)
                continue

            if data['msg'] == 'action':
                if data['data'] == 'restart':
                    pass
                if data['data'] == 'lose':
                    pass
                if data['data'] == 'goback':
                    pass
                if data['data'] == 'cuicu':
                    pass
                if data['data'] == 'ready':
                    pass
                if data['data'] == 'exit':
                    pass
                print(data)
            elif data['msg'] == 'position':
                # 在对应位置落子
                pos = data['pos']
                if chessboard[pos[1]][pos[0]] is not None:
                    return  # 如果对应位置不为空，说明有棋子，则直接返回

                # 不为空，则生成棋子并显示
                self.chess = Chessman(self.color, self)
                self.chess.move(QPoint(pos[0]*30+50,pos[0]*30+50))
                self.chess.show()
                self.change_color()

                # 在棋盘的对应位置放上棋子
                chessboard[pos[1]][pos[0]] = self.chess
                # 并且在列表中记录坐标
                history.append((pos[1], pos[0], self.chess.color))
                self.my_turn = True
        self.is_connected = False  # 连接断开

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
        if not self.my_turn:
            return
        # 如果点击在棋盘区域
        if a0.x() >= 50 and a0.x() <= 50+30*19 and a0.y() >= 50 and a0.y() <= 50+30*19:

            # 讲像素坐标转化成棋盘坐标，判断棋盘此位置是否为空
            pos = trans_pos(a0)
            if chessboard[pos[1]][pos[0]] is not None:
                return # 如果对应位置不为空，说明有棋子，则直接返回

            # 不为空，则生成棋子并显示
            self.chess = Chessman(self.color,self)
            self.chess.move(a0.pos())
            self.chess.show()
            self.change_color()

            # 在棋盘的对应位置放上棋子
            chessboard[pos[1]][pos[0]] = self.chess
            # 并且在列表中记录坐标
            history.append((pos[1], pos[0],self.chess.color))
            # 将坐标发送给另一方
            data={"msg":"position","data":pos}
            if self.ip is None:
                self.tcp_server.sendall((json.dumps(data)+" END").encode())
            else:
                self.tcp_client.sendall((json.dumps(data)+" END").encode())

            # 每次落子后，都判断一下胜负
            res = is_win(chessboard)
            if res:
                self.win(res) # 通过颜色，显示胜利的图片
            self.my_turn = False

    def change_color(self):
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'

    def restart(self):
        '''
        重新开始游戏
        '''
        # 主机模式下
        if self.ip is None:
            # 连接尚未成功
            if self.is_connected == False:
                QMessageBox.information(self,"提示","对手尚未上线，请稍候")
                return
            else:
                data = {"msg":"action","data":"restart"}
                self.tcp_server.sendall((json.dumps(data) + " END").encode())
        # 客户端模式下
        else:
            # 网络未连接，重新连接
            if self.is_connected == False:
                server_addr = (self.ip, 3003)
                try:
                    self.tcp_client.connect(server_addr)
                    self.is_connected = True  # 连接成功
                    threading.Thread(target=self.recv_data, args=(self.tcp_client, ''))
                except (ConnectionRefusedError, OSError):
                    QMessageBox.information(self, "错误", "网络连接失败，请点击开始按钮重试")
                return
            else:
                data = {"msg": "action", "data": "restart"}
                self.tcp_client.sendall((json.dumps(data) + " END").encode())

    def goback(self):
        '''
        悔棋按钮
        '''
        pass

    def lose(self):
        '''
        认输按钮
        '''
        pass

    def cuicu(self):
        '''
        催促按钮
        '''
        QMessageBox.information(self,"催促","催促")