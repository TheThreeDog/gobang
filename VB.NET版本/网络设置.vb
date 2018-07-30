Imports System.Net

Public Class 网络设置
    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click
        网络对战.ipadr = textip.Text                   'IP地址从文本框中获取
        If 白棋.Checked = True Then                    '选择黑棋或白棋的同时，后台确定了使用的端口号
            网络对战.localport = 3003
            网络对战.duifangport = 3004
            网络对战.changeColor = True               '是否交换颜色，如果不交换，及是本地黑色，如果交换，则对方式黑色。同样根据这个变量决定认输，下棋时的状态
            网络对战.Label1.Text = "对方IP：" & textip.Text
            网络对战.Label2.Text = "对方端口:3004"
            网络对战.Label4.Text = "本地端口:3003"
        End If
        If 黑棋.Checked = True Then
            网络对战.localport = 3004
            网络对战.duifangport = 3003
            网络对战.changeColor = False
            网络对战.Label1.Text = "对方IP：" & textip.Text
            网络对战.Label2.Text = "对方端口:3003"
            网络对战.Label4.Text = "本地端口:3004"
        End If
        网络对战.Show()
        Me.Close()
    End Sub

    Private Sub 网络设置_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim HostName = System.Net.Dns.GetHostName '获得本机的机器名
        Dim ipv4 As String = String.Empty
        For Each ip As IPAddress In Dns.GetHostAddresses(HostName)      '判断是否为IPV4 过滤掉IPV6地址
            If (ip.AddressFamily.ToString = "InterNetwork") Then
                ipv4 = ip.ToString
                Exit For
            End If

        Next
        Me.Text = "网络对战   " & HostName & "-" & ipv4               '在上方显示本机IP地址
    End Sub
End Class