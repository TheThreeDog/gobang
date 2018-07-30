Imports System.Net.Sockets
Imports System.Threading
Imports System.Net
Imports System.Text
Imports System.Reflection
Imports System.IO
Public Class 网络对战

    Public ipadr As String                          'IP地址
    Public localport As Integer                    '本地端口号
    Public duifangport As Integer                 ' 对方端口号

    Private jilu() As Integer = {0, 0, 0, 0}        '记录悔棋信息的数组
    Private img_position As New System.Drawing.Point(109, 158)         '加载胜利图片的位置
    Private img_duifang As System.Drawing.Image = My.Resources.白子    ’对方棋子用白色
    Private img_local As System.Drawing.Image = My.Resources.黑子      '本地棋子用黑色
    Private img_heisheng As System.Drawing.Image = My.Resources.黑棋胜利
    Private img_baisheng As System.Drawing.Image = My.Resources.白棋胜利
    Private str_local As String = "黑方"                              '字符串，状态栏里用到
    Private str_duifang As String = "白方"
    Private one As Integer = 1                                       '虚拟棋盘中记录的数字，一是一二是二
    Private two As Integer = 2

    Dim res As Stream = Assembly.GetEntryAssembly.GetManifestResourceStream("VB五子棋.luozisheng.wav")
    Dim music(res.Length - 1) As Byte
    Dim xx As Integer = 0
    Dim yy As Integer = 0
    Private clicktime As Integer = 0            '开始按钮点击次数，第一次点击与不是第一次点击实行不同函数体
    Private sureexit As Boolean = False         '确定要退出
    Private isShow = False                      '关闭本窗体时是否显示Form1
    Public changeColor As Boolean = False       '默认本地黑子是否更换
    Private isFirstPlayer As Boolean = True     '先点击的先下棋
    Private can_go As Boolean = False           '是否能走棋
    Private readflag As Boolean = True  '设定是否侦听
    Private th_flag As Boolean = False
    Private th As Thread                '定义线程
    Private remote As IPEndPoint   '定义一个远程节点，获取远程计算机的IP地址和发送的信息 。
    Private udpclient As UdpClient ' = New UdpClient(11000)   '创建一个UDP服务
    Private zuobiao As String = Nothing        'send函数发送的数组


    '应用委托事件：：：！！！
    Private Delegate Sub testDelegate() '定义一个委托
    Private Sub chongzhi()   '刷屏函数
        '加载网络对战时的图片' 
        Me.BackgroundImage = My.Resources.网络对战
        Dim x As Integer
        Dim y As Integer
        For x = 0 To 18 Step 1
            For y = 0 To 18 Step 1
                Form1.qipan(x, y) = 0
            Next
        Next     '重置后，虚拟棋盘全部归零
        clicktime = 0
        Form1.needReStar = False
        isShow = False
        isFirstPlayer = True     '先点击的先下棋
        can_go = False           '是否能走棋
        readflag = True  '设定是否侦听
        th_flag = False
        xx = 0
        yy = 0
    End Sub
    Private Sub shuaping()     '刷屏函数   清空棋盘，但是大多数变量并不重置
        Me.BackgroundImage = My.Resources.网络对战
        Dim x As Integer
        Dim y As Integer
        For x = 0 To 18 Step 1
            For y = 0 To 18 Step 1
                Form1.qipan(x, y) = 0
            Next
        Next     '重置后，虚拟棋盘全部归零
        xx = 0
        yy = 0
        'can_go = False
    End Sub
    Private Sub luozione()          '委托主函数执行这个落子函数，在监听线程中委托到主线程执行
        If Form1.qipan(xx, yy) = 0 Then
            Dim p As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
            Dim gr As System.Drawing.Graphics = Me.CreateGraphics
            gr.DrawImage(img_duifang, p)    '黑子
            gr.DrawImage(Form1.img_biaoshi, p)
            res.Read(music, 0, music.Length)
            My.Computer.Audio.Play(music, AudioPlayMode.Background)
            Form1.qipan(xx, yy) = one
            Form1.judge(Form1.qipan, 3, gr)
            jilu(0) = xx
            jilu(1) = yy
            can_go = True
            Label5.Text = "状态：" & str_local & "下棋"    '本地下棋，本地是黑方或者白方
        End If

    End Sub
    Private Sub send()                  'UDP发送函数，将点击的坐标转换成字符数组再传换成byte数组发送
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress           'IP地址
        Try     '判断IP都值得正确性
            '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号（对方端口）

        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(zuobiao)   '把数组zuobiao转化成可发送的数据
        sendUdp.Connect(ipadr, duifangport)                         '建立连接，IP地址，对方端口号
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub send(ByVal _x As Integer, ByVal _y As Integer)    'send函数的重载，可以传递指定的两个整数（特殊坐标  -1-1 等）
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress
        Try     '判断IP都值得正确性
            '  remoteIP = IPAddress.Parse(text1.text)   '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号 'Convert.ToInt32(text2.text)
        Dim sendmsg As String = Nothing
        sendmsg = _x.ToString() + "," + _y.ToString()
        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(sendmsg)
        sendUdp.Connect(ipadr, duifangport)
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub send2()   '发送-2，-2 到接收方，以此类推
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress
        Try     '判断IP都值得正确性
            '  remoteIP = IPAddress.Parse(text1.text)   '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号 'Convert.ToInt32(text2.text)
        Dim sendtwo As String = "-2,-2"
        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(sendtwo)
        sendUdp.Connect(ipadr, duifangport)
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub send3()
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress
        Try     '判断IP都值得正确性
            '  remoteIP = IPAddress.Parse(text1.text)   '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号 'Convert.ToInt32(text2.text)
        Dim sendtwo As String = "-3,-3"
        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(sendtwo)
        sendUdp.Connect(ipadr, duifangport)
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub send4()
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress
        Try     '判断IP都值得正确性
            '  remoteIP = IPAddress.Parse(text1.text)   '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号 'Convert.ToInt32(text2.text)
        Dim sendtwo As String = "-4,-4"
        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(sendtwo)
        sendUdp.Connect(ipadr, duifangport)
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub send5()
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress
        Try     '判断IP都值得正确性
            '  remoteIP = IPAddress.Parse(text1.text)   '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号 'Convert.ToInt32(text2.text)
        Dim sendtwo As String = "-5,-5"
        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(sendtwo)
        sendUdp.Connect(ipadr, duifangport)
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub send6()
        Dim sendUdp As New UdpClient()     '创建UDP服务
        Dim remoteIP As IPAddress
        Try     '判断IP都值得正确性
            '  remoteIP = IPAddress.Parse(text1.text)   '里面写收到的IP地址
            remoteIP = IPAddress.Parse(ipadr)
        Catch
            MsgBox("请输入正确的 IP地址")
            Return
        End Try
        Dim remoteep As New IPEndPoint(remoteIP, duifangport)       '后面是获取的端口号 'Convert.ToInt32(text2.text)
        Dim sendtwo As String = "-6,-6"
        Dim buffer As [Byte]() = Encoding.ASCII.GetBytes(sendtwo)
        sendUdp.Connect(ipadr, duifangport)
        sendUdp.Send(buffer, buffer.Length)  '传送信息到指定计算机的txt-remoteport端口号
        sendUdp.Close()  '关闭UDP服务
    End Sub
    Private Sub repaire()           '用委托修复胜利或失败后出现的BUG 
        If Form1.needReStar = True Then
            chongzhi()
        End If
    End Sub
    Private Sub huiqi()
        Dim gr As System.Drawing.Graphics = Me.CreateGraphics
        '通过数组jilu来记录两次落子信息，在悔棋时实现去掉一黑一白
        Dim p1 As New System.Drawing.Point(jilu(0) * 30 + 35, jilu(1) * 30 + 35)
        Dim p2 As New System.Drawing.Point(jilu(2) * 30 + 35, jilu(3) * 30 + 35)
        Dim img As System.Drawing.Image
        img = My.Resources.空白
        gr.DrawImage(img, p1)
        gr.DrawImage(img, p2)
        Form1.qipan(jilu(0), jilu(1)) = 0
        Form1.qipan(jilu(2), jilu(3)) = 0
        xx = 0
        yy = 0
    End Sub
    Private Sub timerclose()        '关闭timer控件的函数
        Me.Timer1.Enabled = False
    End Sub

    '以上为委托中用到的事件，委托中不会加参数，所以导致代码特别冗余  有待改进




    Function GetEmbeddedResource(ByVal strname As String) As System.IO.Stream
        Return System.Reflection.Assembly.GetExecutingAssembly.GetManifestResourceStream(strname)
    End Function    '加载声音“能不能快一点啊，我等到花儿也谢了”
    Private Sub PlayResource()
        My.Computer.Audio.Play(GetEmbeddedResource("VB五子棋.cuicu.wav"), AudioPlayMode.Background)
    End Sub                                                   '播放催促的声音
    Private Sub read()            '不断侦听指定端口发送来的信息
        Dim g As System.Drawing.Graphics = Me.CreateGraphics  '画布定义
        remote = New IPEndPoint(IPAddress.Any, localport)     '从本地端口接受所有IP发送来的信息
        While readflag = True                                 '在线程中循环监听
            Dim receiveBytes As Byte() = udpclient.Receive(remote)  '得到对方发送来的信息
            Dim returnData As String = Encoding.ASCII.GetString(receiveBytes) '收到的byte数组转化为Sring数组
            Dim a1 As String = returnData.ToString                            '数组是以坐标形式发送的，所以以,分离得到两个数字，即横纵坐标
            Dim a As Integer = Split(a1, ",")(0)                              '横坐标
            Dim b As Integer = Split(a1, ",")(1)                              '纵坐标
            '收到特殊坐标对应处理
            If a = -2 And b = -2 Then        '拒绝重新开始                   
                MsgBox("对方拒绝了您的请求")
                Me.Invoke(New testDelegate(AddressOf timerclose))
                Label5.Text = "状态：" & str_local & "下棋"
            End If
            If a = -4 And b = -4 Then        '回应开始游戏
                can_go = True
                isFirstPlayer = False
                Me.Invoke(New testDelegate(AddressOf timerclose))
                MsgBox("对方已就绪，可以下棋")
                Label5.Text = "状态：" & str_local & "下棋"
            End If
            If a = -3 And b = -3 Then        '同意重新开始
                MsgBox("对方同意了了您的请求")
                Me.Invoke(New testDelegate(AddressOf timerclose))
                Me.Invoke(New testDelegate(AddressOf shuaping))
                can_go = True
                Label5.Text = "状态：" & str_local & "下棋"
            End If

            If a = -1 And b = -1 Then        '对方退出游戏
                Label5.Text = "状态：游戏结束"
                MsgBox("对方已退出游戏")
                udpclient.Close()
                isShow = True
                sureexit = True
                Me.Invoke(New testDelegate(AddressOf Close))
            End If
            If a = -5 And b = -5 Then      '对方回应同意悔棋请求
                MsgBox("对方同意悔棋")
                Me.Invoke(New testDelegate(AddressOf huiqi))
                Label5.Text = "状态：" & str_local & "下棋"
            End If
            If a = -6 And b = -6 Then      '对方回应拒绝悔棋请求
                MsgBox("对方拒绝了悔棋请求")
                Label5.Text = "状态：" & str_local & "下棋"
            End If

            '收到坐标信息，对应不同按钮执行不同功能
            If a >= 644 And a <= 730 And b >= 433 And b <= 468 Then     '催促
                PlayResource()
            End If
            If a >= 644 And a <= 730 And b >= 304 And b <= 340 Then      '悔棋
                Dim response As MsgBoxResult
                Label5.Text = "状态：" & str_duifang & "悔棋"
                response = MsgBox("对方请求悔棋", MsgBoxStyle.OkCancel)
                If response = MsgBoxResult.Ok Then                      '同意，发送-5 -5 
                    Me.Invoke(New testDelegate(AddressOf send5))
                    Me.Invoke(New testDelegate(AddressOf huiqi))
                    Label5.Text = "状态：" & str_duifang & "下棋"
                Else                                                    '不同意，发送 -6 -6 
                    Me.Invoke(New testDelegate(AddressOf send6))
                    Label5.Text = "状态：" & str_duifang & "下棋"
                End If

            End If
            If a >= 644 And a <= 730 And b >= 370 And b <= 403 Then   '认输
                '白棋胜利
                If changeColor = False Then                           '如果没有更换默认棋子的设置
                    Label5.Text = "状态：" & str_local & "胜利"       '“本地”胜利
                    g.DrawImage(Form1.img_heisheng, Form1.img_position) '没有更换，本地是黑棋
                    MsgBox("对方认输，黑棋胜利")
                Else
                    Label5.Text = "状态：" & str_local & "胜利"
                    g.DrawImage(Form1.img_baisheng, Form1.img_position) '更换了本地就是白旗
                    MsgBox("对方认输，白棋胜利")
                End If
                Me.Invoke(New testDelegate(AddressOf chongzhi)) '刷屏
                Label5.Text = "状态：等待重新开始"

            End If
            If a >= 644 And a <= 730 And b >= 241 And b <= 275 Then   '开始，即刷屏
                If isFirstPlayer Then                                 '第一次收到对方进入游戏，点击开始
                    can_go = False                                   '不能走棋
                    clicktime = 2
                    Timer1.Enabled = False                            '收到开始信息的话停止timer控件
                    isFirstPlayer = False                              '先按下开始的先走棋，后手的ISfirstplayer为否
                    MsgBox("对方已加入，请等待对方下棋")
                    Label5.Text = "状态：" & str_duifang & "下棋"
                    Me.Invoke(New testDelegate(AddressOf send4))        '发送-4 -4 等对方下棋
                Else
                    Dim response As MsgBoxResult                       '之后再收到  就是重新开始的意思
                    Label5.Text = "状态：对方请求重新开始"
                    Me.Invoke(New testDelegate(AddressOf repaire))
                    response = MsgBox("对方请求重新开始", MsgBoxStyle.OkCancel)
                    Form1.needReStar = False
                    If response = MsgBoxResult.Ok Then
                        Me.Invoke(New testDelegate(AddressOf send3))
                        Me.Invoke(New testDelegate(AddressOf chongzhi)) '刷屏
                        Label5.Text = "状态：" & str_duifang & "下棋"
                    Else
                        Me.Invoke(New testDelegate(AddressOf send2))
                        Label5.Text = "状态：" & str_duifang & "下棋"
                    End If

                End If
                isFirstPlayer = False
                clicktime = 1
            End If
            If can_go = False Then
                If a >= 50 And a <= 590 And b >= 50 And b <= 590 Then '点在棋盘内，实现落子
                    If xx <> 0 Or yy <> 0 Then                       '先去掉上一个标识
                        Dim px As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                        Dim imgx As System.Drawing.Image
                        If True Then
                            imgx = img_local
                            g.DrawImage(imgx, px)
                        End If
                    End If
                    If (a - 50) Mod 30 <= 15 Then
                        xx = (a - 50) \ 30
                    Else
                        xx = (a - 50) \ 30 + 1
                    End If
                    If (b - 50) Mod 30 <= 15 Then
                        yy = (b - 50) \ 30
                    Else
                        yy = (b - 50) \ 30 + 1    '让落棋位置在整点处，而不是点哪下哪。
                    End If
                    Me.Invoke(New testDelegate(AddressOf luozione))   '委托主线程执行落子
                End If
            End If
        End While
    End Sub


    Private Sub 网络对战_MouseClick(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles MyBase.MouseClick

        zuobiao = e.X.ToString() + "," + e.Y.ToString()      '把点击点的横纵坐标封装在zuobiao数组中发送

        Dim g As System.Drawing.Graphics = Me.CreateGraphics

        If Form1.needReStar = True Then                     '如果需要冲新开始比如有一方认输后
            Label5.Text = "状态：等待重新开始"
            chongzhi()
            Form1.needReStar = False
        Else

            If can_go = False Then                      '在可以走棋时
                If clicktime = 0 Then                  '若点击次数为0，提示可以开始游戏
                    If e.X >= 50 And e.X <= 590 And e.Y >= 50 And e.Y <= 590 Then MsgBox("现在可以开始游戏")
                ElseIf clicktime = 1 And Not (e.X >= 644 And e.X <= 730 And e.Y >= 433 And e.Y <= 468) Then
                    MsgBox("请等待对方操作")            '若不是0，说明还没轮到自己操作
                End If
            End If
            If e.X >= 644 And e.X <= 730 And e.Y >= 433 And e.Y <= 468 Then      '催促
                If can_go = False Then
                    PlayResource()
                    send()
                End If
            End If
            If e.X >= 644 And e.X <= 730 And e.Y >= 241 And e.Y <= 275 Then   '开始，即刷屏
                If isFirstPlayer Then
                    Timer1.Enabled = False
                    Timer1.Enabled = True                '开启timer控件，若10秒内对方没操作，就提示再次按下开始
                    send()
                    'isFirstPlayer = False
                    clicktime = 1
                    Label5.Text = "状态：等待对方回应"   '状态栏随时改变

                    'Form1.chongzhi(2, g) 
                End If
                If can_go Then
                    Label5.Text = "状态：请求重新开始"
                    send()
                End If
            End If

            If can_go Then
                If e.X >= 644 And e.X <= 730 And e.Y >= 304 And e.Y <= 340 And isFirstPlayer = False Then      '悔棋
                    If Form1.qipan(jilu(0), jilu(1)) = 0 And Form1.qipan(jilu(2), jilu(3)) = 0 Then
                        Label5.Text = "状态：" & str_local & "请求悔棋"
                        MsgBox("还有完没完啦！悔棋代码费死脑细胞好嘛！！！")
                        Label5.Text = "状态：" & str_local & "下棋"
                        '悔棋代码很麻烦！！！
                    Else
                        Label5.Text = "状态：" & str_local & "请求悔棋"    '本地请求悔棋
                        send()
                    End If
                End If
                If e.X >= 680 And e.X <= 733 And e.Y >= 8 And e.Y <= 61 Then       '返回
                    isShow = True
                    Me.Close()
                    '返回主界面
                End If
                If e.X >= 644 And e.X <= 730 And e.Y >= 370 And e.Y <= 403 Then   '认输
                    '白棋胜利
                    send()
                    If changeColor = False Then
                        g.DrawImage(Form1.img_baisheng, Form1.img_position)   '如果没有换，就是黑棋认输
                    Else
                        g.DrawImage(Form1.img_heisheng, Form1.img_position)   '反之白旗认输
                    End If
                    Label5.Text = "状态：" & str_duifang & "胜利"
                    MsgBox(str_duifang & "胜利")
                    chongzhi() '刷屏
                    Label5.Text = "状态：等待重新开始"
                End If
                If e.X >= 50 And e.X <= 590 And e.Y >= 50 And e.Y <= 590 And clicktime = 1 Then '点在棋盘内，实现落子
                    If xx <> 0 Or yy <> 0 Then
                        Dim px As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                        Dim imgx As System.Drawing.Image
                        If Form1.qipan(xx, yy) = one Then
                            imgx = img_duifang
                            g.DrawImage(imgx, px)
                        End If
                    End If
                    If (e.X - 50) Mod 30 <= 15 Then
                        xx = (e.X - 50) \ 30
                    Else
                        xx = (e.X - 50) \ 30 + 1
                    End If
                    If (e.Y - 50) Mod 30 <= 15 Then
                        yy = (e.Y - 50) \ 30
                    Else
                        yy = (e.Y - 50) \ 30 + 1    '让落棋位置在整点处，而不是点哪下哪。
                    End If
                    If Form1.qipan(xx, yy) = 0 Then
                        Dim p As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                        g.DrawImage(img_local, p)
                        g.DrawImage(Form1.img_biaoshi, p)
                        res.Read(music, 0, music.Length)
                        My.Computer.Audio.Play(music, AudioPlayMode.Background)
                        can_go = False
                        Form1.qipan(xx, yy) = two
                        send()
                        Form1.judge(Form1.qipan, 3, g)
                        Label5.Text = "状态：" & str_duifang & "下棋"
                        jilu(2) = xx                                      '记录下骡子的位置，悔棋要用
                        jilu(3) = yy
                    Else
                    End If
                End If
            End If
        End If

    End Sub

    Private Sub 网络对战_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim HostName = System.Net.Dns.GetHostName '获得本机的机器名
        Dim ipv4 As String = String.Empty
        For Each ip As IPAddress In Dns.GetHostAddresses(HostName) '过滤掉IPV6地址
            If (ip.AddressFamily.ToString = "InterNetwork") Then
                ipv4 = ip.ToString
                Exit For
            End If

        Next
        Me.Text = "网络对战   " & HostName & "-" & ipv4
        Label5.Text = "状态：等待链接"
        Label3.Text = "本地IP：" & ipv4

        If changeColor Then                     '如果更换，及本地是白旗，那么本地字符串就是白方， 一是二，二是一
            str_local = "白方"
            str_duifang = "黑方"
            img_duifang = My.Resources.黑子
            img_local = My.Resources.白子
            one = 2
            two = 1
        Else
            str_local = "黑方"
            str_duifang = "白方"
            img_duifang = My.Resources.白子
            img_local = My.Resources.黑子
            one = 1
            two = 2
        End If
        udpclient = New UdpClient(localport)                 '新启动一个UDP服务器，本地端口号
        th = New Thread(New ThreadStart(AddressOf read))  '创建一个线程
        th.IsBackground = True                           '后台线程会自行销毁
        th_flag = True
        th.Start()    '启动线程
        Form1.needReStar = False
    End Sub

    Private Sub 网络对战_FormClosing(ByVal sender As System.Object, ByVal e As System.Windows.Forms.FormClosingEventArgs) Handles MyBase.FormClosing
        If sureexit = True Then             '窗体关闭的时候，TRUE是收到了关闭的信息，所以要强行退出，else是自己点的退出
            If isShow = True Then
                Form1.Show()
            End If
            th.Abort()
            udpclient.Close()
        Else
            Dim response As MsgBoxResult
            response = MsgBox("确定要退出？", MsgBoxStyle.OkCancel)
            If response = MsgBoxResult.Ok Then
                e.Cancel = False
                If isShow = True Then
                    Form1.Show()
                End If
                send(-1, -1)             '关闭时发送自己的关闭信息
                th.Abort()
                udpclient.Close()
            Else
                e.Cancel = True

            End If
        End If


    End Sub

    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick
        Me.Label5.Text = ("状态：无响应，请重试")   'timer控件10秒执行一次，如果对面响应了，就会关闭这个控件
        MsgBox("对方无响应，请重试")
        isFirstPlayer = True
        clicktime = 0
    End Sub
End Class