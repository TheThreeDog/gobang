# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 20:59'

import socket
import threading
import json

from PyQt5.QtWidgets import QLabel,QMessageBox,QWidget,QLineEdit,QVBoxLayout,QHBoxLayout,QPushButton,QListWidget,QListWidgetItem
from PyQt5.QtGui import QMouseEvent,QPixmap,QIcon,QCloseEvent
from PyQt5.QtCore import QPoint,pyqtSignal,Qt
import pygame

from Base import Chessman,is_win,trans_pos
from Base import BasePlayer

from TDWidgets import TDPushButton
import Base

# addr = ("www.threedog.top",3003)
addr = ('127.0.0.1',3003)
chessboard = Base.chessboard
# 列表记录走棋坐标，用于悔棋操作
history = []

pygame.mixer.init()
pygame.mixer.music.load("source/luozisheng.wav")
sound = pygame.mixer.Sound("source/cuicu.wav")


def recv_sockdata(the_socket):
    '''从网络接收数据'''
    total_data = ""
    while True:
        data = the_socket.recv(1024).decode()
        if "END" in data:
            # 注意这里不去掉末尾的END，直接转发给另一端
            total_data += data[:data.index("END")]
            break
        total_data += data
    # print("total data:" , total_data)
    return total_data


class NetworkConfig(QWidget):
    '''
    配置网络信息的窗体
    '''

    # 传输数据的信号
    dataSignal = pyqtSignal(dict, name='data')
    #  连接中断的信号
    disconnectSignal = pyqtSignal()

    def __init__(self,main_window,parent=None):
        super().__init__(parent)
        self.setWindowTitle('网络配置')
        self.setWindowIcon(QIcon('source/icon.ico'))
        self.main_window = main_window

        self.game_window = None
        self.is_join = False
        self.keep_recv = True

        # 启动网络
        try:
            self.sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # # 设置端口复用
            self.sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock1.connect(addr)
            self.is_connected = True
            threading.Thread(target=self.recv_data,args=(self.sock1,)).start()
            self.dataSignal.connect(self.deal_data)
        except ConnectionRefusedError as e:
            QMessageBox.information(self,"消息","连接服务器失败，程序即将退出")
            raise e

        # 显示自己的昵称
        self.layout_h = QHBoxLayout()  # 水平布局1
        self.label_name = QLabel("昵称：",self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText("未命名")
        self.layout_h.addWidget(self.label_name,1)
        self.layout_h.addWidget(self.name_edit,3)

        # 玩家列表文字：
        self.layout_h1 = QHBoxLayout()  # 水平布局1
        self.label_players = QLabel("玩家列表：",self)
        self.refresh_btn = QPushButton("刷新",self)
        self.refresh_btn.clicked.connect(self.refresh)
        self.layout_h1.addWidget(self.label_players)
        self.layout_h1.addWidget(self.refresh_btn)

        # 加载玩家列表
        self.layout_h2 = QHBoxLayout()  # 水平布局1
        self.list_widget = QListWidget()
        self.refresh()  # 发送消息刷新用户列表
        self.list_widget.itemDoubleClicked.connect(self.item_double_clicked)
        self.layout_h2.addWidget(self.list_widget)

        self.layout_h3 = QHBoxLayout()  # 水平布局2
        self.join_btn = QPushButton("加入房间",self)
        self.join_btn.clicked.connect(self.join)
        self.battle_btn = QPushButton("选择对战",self)
        self.battle_btn.clicked.connect(self.battle)
        self.battle_btn.setEnabled(False)
        self.layout_h3.addWidget(self.join_btn)
        self.layout_h3.addWidget(self.battle_btn)

        self.layout_main = QVBoxLayout()  # 整体垂直布局
        self.layout_main.addLayout(self.layout_h)
        self.layout_main.addLayout(self.layout_h1)
        self.layout_main.addLayout(self.layout_h2)
        self.layout_main.addLayout(self.layout_h3)
        self.setLayout(self.layout_main)
        self.disconnectSignal.connect(self.dis_connect)

        data = {"target":"server",'msg':'get_addr','data':''}
        self.sock1.sendall((json.dumps(data)+" END").encode())

    def item_double_clicked(self,item):
        if not self.is_join:
            return  # 如果没有加入房间， 双击无效
        # print(item)
        # print(item.text())
        data = {
            "target": "server",
            "msg": "battle",
            "data": item.text()
        }
        self.sock1.sendall((json.dumps(data) + " END").encode())

    def refresh(self):
        data = {
            "target":"server",
            "msg":"refresh",
            "data":""
        }
        self.sock1.sendall((json.dumps(data)+" END").encode())

    def join(self):
        '''加入房间'''
        if not self.is_join:
            # listwidget_item = QListWidgetItem(self.name_edit.text(),self.list_widget)
            # self.list_widget.addItem(listwidget_item)
            data = {
                "target": "server",
                "msg": "join",
                "data": self.name_edit.text().strip()
            }
            # print(self.name_edit.text())
            self.sock1.sendall((json.dumps(data) + " END").encode())
            self.battle_btn.setEnabled(True)
            self.name_edit.setEnabled(False)
            self.join_btn.setText("退出房间")
            self.is_join = True
        else:
            # 退出房间
            data = {
                "target": "server",
                "msg": "quit"
                # "data": self.name_edit.text()
            }
            self.sock1.sendall((json.dumps(data) + " END").encode())
            self.battle_btn.setEnabled(False)
            self.name_edit.setEnabled(True)
            self.is_join = False
            self.join_btn.setText("加入房间")

    def battle(self):
        '''选择对战'''
        data = {
            "target": "server",
            "msg": "battle",
            "data": self.list_widget.currentItem().text()
        }
        self.sock1.sendall((json.dumps(data) + " END").encode())

    def deal_data(self,json_data):
        print("data in client :",json_data)
        '''数据处理'''
        if json_data['msg'] == 'player_list':
            # print(json_data['data'])
            self.list_widget.clear()
            for name in json_data['data']:
                self.widget_item = QListWidgetItem(name, self.list_widget)
                self.list_widget.addItem(self.widget_item)

        elif json_data['msg'] == 'get_name':  # 收到服务器分配的用户名
            self.name_edit.setText(json_data['data'])
            self.name = self.name_edit.text()

        elif json_data['msg'] == "replay":
            if json_data['type'] == 'join':  # 加入游戏失败
                QMessageBox.information(self,"消息",json_data['data'])
                self.battle_btn.setEnabled(False)
                self.name_edit.setEnabled(True)
                self.is_join = False
                self.join_btn.setText("加入房间")

            if json_data['type'] == 'battle':  # 对战
                print(json_data)
                addr = tuple(json_data['data'])# 将数据（存放的是对方的地址）转成元祖
                # self.sock1.close()
                while True:
                    try :
                        print(addr)
                        self.sock1.shutdown(socket.SHUT_RDWR)
                        self.sock1.close()
                        self.sock1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        self.sock1.connect(addr)
                        break
                    except Exception as e:
                        print(e)
                        pass
                print("连接已经建立")
                self.sock1.sendall(json.dumps({"msg":"哈哈哈哈哈哈"}).encode())

                # if json_data['data'] == True:

                    # 进入对战模式
                    # self.game_window = NetworkPlayer(sock=self.sock,name=json_data['name'])
                    # self.game_window.backSignal.connect(self.main_window.show)  # 点击后退按钮触发的信号
                    # self.game_window.exitSignal.connect(self.main_window.game_over)  # 如果程序退出，触发的信号
                    # self.game_window.show()
                    # self.close()
                # else :
                #     QMessageBox.information(self,"提示",json_data['info'])

        elif json_data['msg'] == 'get_addr':
            print(json_data["data"])
            self.sock2.bind(tuple(json_data['data']))
            print("start listen")
            self.sock2.listen(1)
            # 线程监听，等待连接
            threading.Thread(target=self.start_listen,args=(self.sock2,)).start()

    def start_listen(self,server_sock):
        print("accepting!")
        while True:
            try:
                # 接受一个新连接:
                sock, addr = server_sock.accept()
                self.tcp_socket = sock
                # 连接成功后先向对方发送昵称信息
                data = {"msg": "name", "data": self.name}
                self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                # 启动一个死循环处理数据，如果对方断开连接，会进行循环监听下次一客户端的连接
                self.recv_data(sock)
            except OSError:
                print("监听失败，socket已经失效")
                break

    def dis_connect(self):
        QMessageBox.information(self,"提示","与服务器断开连接，即将返回主界面")
        self.is_connected = False
        self.close()

    def recv_data(self,sock):
        while self.keep_recv:
            try:
                res_data = recv_sockdata(sock)     # 本地收到数据
                json_data = json.loads(res_data)        # json转成字典
                # 在线程处理函数中不能直接进行界面的相关操作，所以用一个信号把数据发送出来
                self.dataSignal.emit(json_data)
                # self.deal_data(json_data,parent)

            except (ConnectionAbortedError,ConnectionResetError):
                # print("与服务器断开连接")
                self.disconnectSignal.emit()
                break  # 退出循环，线程结束

            except json.JSONDecodeError:
                # print("数据解析错误")
                print("Error Data:",res_data)
            except OSError:
                break

    def closeEvent(self, a0: QCloseEvent):
        if self.is_connected:
            data = {
                "target": "server",
                "msg": "quit"
            }
            self.keep_recv = False # 结束接收线程
            self.sock1.sendall((json.dumps(data) + " END").encode())
        else:
            self.main_window.show()
        super().closeEvent(a0)


class NetworkPlayer(BasePlayer):
    dataSignal = pyqtSignal(dict,name='data')
    disconnectSignal = pyqtSignal()

    # 网络对战窗体
    def __init__(self,name,sock,parent=None):
        super().__init__(parent)
        self.name = name # 对方的昵称
        self.setWindowTitle('与 {} 对战中'.format(name))

        self.label_statu = QLabel("游戏状态：",self)
        self.label_statu.resize(100,20)
        self.label_statuvalue = QLabel("点击开始",self)
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
        # 保持连接
        self.keep_connect = True
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
        self.is_connected = True  # 默认情况下有连接
        self.is_listening = True  # 默认情况下启动了监听
        self.tcp_socket = sock
        self.label_statuvalue.setText("连接成功,\n点击开始")
        threading.Thread(target=self.recv_data, args=(self.tcp_socket, '')).start()

        self.dataSignal.connect(self.deal_data)
        self.disconnectSignal.connect(self.dis_connect)

    def dis_connect(self):
        QMessageBox.information(self,"提示","与服务器断开连接，即将返回主界面")
        self.back()

    def deal_data(self,data):
        '''
        对收到的数据进行处理
        '''
        print(data)
        if data['msg'] == 'action':

            if data['data'] == 'restart':
                result = QMessageBox.information(self,"消息","对方请求(重新)开始游戏，是否同意？",QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    data = {"msg": "replay", "data": True, "type":"restart","target":"player"}
                    self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                    self.restart_func()
                    self.is_over = False
                    self.my_turn = True
                    if self.my_turn:
                        self.label_statuvalue.setText("己方回合")
                    else:
                        self.label_statuvalue.setText("对方回合")
                else:
                    data = {"msg": "replay", "data": False, "type": "restart","target":"player"}
                    self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                    self.label_statuvalue.setText("点击开始")

            if data['data'] == 'lose':
                QMessageBox.information(self,"消息","对方认输")
                if self.my_turn:
                    self.win(color=self.color)
                else:
                    self.change_color()
                    self.win(color=self.color)

            if data['data'] == 'goback':
                result = QMessageBox.information(self, "消息", "对方请求悔棋，是否同意？", QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    data = {"msg": "replay", "data": True, "type": "goback","target":"player"}
                    self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                    self.goback_func()
                    # self.is_over = False
                    if self.my_turn:
                        self.label_statuvalue.setText("己方回合")
                    else:
                        self.label_statuvalue.setText("对方回合")
                else:
                    data = {"msg": "replay", "data": False, "type": "goback","target":"player"}
                    self.tcp_socket.sendall((json.dumps(data) + " END").encode())
                    # self.label_statuvalue.setText("等待开始")

            if data['data'] == 'cuicu':
                # print(self.is_connected)
                if not self.is_connected:
                    return
                if self.is_over :
                    return
                # print("cuicu")
                sound.play()
                # pygame.mixer.music.load("source/luozisheng.wav")

            if data['data'] == 'ready':
                pass

            if data['data'] == 'exit':
                # 对方退出游戏  回到游戏大厅
                print("receive exit!!!")
                self.keep_connect = False
                QMessageBox.information(self,"消息","对方退出游戏对局，即将返回游戏主界面")
                self.back()
                # self.is_connected = False
                # self.is_listening = False
                # self.tcp_socket.close()
                # self.tcp_socket = None
            # print(data)

        elif data['msg'] == 'position':
            # print(data['data'])
            # 在对应位置落子
            pos = data['data']
            if chessboard[pos[1]][pos[0]] is not None:
                return  # 如果对应位置不为空，说明有棋子，则直接返回

            self.chess = Chessman(self.color, self)
            self.chess.move(QPoint(pos[0] * 30 + 50, pos[1] * 30 + 50))
            self.chess.show()
            pygame.mixer.music.play() # 播放声音
            self.logo_move()  # 移动小标
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
            if data['type'] == 'restart': # 重开回执
                if data['data'] == True:
                    self.restart_func()
                else:
                    QMessageBox.information(self,"消息","对方拒绝了你的请求")
                    self.label_statuvalue.setText("点击开始")
                    return
                if self.my_turn:
                    self.label_statuvalue.setText("己方回合")
                else:
                    self.label_statuvalue.setText("对方回合")
            if data['type'] == 'goback': # 悔棋回执

                if data['data'] == True:
                    self.is_over = False
                    self.goback_func()
                else:
                    QMessageBox.information(self,'消息','对方拒绝了你的请求')
                if self.my_turn:
                    self.label_statuvalue.setText("己方回合")
                else:
                    self.label_statuvalue.setText("对方回合")
                self.is_over = False

        elif data['msg'] == 'name':
            self.setWindowTitle('与 {} 对战中'.format(data['data']))
        # {"msg": "self_addr", "data": sock.getpeername()}

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
        # print("start receiving data ...")
        while self.keep_connect:
            # print("start receiving data ...")
            try:
                res_data = recv_sockdata(sock)
            except (ConnectionAbortedError,ConnectionResetError):
                if self.keep_connect == False:
                    break
                # print("与服务器连接断开")
                # QMessageBox.information(self, "消息", "与服务器断开连接，即将退回到主界面")
                # QMessageBox.information(self,"提示","对方已经断开连接")
                self.is_connected = False
                # 连接断开
                # self.label_statuvalue.setText("对方断线,\n点击开始重试")
                self.disconnectSignal.emit()
                break
            try:
                data = json.loads(res_data)
                # print(type(data))
                # 在线程处理函数中不能直接进行界面的相关操作，所以用一个信号把数据发送出来
                self.dataSignal.emit(data)
            except json.decoder.JSONDecodeError as e:
                print(e)
                print("error data:\n"+res_data)
                continue
            # self.deal_data(data,parent)
        self.is_connected = False  # 连接断开
        self.tcp_socket.close()
        # self.back()

    def closeEvent(self, a0: QCloseEvent):
        self.keep_connect = False
        if self.tcp_socket is not None and self.is_connected == True:
            print("???")
            self.tcp_socket.sendall((json.dumps({"msg":"action","data":"exit","target":"player"})+" END").encode())
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
            # print("not my turn")
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
            pygame.mixer.music.play()  # 播放声音
            self.logo_move() # 移动小标
            self.change_color()

            # 在棋盘的对应位置放上棋子
            chessboard[pos[1]][pos[0]] = self.chess
            # 并且在列表中记录坐标
            history.append((pos[1], pos[0],self.chess.color))
            # 将坐标发送给另一方
            if self.tcp_socket is not None:
                data={"msg":"position","data":pos,"target":"player"}
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
        data = {"msg": "action", "data": "restart","target":"player"}
        self.tcp_socket.sendall((json.dumps(data) + " END").encode())
        self.label_statuvalue.setText("请求(重新)开始")
        self.my_turn = False

    def goback(self):
        '''
        悔棋按钮
        '''
        if self.my_turn is False:
            return # 如果是对方回合，不能悔棋
        if self.is_over:
            return
        if not self.is_connected:
            return
        else :
            data = {"msg": "action", "data": "goback","target":"player"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            self.label_statuvalue.setText("请求悔棋")
            self.is_over = True

    def goback_func(self):
        if self.is_over:
            return None  # 如果游戏已经结束了
        if len(history) == 0:
            return None  # 没有落子，不能悔棋
        chess = history.pop(-1)
        chessboard[chess[0]][chess[1]].close()
        chessboard[chess[0]][chess[1]] = None
        # self.change_color()
        if len(history) == 0:
            return None  # 没有落子，不能悔棋
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
            return
        if not self.is_connected:
            return
        else :
            data = {"msg": "action", "data": "lose","target":"player"}
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
        if self.my_turn:
            return
        if self.is_over:
            return
        if not self.is_connected:
            return
        else:
            data = {"msg": "action", "data": "cuicu","target":"player"}
            self.tcp_socket.sendall((json.dumps(data) + " END").encode())
            # self.label_statuvalue.setText("请求(重新)开始")

    def logo_move(self):
        self.chess_pos.show()
        self.chess_pos.move(self.chess.pos())
        self.chess_pos.raise_()

    def __del__(self):
        # print("析构函数被执行")
        pass

