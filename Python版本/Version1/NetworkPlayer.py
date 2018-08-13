# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

import socket
import threading
import json

from PyQt5.QtWidgets import QLabel,QMessageBox,QWidget,QLineEdit,QVBoxLayout,QHBoxLayout,QPushButton
from PyQt5.QtGui import QMouseEvent,QPixmap,QIcon,QCloseEvent
from PyQt5.QtCore import QPoint,pyqtSignal,Qt

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

        # 显示自己的昵称
        self.layout_h = QHBoxLayout() # 水平布局1
        self.label_name = QLabel("昵称：",self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText("玩家1")
        self.layout_h.addWidget(self.label_name,1)
        self.layout_h.addWidget(self.name_edit,3)
        # 输入对方IP进行连接， 或者选择自己是主机
        self.layout_h1 = QHBoxLayout() # 水平布局1
        self.label_ip = QLabel("主机IP：",self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText("127.0.0.1")
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
        self.layout_main.addLayout(self.layout_h)
        self.layout_main.addLayout(self.layout_h1)
        self.layout_main.addLayout(self.layout_h2)
        self.setLayout(self.layout_main)
        self.game_window = None

    def connect_to_host(self):
        '''连接主机'''
        self.game_window = NetworkClient(name=self.name_edit.text(),ip = self.line_edit.text())
        self.game_window.exitSignal.connect(self.main_window.game_over)  # 游戏结束
        self.game_window.backSignal.connect(self.main_window.show)  # 返回
        self.game_window.show()
        self.close()

    def waiting_for_client(self):
        '''等待客户端'''
        self.game_window = NetworkServer(name=self.name_edit.text())
        self.game_window.exitSignal.connect(self.main_window.game_over)  # 游戏结束
        self.game_window.backSignal.connect(self.main_window.show)  # 返回
        self.game_window.show()
        self.close()


class NetworkPlayer(BasePlayer):
    dataSignal = pyqtSignal(dict,name='data')

    # 网络对战窗体
    def __init__(self,name,parent=None):
        super().__init__(parent)
        self.ip = None
        self.name = name
        self.label_statu = QLabel("游戏状态：",self)
        self.label_statu.resize(100,20)
        self.label_statuvalue = QLabel("等待连接",self)
        self.label_statuvalue.resize(200,30)
        self.label_statuvalue.setAlignment(Qt.AlignTop)
        self.label_statu.move(630,200)
        self.label_statuvalue.move(690,204)

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
        self.is_connected = False  # 默认情况下没有连接
        self.is_listening = False  # 默认情况下没有监听
        self.tcp_socket = None  # 默认情况下网络连接为None

        self.dataSignal.connect(self.deal_data)

    def deal_data(self,data):
        '''
        对收到的数据进行处理
        '''
        print(data)
        if data['msg'] == 'action':
            if data['data'] == 'restart':
                result = QMessageBox.information(self,"消息","对方请求(重新)开始游戏，是否同意？",QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    data = {"msg": "replay", "data": True, "type":"restart"}
                    self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                    self.restart_func()
                    self.is_over = False
                    if self.my_turn:
                        self.label_statuvalue.setText("己方回合")
                    else:
                        self.label_statuvalue.setText("对方回合")
                else:
                    data = {"msg": "replay", "data": False, "type": "restart"}
                    self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                    self.label_statuvalue.setText("等待开始")

            if data['data'] == 'lose':
                QMessageBox.information(self,"消息","对方认输")
                if self.my_turn:
                    self.change_color()
                    self.win(color=self.color)
                else:
                    self.win(color=self.color)
            if data['data'] == 'goback':
                pass
            if data['data'] == 'cuicu':
                pass
            if data['data'] == 'ready':
                pass
            if data['data'] == 'exit':
                # 对方退出游戏
                self.is_connected = False
                self.is_listening = False
                self.tcp_socket.close()
                self.tcp_socket = None
            print(data)

        elif data['msg'] == 'position':
            print(data['data'])
            # 在对应位置落子
            pos = data['data']
            if chessboard[pos[1]][pos[0]] is not None:
                return  # 如果对应位置不为空，说明有棋子，则直接返回

            self.chess = Chessman(self.color, self)
            self.chess.move(QPoint(pos[0] * 30 + 50, pos[1] * 30 + 50))
            self.chess.show()
            self.change_color()

            # 在棋盘的对应位置放上棋子
            chessboard[pos[1]][pos[0]] = self.chess
            # 并且在列表中记录坐标
            history.append((pos[1], pos[0], self.chess.color))
            # 每次落子后，都判断一下胜负
            res = is_win(chessboard)
            if res:
                self.win(res) # 通过颜色，显示胜利的图片
                return
            self.my_turn = True
            self.label_statuvalue.setText("己方回合")
        elif data['msg'] == 'replay':
            if data['type'] == 'restart':
                if data['data'] == True:
                    self.restart_func()
                else:
                    QMessageBox.information(self,"消息","对方拒绝了你的请求")
                if self.my_turn:
                    self.label_statuvalue.setText("己方回合")
                else:
                    self.label_statuvalue.setText("对方回合")
        elif data['msg'] == 'name':
            self.setWindowTitle('与 {} 对战中'.format(data['data']))

    def restart_func(self):
        # 清空所有棋子
        for j in range(0, 19):
            for i in range(0, 19):
                if chessboard[i][j] is not None:
                    chessboard[i][j].close()
                    chessboard[i][j] = None
        history.clear()  # 清空历史数组
        if self.is_over:  # 如果游戏已经结束
            if self.win_label is not None:
                self.win_label.close()
            self.win_label = None
            self.is_over = False
        self.chess_pos.hide()  # 这个位置标识隐藏起来

    def recv_data(self,sock,addr):
        self.is_connected = True  # 连接状态
        print("start receiving data ...")
        while True:
            print("start receiving data ...")
            try:
                res_data = recv_sockdata(sock)
            except (ConnectionAbortedError,ConnectionResetError):
                print("对方离开游戏")
                # QMessageBox.information(self,"提示","对方已经断开连接")
                self.is_connected = False
                # 连接断开
                self.label_statuvalue.setText("对方断线,\n点击开始重试")
                break
            try:
                data = json.loads(res_data,encoding="utf-8")
            except json.decoder.JSONDecodeError as e:
                print("error data:\n"+res_data)
                continue
            # 在线程处理函数中不能直接进行界面的相关操作，所以用一个信号把数据发送出来
            self.dataSignal.emit(data)
            # self.deal_data(data,parent)
        self.is_connected = False  # 连接断开
        self.tcp_socket.close()

    def closeEvent(self, a0: QCloseEvent):
        if self.tcp_socket is not None and self.is_connected == True:
            self.tcp_socket.sendall((json.dumps({"msg":"action","data":"exit"})).encode())
            self.tcp_socket.close()

        return super().closeEvent(a0)

    def win(self,color):
        '''
        黑旗胜利或者白棋胜利了
        '''
        if color == 'b':
            win_pic = QPixmap('source/黑棋胜利.png')
            self.label_statuvalue.setText("黑旗胜利")
        else:
            win_pic = QPixmap('source/白棋胜利.png')
            self.label_statuvalue.setText("白棋胜利")
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
            print("not my turn")
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
            if self.tcp_socket is not None:
                data={"msg":"position","data":pos}
                self.tcp_socket.sendall((json.dumps(data)+" END").encode())

            # 每次落子后，都判断一下胜负
            res = is_win(chessboard)
            if res:
                self.win(res) # 通过颜色，显示胜利的图片
                return
            self.my_turn = False
            self.label_statuvalue.setText("对方回合")

    def change_color(self):
        if self.color == 'w':
            self.color = 'b'
        else:
            self.color = 'w'

    def restart(self):
        '''
        重新开始游戏
        '''
        pass

    def goback(self):
        '''
        悔棋按钮
        '''
        if not self.is_connected:
            return
        else :
            data = {"msg": "action", "data": "goback"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            self.label_statuvalue.setText("请求悔棋")

    def lose(self):
        '''
        认输按钮
        '''
        if not self.is_connected:
            return
        else :
            data = {"msg": "action", "data": "lose"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            self.label_statuvalue.setText("对方胜利")
            if self.my_turn:
                self.change_color()
                self.win(color=self.color)
            else:
                self.win(color=self.color)

    def cuicu(self):
        '''
        催促按钮
        '''
        if not self.is_connected:
            return
        else :
            data = {"msg": "action", "data": "cuicu"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            # self.label_statuvalue.setText("请求(重新)开始")


class NetworkClient(NetworkPlayer):
    '''
    客户端类
    '''
    def __init__(self,name,ip=None,parent=None):
        super().__init__(name=name,parent=parent)
        self.ip = ip
        # 是否是我的回合
        self.my_turn = True  # 默认客户端先走棋
        self.color = "b"  #  现行执黑
        # 连接主机
        print('连接主机')
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (ip, 3003)
        try:
            self.tcp_socket.connect(server_addr)
            self.is_connected = True # 连接成功
            print("连接成功")
            self.label_statuvalue.setText("连接成功,\n点击开始")
            # 连接成功后，先发送自己的昵称信息过去
            data = {"msg": "name", "data": self.name}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            threading.Thread(target=self.recv_data,args=(self.tcp_socket,'')).start()
        except (ConnectionRefusedError,OSError):
            QMessageBox.information(self,"错误","网络连接失败，请点击开始按钮重试")
            self.label_statuvalue.setText("连接失败,\n点击开始重试")

        self.change_color()  # 保证两边黑白棋保持一致

    def restart(self):
        # 网络未连接，重新连接
        if self.is_connected == False:
            server_addr = (self.ip, 3003)
            try:
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.connect(server_addr)
                self.is_connected = True  # 连接成功
                self.label_statuvalue.setText("连接成功,\n点击开始")
                threading.Thread(target=self.recv_data, args=(self.tcp_socket, ''))
            except (ConnectionRefusedError, OSError) as e:
                print(e)
                QMessageBox.information(self, "错误", "网络连接失败，请点击开始按钮重试")
                self.label_statuvalue.setText("连接失败")
            return
        else:
            data = {"msg": "action", "data": "restart"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            self.label_statuvalue.setText("请求(重新)开始")

    def closeEvent(self, a0: QCloseEvent):
        if self.is_connected:
            self.tcp_socket.sendall((json.dumps({"msg": "action", "data": "exit"})).encode())
            self.tcp_socket.close()
            self.is_connected = False
        if self.is_listening:
            self.tcpServer.close()
            self.is_listening = False
        return super().closeEvent(a0)


class NetworkServer(NetworkPlayer):
    '''
    服务器类
    '''
    def __init__(self,name,parent=None):
        super().__init__(name=name,parent=parent)

        # 我是主机
        print('我是主机')
        # 创建Socket
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定地址
        try:
            self.tcpServer.bind(('0.0.0.0', 3003))
        except OSError as e:
            print("监听失败："+ str(e))
            QMessageBox.question(self,"监听失败","端口被占用，请关闭其他程序后点击开始按钮重试")
            print("3003 端口被占用中，请关闭其他程序后点击开始按钮重试。")
            self.label_statuvalue.setText("监听失败,\n点开始重试")
            return
        # 监听端口，传入的参数指定等待连接的最大数量
        self.tcpServer.listen(1)
        # 线程监听，等待连接
        threading.Thread(target=self.start_listen).start()

    def start_listen(self):
        print("accepting!")
        while True:
            try:
                self.is_listening = True
                self.label_statuvalue.setText("等待连接")
                # 接受一个新连接:
                sock, addr = self.tcpServer.accept()
                self.label_statuvalue.setText("连接成功,\n点击开始")
                self.tcp_socket = sock
                # 连接成功后先向对方发送昵称信息
                data = {"msg": "name", "data": self.name}
                self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                # 启动一个死循环处理数据，如果对方断开连接，会进行循环监听下次一客户端的连接
                self.recv_data(sock,addr)
            except OSError:
                print("监听失败，socket已经失效")
                break

    def restart(self):
        # 监听失败的情况
        if self.is_listening == False:
            # 绑定地址
            try:
                self.tcpServer.bind(('0.0.0.0', 3003))
            except OSError as e:
                print("监听失败：" + str(e))
                QMessageBox.question(self, "监听失败", "端口被占用，请关闭其他程序后点击开始按钮重试")
                print("3003 端口被占用中，请关闭其他程序后点击开始按钮重试。")
                self.label_statuvalue.setText("监听失败,\n点开始重试")
                return
            # 监听端口，传入的参数指定等待连接的最大数量
            self.tcpServer.listen(1)
            # 线程监听，等待连接
            threading.Thread(target=self.start_listen).start()

        # 连接尚未成功
        if self.is_connected == False:
            QMessageBox.information(self,"提示","对手尚未上线，请稍候")
            return
        else:
            data = {"msg":"action","data":"restart"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            self.label_statuvalue.setText("等待开始")

    def closeEvent(self, a0: QCloseEvent):
        if self.is_connected:
            self.tcp_socket.sendall((json.dumps({"msg": "action", "data": "exit"})).encode())
            self.tcp_socket.close()
            self.is_connected = False
        if self.is_listening:
            self.tcpServer.close()
            self.is_listening = False
        return super().closeEvent(a0)


