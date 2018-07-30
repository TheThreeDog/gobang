Imports System.Reflection
Imports System.IO
Public Class 双人对战
    Dim b As Integer = 2         '奇偶变换的一个数字，用于黑白交替落子
    Dim xx As Integer = 0
    Dim yy As Integer = 0
    Dim res As Stream = Assembly.GetEntryAssembly.GetManifestResourceStream("VB五子棋.luozisheng.wav")
    Dim music(res.Length - 1) As Byte

    Private Sub 双人对战_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles MyBase.MouseDown
        Dim g As System.Drawing.Graphics = Me.CreateGraphics
        If Form1.needReStar = True Then
            If e.X >= 680 And e.X <= 733 And e.Y >= 8 And e.Y <= 61 Then
                Form1.Show()
                Me.Close()
                '返回主界面！！！！
            End If
            If e.X >= 644 And e.X <= 730 And e.Y >= 241 And e.Y <= 275 Then   '开始，即刷屏
                Form1.chongzhi(2, g)
                Form1.needReStar = False
            End If
        Else
            If b Mod 2 = 0 Then
                If e.X >= 644 And e.X <= 730 And e.Y >= 304 And e.Y <= 340 Then   ' 点在此范围内，进行悔棋操作对应图上的悔棋按钮

                    If Form1.qipan(xx, yy) = 0 Then
                        MsgBox("悔棋很麻烦")
                        '悔棋代码多麻烦！！！！！！

                    Else
                        Dim p As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 34)
                        Dim img As System.Drawing.Image
                        img = My.Resources.空白
                        g.DrawImage(img, p)
                        '用一张空图片覆盖棋子，效果就是悔棋的效果
                        Form1.qipan(xx, yy) = 0                       '将虚拟棋盘上此点清零
                        b = b - 1                                  '这有一个BUG，每次一悔棋，棋子的颜色都会变！！无奈之下，只能这样了，总之是结局了，虽然不知道这个b--是为啥。

                    End If
                    xx = 0                                    'xx  yy归零  为了消除抹去标识的时候的BUG 
                    yy = 0
                End If
                If e.X >= 680 And e.X <= 733 And e.Y >= 8 And e.Y <= 61 Then       '返回
                    Form1.Show()
                    Me.Close()
                    '返回主界面
                End If
                If e.X >= 644 And e.X <= 730 And e.Y >= 241 And e.Y <= 275 Then   '开始，即刷屏
                    Form1.chongzhi(2, g)
                    xx = 0
                    yy = 0
                End If

                If e.X >= 644 And e.X <= 730 And e.Y >= 370 And e.Y <= 403 Then   '认输
                    '黑棋胜利
                    g.DrawImage(Form1.img_heisheng, Form1.img_position)
                    MsgBox("黑棋胜利")
                    Form1.chongzhi(2, g) '刷屏
                    xx = 0
                    yy = 0

                End If

                If e.X >= 50 And e.X <= 590 And e.Y >= 50 And e.Y <= 590 Then '点在棋盘内，实现落

                    If xx <> 0 Or yy <> 0 Then
                        Dim px As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                        Dim imgx As System.Drawing.Image
                        If Form1.qipan(xx, yy) = 2 Then
                            imgx = My.Resources.黑子
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
                        Dim img As System.Drawing.Image
                        img = My.Resources.白子
                        g.DrawImage(img, p)
                        g.DrawImage(Form1.img_biaoshi, p)
                        b = b + 1
                        Form1.qipan(xx, yy) = 1
                        res.Read(music, 0, music.Length)
                        My.Computer.Audio.Play(music, AudioPlayMode.Background)
                        Form1.judge(Form1.qipan, 2, g)
                    Else
                    End If


                End If


            Else                                  '黑子的部分，基本和白子一样
                If e.X >= 644 And e.X <= 730 And e.Y >= 304 And e.Y <= 340 Then   ' 点在此范围内，进行悔棋操作对应图上的悔棋按钮

                    If Form1.qipan(xx, yy) = 0 Then
                        MsgBox("悔棋很麻烦")
                        '悔棋代码多麻烦！！！！！！

                    Else
                        Dim p As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 34)
                        Dim img As System.Drawing.Image
                        img = My.Resources.空白
                        g.DrawImage(img, p)
                        ' putimage(xx*30+35,yy*30+35,&kongbai)  '用一张空图片覆盖棋子，效果就是悔棋的效果
                        Form1.qipan(xx, yy) = 0                       '将虚拟棋盘上此点清零
                        b = b - 1                                  '这有一个BUG，每次一悔棋，棋子的颜色都会变！！无奈之下，只能这样了，总之是结局了，虽然不知道这个b--是为啥。

                    End If
                    xx = 0
                    yy = 0
                End If
                If e.X >= 680 And e.X <= 733 And e.Y >= 8 And e.Y <= 61 Then       '返回
                    Form1.Show()
                    Me.Close()
                    '返回主界面
                End If
                If e.X >= 644 And e.X <= 730 And e.Y >= 241 And e.Y <= 275 Then   '开始，即刷屏
                    Form1.chongzhi(2, g)
                    xx = 0
                    yy = 0
                End If

                If e.X >= 644 And e.X <= 730 And e.Y >= 370 And e.Y <= 403 Then   '认输
                    '白棋胜利
                    g.DrawImage(Form1.img_baisheng, Form1.img_position)
                    MsgBox("黑棋胜利")
                    Form1.chongzhi(2, g) '刷屏
                    xx = 0
                    yy = 0

                End If

                If e.X >= 50 And e.X <= 590 And e.Y >= 50 And e.Y <= 590 Then '点在棋盘内，实现落子
                    If xx <> 0 Or yy <> 0 Then
                        Dim px As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                        Dim imgx As System.Drawing.Image
                        If Form1.qipan(xx, yy) = 1 Then
                            imgx = My.Resources.白子
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
                        Dim img As System.Drawing.Image
                        img = My.Resources.黑子
                        g.DrawImage(img, p)
                        g.DrawImage(Form1.img_biaoshi, p)
                        res.Read(music, 0, music.Length)
                        My.Computer.Audio.Play(music, AudioPlayMode.Background)
                        b = b + 1
                        Form1.qipan(xx, yy) = 2
                        Form1.judge(Form1.qipan, 2, g)

                    Else
                    End If

                End If
                End If
            End If

    End Sub


    Private Sub 双人对战_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim x As Integer
        Dim y As Integer
        For x = 0 To 19 Step 1
            For y = 0 To 19 Step 1
                Form1.qipan(x, y) = 0
            Next
        Next     '重置后，虚拟棋盘全部归零
        Form1.needReStar = False
    End Sub
End Class
