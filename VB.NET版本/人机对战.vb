Imports System.Reflection
Imports System.IO
Public Class 人机对战
    Private jilu() As Integer = {0, 0, 0, 0}         '记录下棋的位置，悔棋使用
    Dim res As Stream = Assembly.GetEntryAssembly.GetManifestResourceStream("VB五子棋.luozisheng.wav")     '加载落子的声音
    Dim music(res.Length - 1) As Byte
    Private xx As Integer = 0
    Private yy As Integer = 0
    Private s As Integer = 0
    Private t As Integer = 0
    Private Function score(ByVal m As Integer, ByVal n As Integer, ByVal k As Integer) As Integer   '计分函数（棋盘横纵表，纵坐标，棋子标签）
        Dim s, i, j, p, q, x, shu, heng, zuoxie, youxie As Integer '定义初始化所有计分用到的变量
        Dim b() As Integer = {0, 0, 0, 0}
        i = 0
        j = 0
        p = 0
        q = 0
        x = 0
        If k = 1 Then
            s = 1
        Else
            s = 2
        End If
        For i = m To m + 5 Step 1  '横方向
            If i < 19 Then
                If Form1.qipan(i, n) <> s Then
                    If Form1.qipan(i, n) = 0 Then
                        b(0) = b(0) + 1
                    End If
                    Exit For
                Else
                    p = p + 1     '朝一个方向进行，每次遇到相同的颜色都加一分
                End If
            End If
        Next
        For i = m - 1 To m - 5 Step -1
            If (i > 0) Then
                If Form1.qipan(i, n) <> s Then
                    If Form1.qipan(i, n) = 0 Then
                        b(0) = b(0) + 1
                    End If
                    Exit For
                Else
                    q = q + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
                End If
            End If
        Next
        heng = p + q
        j = n
        p = 0
        While j < n + 5 And j < 19                      ' 竖方向
            If Form1.qipan(m, j) <> s Then
                If Form1.qipan(m, j) = 0 Then
                    b(1) = b(1) + 1
                End If
                Exit While
            Else
                p = p + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
            End If
            j = j + 1
        End While
        j = n - 1
        q = 0
        While j > n - 5 And j > 0
            If Form1.qipan(m, j) <> s Then
                If Form1.qipan(m, j) = 0 Then
                    b(1) = b(1) + 1
                End If
                Exit While
            Else
                q = q + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
            End If
            j = j - 1
        End While
        shu = p + q

        i = m
        j = n
        p = 0
        While i < 19 And i < m + 5 And j < 19              '左斜方向
            If Form1.qipan(i, j) <> s Then
                If Form1.qipan(i, j) = 0 Then
                    b(2) = b(2) + 1
                End If
                Exit While
            Else
                p = p + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
            End If
            i = i + 1
            j = j + 1
        End While

        i = m - 1
        j = n - 1
        q = 0
        While i > 0 And i > m - 5 And j > 0
            If Form1.qipan(i, j) <> s Then
                If Form1.qipan(i, j) = 0 Then
                    b(2) = b(2) + 1
                End If
                Exit While
            Else
                q = q + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
            End If
            i = i - 1
            j = j - 1
        End While
        zuoxie = p + q

        i = m
        j = n
        p = 0
        While i > 0 And i > m - 5 And j < 19                          '  右斜部分
            If Form1.qipan(i, j) <> s Then
                If Form1.qipan(i, j) = 0 Then
                    b(3) = b(3) + 1
                End If
                Exit While
            Else
                p = p + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
            End If
            i = i - 1
            j = j + 1
        End While

        i = m + 1
        j = n - 1
        q = 0
        While i < 19 And i < m + 5 And j > 0                            '右斜部分
            If Form1.qipan(i, j) <> s Then
                If Form1.qipan(i, j) = 0 Then
                    b(3) = b(3) + 1
                End If
                Exit While
            Else
                q = q + 1   '同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
            End If
            i = i + 1
            j = j - 1
        End While
        youxie = p + q
        If (heng > 4 Or shu > 4 Or zuoxie > 4 Or youxie > 4) Then   '如果有某个方向上分数超过四分，则此处下棋就赢，用x记录分数 ，等于100；

            x = 100

        Else
            i = 0
            While i < 4
                If b(i) = 0 Then      'b()等于零说明在这空白点的附近的空白点的附近同样没有同色棋子，故分数减20
                    b(i) = -20
                End If
                i = i + 1
            End While


            x = heng + b(0)
            If shu + b(1) > x Then
                x = shu + b(1)
            End If
            If zuoxie + b(2) > x Then
                x = zuoxie + b(2)
            End If
            If youxie + b(3) > x Then
                x = youxie + b(3)     '在四个方向中选择分数最大的方向执行
            End If
        End If
        Return x            '返回此点的分数
    End Function
    Private Function ai(ByVal g As Graphics)
        Dim i, j, max As Integer
        Dim score_c(19, 19) As Integer
        Dim score_p(19, 19) As Integer
        For x As Integer = 0 To 19 Step 1            '两个数组初始化为零
            For y As Integer = 0 To 19 Step 1
                score_c(x, y) = 0     '两个额外的数组记录每个空白点的对应分数。
                score_p(x, y) = 0     '分别为电脑的分数，和玩家的分数
            Next
        Next
        For i = 1 To 18 Step 1
            For j = 1 To 18 Step 1
                If Form1.qipan(i, j) = 0 Then
                    Form1.qipan(i, j) = 1
                    score_p(i, j) += score(i, j, 1) ' 记录如果玩家下在此处，得到多少分
                    Form1.qipan(i, j) = 2
                    score_c(i, j) += score(i, j, -1) ' 记录如果电脑下在此处，得到多少分
                    Form1.qipan(i, j) = 0
                End If
            Next
        Next
        '找到能下棋的空位置中，假设电脑和人下在此处，得到分数中最大值
        s = 1
        t = 1
        max = score_c(1, 1)
        For i = 1 To 18 Step 1
            For j = 1 To 18 Step 1
                If score_c(i, j) > max Then
                    max = score_c(i, j)     '每次空点都分别计算。 电脑 玩家下载此处的值
                    s = i
                    t = j
                End If
            Next
        Next
        For i = 1 To 18 Step 1
            For j = 1 To 18 Step 1
                If score_p(i, j) > max Then      '将最大值传递给max，并且将最大的坐标传递给s，t  用在对应的qipan上
                    max = score_p(i, j)
                    s = i
                    t = j
                End If
            Next
        Next

        Form1.qipan(s, t) = 2  '在最高分处落棋
        Dim position As New System.Drawing.Point(s * 30 + 35, t * 30 + 35)
        Dim img As System.Drawing.Image
        img = My.Resources.黑子
        g.DrawImage(img, position)     '落子
        g.DrawImage(Form1.img_biaoshi, position)  '加上标识
        res.Read(music, 0, music.Length)
        My.Computer.Audio.Play(music, AudioPlayMode.Background)
        jilu(0) = s
        jilu(1) = t

    End Function
    Private Sub 人机对战_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim x As Integer
        Dim y As Integer
        For x = 0 To 18 Step 1
            For y = 0 To 18 Step 1
                Form1.qipan(x, y) = 0
            Next
        Next     '重置后，虚拟棋盘全部归零
        Form1.needReStar = False       '是否需要重新开始
    End Sub
    Private Sub 人机对战_MouseClick(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles MyBase.MouseClick
        Dim g As System.Drawing.Graphics = Me.CreateGraphics
        If Form1.needReStar = True Then           '在需要重新开始时这有这两个键有效
            If e.X >= 680 And e.X <= 733 And e.Y >= 8 And e.Y <= 61 Then
                Form1.Show()
                Me.Close()
                '返回主界面！！！！
            End If
            If (e.X >= 644 And e.X <= 730 And e.Y >= 241 And e.Y <= 275) Then  '开始
                Form1.chongzhi(1, g)
                Form1.needReStar = False
            End If
        Else
            '获取鼠标信息
            If (e.X >= 644 And e.X <= 730 And e.Y >= 304 And e.Y <= 340) Then

                If Form1.qipan(jilu(0), jilu(1)) = 0 And Form1.qipan(jilu(2), jilu(3)) = 0 Then
                    MsgBox("还有完没完啦！知道悔棋代码很麻烦么@_@")
                    '悔棋代码很麻烦！！！
                Else    '通过数组jilu来记录两次落子信息，在悔棋时实现去掉一黑一白
                    Dim p1 As New System.Drawing.Point(jilu(0) * 30 + 35, jilu(1) * 30 + 35)
                    Dim p2 As New System.Drawing.Point(jilu(2) * 30 + 35, jilu(3) * 30 + 35)
                    Dim img As System.Drawing.Image
                    img = My.Resources.空白
                    g.DrawImage(img, p1)
                    g.DrawImage(img, p2)
                    Form1.qipan(jilu(0), jilu(1)) = 0
                    Form1.qipan(jilu(2), jilu(3)) = 0
                End If
            End If


            If (e.X >= 644 And e.X <= 730 And e.Y >= 241 And e.Y <= 275) Then  '开始
                Form1.chongzhi(1, g)
            End If
            If e.X >= 680 And e.X <= 733 And e.Y >= 8 And e.Y <= 61 Then
                Form1.Show()
                Me.Close()
                '返回主界面！！！！
            End If
            If (e.X >= 644 And e.X <= 730 And e.Y >= 370 And e.Y <= 403) Then    '认输
                MsgBox("黑子获胜")
                g.DrawImage(Form1.img_heisheng, Form1.img_position)
                '黑棋子获胜
                Form1.chongzhi(1, g)
            End If

            If e.X >= 50 And e.X <= 590 And e.Y >= 50 And e.Y <= 590 Then    '棋子落在棋盘内
                If s <> 0 Or t <> 0 Then                                   '要落子先抹去上一个标识
                    Dim px As New System.Drawing.Point(s * 30 + 35, t * 30 + 35)
                    Dim imgx As System.Drawing.Image
                    If Form1.qipan(s, t) = 2 Then
                        imgx = My.Resources.黑子
                        g.DrawImage(imgx, px)
                    End If
                End If
                If (e.X - 50) Mod 30 <= 15 Then
                    xx = (e.X - 50) \ 30
                Else
                    xx = (e.X - 50) \ 30 + 1
                End If
                If ((e.Y - 50) Mod 30 <= 15) Then
                    yy = (e.Y - 50) \ 30
                Else
                    yy = (e.Y - 50) \ 30 + 1
                End If
                If Form1.qipan(xx, yy) = 0 Then

                    Dim p As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                    Dim img As System.Drawing.Image
                    img = My.Resources.白子
                    g.DrawImage(img, p)  '落子
                    g.DrawImage(Form1.img_biaoshi, p)   '加上标识
                    Form1.qipan(xx, yy) = 1             '虚拟棋盘的对应位置！
                    res.Read(music, 0, music.Length)
                    My.Computer.Audio.Play(music, AudioPlayMode.Background)
                    If Form1.judge(Form1.qipan, 1, g) = 0 Then

                        System.Threading.Thread.Sleep(500) 'Sleep(500);  电脑延迟半秒下棋
                        If xx <> 0 Or yy <> 0 Then                        '抹去再上一个位置的标识
                            Dim px As New System.Drawing.Point(xx * 30 + 35, yy * 30 + 35)
                            Dim imgx As System.Drawing.Image
                            If Form1.qipan(xx, yy) = 1 Then
                                imgx = My.Resources.白子
                                g.DrawImage(imgx, px)
                            End If
                        End If
                        ai(g)              '每下一颗白子，执行一次ai函数落个黑子。
                        Form1.judge(Form1.qipan, 1, g)
                        jilu(2) = xx
                        jilu(3) = yy

                    End If
                End If
            End If
        End If
    End Sub
End Class

