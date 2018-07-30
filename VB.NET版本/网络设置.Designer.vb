<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class 网络设置
    Inherits System.Windows.Forms.Form

    'Form 重写 Dispose，以清理组件列表。
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Windows 窗体设计器所必需的
    Private components As System.ComponentModel.IContainer

    '注意: 以下过程是 Windows 窗体设计器所必需的
    '可以使用 Windows 窗体设计器修改它。
    '不要使用代码编辑器修改它。
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(网络设置))
        Me.Label1 = New System.Windows.Forms.Label()
        Me.textip = New System.Windows.Forms.TextBox()
        Me.Button1 = New System.Windows.Forms.Button()
        Me.黑棋 = New System.Windows.Forms.RadioButton()
        Me.白棋 = New System.Windows.Forms.RadioButton()
        Me.SuspendLayout()
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(26, 31)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(53, 12)
        Me.Label1.TabIndex = 0
        Me.Label1.Text = "IP地址："
        '
        'textip
        '
        Me.textip.Location = New System.Drawing.Point(85, 28)
        Me.textip.Name = "textip"
        Me.textip.Size = New System.Drawing.Size(235, 21)
        Me.textip.TabIndex = 3
        Me.textip.Text = "127.0.0.1"
        '
        'Button1
        '
        Me.Button1.Location = New System.Drawing.Point(243, 106)
        Me.Button1.Name = "Button1"
        Me.Button1.Size = New System.Drawing.Size(77, 50)
        Me.Button1.TabIndex = 6
        Me.Button1.Text = "确定"
        Me.Button1.UseVisualStyleBackColor = True
        '
        '黑棋
        '
        Me.黑棋.AutoSize = True
        Me.黑棋.Checked = True
        Me.黑棋.Location = New System.Drawing.Point(85, 86)
        Me.黑棋.Name = "黑棋"
        Me.黑棋.Size = New System.Drawing.Size(47, 16)
        Me.黑棋.TabIndex = 7
        Me.黑棋.TabStop = True
        Me.黑棋.Text = "黑棋"
        Me.黑棋.TextAlign = System.Drawing.ContentAlignment.MiddleRight
        Me.黑棋.UseVisualStyleBackColor = True
        '
        '白棋
        '
        Me.白棋.AutoSize = True
        Me.白棋.Location = New System.Drawing.Point(85, 140)
        Me.白棋.Name = "白棋"
        Me.白棋.Size = New System.Drawing.Size(47, 16)
        Me.白棋.TabIndex = 8
        Me.白棋.Text = "白棋"
        Me.白棋.UseVisualStyleBackColor = True
        '
        '网络设置
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 12.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(384, 207)
        Me.Controls.Add(Me.白棋)
        Me.Controls.Add(Me.黑棋)
        Me.Controls.Add(Me.Button1)
        Me.Controls.Add(Me.textip)
        Me.Controls.Add(Me.Label1)
        Me.Icon = CType(resources.GetObject("$this.Icon"), System.Drawing.Icon)
        Me.Name = "网络设置"
        Me.Text = "网络设置"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents textip As System.Windows.Forms.TextBox
    Friend WithEvents Button1 As System.Windows.Forms.Button
    Friend WithEvents 黑棋 As System.Windows.Forms.RadioButton
    Friend WithEvents 白棋 As System.Windows.Forms.RadioButton
End Class
