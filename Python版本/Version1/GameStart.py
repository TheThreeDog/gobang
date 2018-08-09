# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/7/30 15:09'
# 开启PyQt的Debug模式
import cgitb
cgitb.enable( format = 'error')
# 游戏的主窗体
import sys
from TDWidgets import TDPushButton
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap,QCloseEvent
from PyQt5.QtCore import pyqtSignal

from SinglePlayer import SinglePlayer
from DoublePlayer import DoublePlayer
from NetworkPlayer import NetworkPlayer,NetworkConfig

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI() # 初始化界面

    def initUI(self):
        self.setFixedSize(760, 650)# 设置固定大小
        self.move(200, 10)
        self.setWindowTitle('五子棋-三级狗')
        self.setWindowIcon(QIcon('source/icon.ico'))
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('source/五子棋界面.png')))   # 设置背景图片
        self.setPalette(palette1)
        # 加载选择按钮
        self.single_button = TDPushButton(self,'source/人机对战_normal.png','source/人机对战_hover.png','source/人机对战_press.png',parent=self)
        self.single_button.move(250,300)
        self.single_button.show()
        self.single_button.click_signal.connect(self.single_player) # 连接信号和槽，点击按钮触发函数
        self.double_button = TDPushButton(self,'source/双人对战_normal.png','source/双人对战_hover.png','source/双人对战_press.png',parent=self)
        self.double_button.move(250,400)
        self.double_button.show()
        self.double_button.click_signal.connect(self.double_player)
        self.network_button = TDPushButton(self,'source/联机对战_normal.png','source/联机对战_hover.png','source/联机对战_press.png',parent=self)
        self.network_button.move(250,500)
        self.network_button.show()
        self.network_button.click_signal.connect(self.network_player)
        self.game_window = None

    def single_player(self):
        self.close()
        self.game_window = SinglePlayer()
        self.game_window.exitSignal.connect(self.game_over) # 游戏结束
        self.game_window.backSignal.connect(self.show) # 游戏
        self.game_window.show()

    def double_player(self):
        self.close()
        self.game_window = DoublePlayer()
        self.game_window.exitSignal.connect(self.game_over) # 游戏结束
        self.game_window.backSignal.connect(self.show) # 游戏
        self.game_window.show()

    def network_player(self):
        self.close()
        self.game_window = NetworkConfig(main_window=self)
        self.game_window.show()

    def game_over(self):
        sys.exit(app.exec_())

app = None
# 游戏运行的主逻辑
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())