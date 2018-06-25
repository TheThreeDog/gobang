/*********************************/
/*           五子棋程序          */
/*           软一第六组          */
/*********************************/

//五子棋程序，通过easyx实现绘图，鼠标操作，界面清新。
//代码核心为五子棋算法：通过二维数组做虚拟棋盘记录信息，通过算法实现输赢，人机。
//除代码外，小组在界面设计上下了很大功夫，更易于让人们接受。
#include<graphics.h>     //c语言绘图头文件
#include<conio.h>
#pragma comment(lib,"Winmm.lib")  //加载声音文件需要

int qipan[19][19]={0};         //二维数组做虚拟棋盘，初始化为0，代表没有旗子，落子时对应位置记录1（代表白子）2（代表黑子）
int jilu[4]={0};               //落子信息的临时记录，用于悔棋
IMAGE heizi,baizi,kongbai;     // 定义 IMAGE 对象，加载图片信息
int judge (int qipan[][19],int );//判断输赢，后面的整形用于传递给chongzhi函数判断刷屏加载哪一张图片
void chongzhi (int);           //刷屏函数，参数判断刷屏后显示人机界面还是双人界面。
void doubleplayer(void);	   //双人游戏函数
void singleplayer(void);       //单人游戏函数
int score (int m,int n,int k); //记分函数，人机算法的核心：计算棋盘空白位置的分值
void ai (void);                //人机函数，计算所有可以下子位置中分值最大的落子
int main()
{
	mciSendString("open luozisheng.mp3 alias mymusic", NULL, 0, NULL);//加载音乐文件
	initgraph (760,650);       //设置画布，用于绘图  加载图片
	IMAGE img;                 //IMAGE 对象
	loadimage(&heizi,"黑子.jpg");  //装载图片
	loadimage(&baizi,"白子.jpg");
	loadimage(&kongbai,"空白.jpg");
	loadimage(&img, "五子棋界面.jpg");	// 读取图片到 img 对象中
	putimage(0, 0, &img);      //在0,0坐标位置放置图片
	MOUSEMSG n;                //定义鼠标变量
	while(1)
	{
	n=GetMouseMsg();           //获取鼠标信息
	if(n.uMsg==WM_LBUTTONDOWN) //当左键按下，坐标位置落在指定范围内时，执行对应代码，既达到了“按钮”的效果
	{
		if(n.x>=250&&n.x<=510&&n.y>=300&&n.y<=360)//选择单人游戏
		{
			chongzhi(1);
			singleplayer();
		}
		if(n.x>=250&&n.x<=510&&n.y>=435&&n.y<=500)//选择双人游戏
		{
			chongzhi(2);
			doubleplayer();
		}
	}
	}
	_getch ();
	closegraph();
	return 0;
}

int judge(int qipan[][19],int o )//判断输赢函数，扫描qipan数组中每一个点，从有子的点开始，分别往该子的左下，下，右下，右四个方向开始搜索，哪个方向出现五个相同的数字（1或2分别代表黑白），即成功。
{
	for(int i=0;i<=18;i++)
		for(int j=0;j<=18;j++)
		{
			if (qipan[i][j]==1)
			{
				if(qipan[i][j+1]==1)
				{	if(qipan[i][j+2]==1)
						if(qipan[i][j+3]==1)
							if(qipan[i][j+4]==1)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("白棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}

				}
				if(qipan[i+1][j]==1)
				{	if(qipan[i+2][j]==1)
						if(qipan[i+3][j]==1)
							if(qipan[i+4][j]==1)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("白棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
								{chongzhi(o);
								return 1;}}
				}
				if(qipan[i+1][j+1]==1)
				{	if(qipan[i+2][j+2]==1)
						if(qipan[i+3][j+3]==1)
							if(qipan[i+4][j+4]==1)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("白棋赢"), _T("结束"),MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}
				}
				if(qipan[i-1][j+1]==1)
				{	if(qipan[i-2][j+2]==1)
						if(qipan[i-3][j+3]==1)
							if(qipan[i-4][j+4]==1)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("白棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}
				}
			}

			else if(qipan[i][j]==2)
			{
				if(qipan[i][j+1]==2)
				{	if(qipan[i][j+2]==2)
						if(qipan[i][j+3]==2)
							if(qipan[i][j+4]==2)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("黑棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}
				}
				if(qipan[i+1][j]==2)
				{	if(qipan[i+2][j]==2)
						if(qipan[i+3][j]==2)
							if(qipan[i+4][j]==2)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("黑棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}
				}
				if(qipan[i+1][j+1]==2)
				{	if(qipan[i+2][j+2]==2)
						if(qipan[i+3][j+3]==2)
							if(qipan[i+4][j+4]==2)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("黑棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}
				}
				if(qipan[i-1][j+1]==2)
				{	if(qipan[i-2][j+2]==2)
						if(qipan[i-3][j+3]==2)
							if(qipan[i-4][j+4]==2)
							{HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("黑棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
							{chongzhi(o);
							return 1;}}
				}
			}
			else continue;
		}
return 0;
}
void chongzhi (int w)   //刷屏函数
{
	if(w==2)            //获取2的信息时，则加载双人游戏图片，1时加载单人游戏图片
	{
		IMAGE img;	// 定义 IMAGE 对象
		loadimage(&img, "双人对战.jpg");	// 读取图片到 img 对象中
		putimage(0, 0, &img);
	}
	else
	{
		IMAGE img;	// 定义 IMAGE 对象
		loadimage(&img, "人机对战.jpg");	// 读取图片到 img 对象中
		putimage(0, 0, &img);
	}
	for(int a=50;a<=590;a+=30)    //画出棋盘
	{
	setlinecolor(RGB(93,42,11));     //设置画线的颜色
	line(a,50,a,590);				//画线从 （a，50）到（a，590）
	line(50,a,590,a);
		for(int i=0;i<=18;i++)
		for(int j=0;j<=18;j++)
			qipan[i][j]=0;          //重置后，虚拟棋盘全部归零
	}
}
void doubleplayer ()          //双人对战函数
{
	MOUSEMSG m;
	m=GetMouseMsg();
	int b=2;                 //用于通过奇偶数实现黑子白字的改变
	int xx,yy;               //中介变量，用于把函数坐标与虚拟棋盘坐标相互转化。
		while(1)
	{
		m=GetMouseMsg();    //获取鼠标信息
		switch(m.uMsg)
	{
		case WM_LBUTTONDOWN:  //当鼠标左键按下时
		{
		if(b%2==0)
		{
			if(m.x>=644&&m.x<=730&&m.y>=304&&m.y<=340)   // 点在此范围内，进行悔棋操作对应图上的悔棋按钮
			{
				if(qipan[xx][yy]==0)
				{
					HWND wnd = GetHWnd();
					if (MessageBox(wnd, _T("还有完没完啦，知道悔棋的代码多麻烦吗!!!"), _T("卧槽!"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK);
				}
				else
				{
					putimage(xx*30+35,yy*30+35,&kongbai);  //用一张空图片覆盖棋子，效果就是悔棋的效果
					qipan[xx][yy]=0;                       //将虚拟棋盘上此点清零
					b--;                                   //这有一个BUG，每次一悔棋，棋子的颜色都会变！！无奈之下，只能这样了，总之是结局了，虽然不知道这个b--是为啥。
				}
			}
			if(m.x>=680&&m.x<=733&&m.y>=8&&m.y<=61)       //返回
			{
				main();
			}
			if(m.x>=644&&m.x<=730&&m.y>=241&&m.y<=275)   //开始，即刷屏
			{
					chongzhi(2);
			}
			if(m.x>=644&&m.x<=730&&m.y>=370&&m.y<=403)   //认输
			{
				HWND wnd = GetHWnd();
				if (MessageBox(wnd, _T("黑棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
					chongzhi(2);
			}

			if(m.x>=50 && m.x<=590&&m.y>=50 && m.y<=590 ) //点在棋盘内，实现落子
			{
			if((m.x-50)%30<=15)
				xx=(m.x-50)/30;
			else
				xx=(m.x-50)/30+1;
			if((m.y-50)%30<=15)
			yy=(m.y-50)/30;
			else
			yy=(m.y-50)/30+1;                          //让落棋位置在整点处，而不是点哪下哪。
			if(qipan[xx][yy]==0)
			{                                          //此处可以落子，则放一个棋子的图片，播放一次声音
			putimage(xx*30+35,yy*30+35,&baizi);		  //当然要将XX,YY转化为对应在画布上的坐标
			mciSendString("seek mymusic to start", 0, 0, 0);
			mciSendString("play mymusic", NULL, 0, NULL);
			b++;
			}
			else continue;
			qipan[xx][yy]=1;
			judge(qipan,2);

			}


		}
		else                                  //黑子的部分，基本和白子一样
		{

			if(m.x>=644&&m.x<=730&&m.y>=304&&m.y<=340)
			{
				if(qipan[xx][yy]==0)
				{
					HWND wnd = GetHWnd();
					if (MessageBox(wnd, _T("还有完没完啦，知道悔棋的代码多麻烦吗!!!"), _T("卧槽!"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK);
				}
				else
				{
					putimage(xx*30+35,yy*30+35,&kongbai);
					qipan[xx][yy]=0;
					b--;
				}
			}
			if(m.x>=644&&m.x<=730&&m.y>=370&&m.y<=403)
			{
				HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("白棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
								chongzhi(2);
			}
			if(m.x>=680&&m.x<=733&&m.y>=8&&m.y<=61)
			{
				main();
			}
				if(m.x>=644&&m.x<=730&&m.y>=241&&m.y<=275)
			{
					chongzhi(2);}

				if(m.x>=50 && m.x<=590 && m.y>=50 && m.y<=590)
					{
						if((m.x-50)%30<=15)
							xx=(m.x-50)/30;
						else
							xx=(m.x-50)/30+1;
						if((m.y-50)%30<=15)
							yy=(m.y-50)/30;
						else
							yy=(m.y-50)/30+1;
						if(qipan[xx][yy]==0)
						{
							putimage(xx*30+35,yy*30+35,&heizi);
							mciSendString("seek mymusic to start", 0, 0, 0);
							mciSendString("play mymusic", NULL, 0, NULL);
							b++;
						}
						else continue;
						qipan[xx][yy]=2;
						judge(qipan,2);

					}

		}

		break;

		}

	}


	}

}
void singleplayer (void)				//人机函数
{
	MOUSEMSG m;
	m=GetMouseMsg();

	int xx,yy;
		while(1)
	{
		m=GetMouseMsg();
		switch(m.uMsg)
	{
		case WM_LBUTTONDOWN:
		{

			if(m.x>=644&&m.x<=730&&m.y>=304&&m.y<=340)
			{
				if(qipan[jilu[0]][jilu[1]]==0&&qipan[jilu[2]][jilu[3]]==0)
				{
					HWND wnd = GetHWnd();
					if (MessageBox(wnd, _T("还有完没完啦，知道悔棋的代码多麻烦吗!!!"), _T("卧槽!"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK);
				}
				else    //通过数组jilu来记录两次落子信息，在悔棋时实现去掉一黑一白
				{
					putimage(jilu[0]*30+35,jilu[1]*30+35,&kongbai);
					putimage(jilu[2]*30+35,jilu[3]*30+35,&kongbai);
					qipan[jilu[0]][jilu[1]]=0;
					qipan[jilu[2]][jilu[3]]=0;
				}
			}
			if(m.x>=644&&m.x<=730&&m.y>=241&&m.y<=275)
			{
				chongzhi(1);
			}
			if(m.x>=680&&m.x<=733&&m.y>=8&&m.y<=61)
			{
				main();
			}
			if(m.x>=644&&m.x<=730&&m.y>=370&&m.y<=403)
			{
				HWND wnd = GetHWnd();
							if (MessageBox(wnd, _T("黑棋赢"), _T("结束"), MB_OKCANCEL | MB_ICONQUESTION) == IDOK)
								chongzhi(1);
			}
			if(m.x>=50 && m.x<=590&&m.y>=50 && m.y<=590 )
			{
			if((m.x-50)%30<=15)
			xx=(m.x-50)/30;
			else
			xx=(m.x-50)/30+1;
			if((m.y-50)%30<=15)
			yy=(m.y-50)/30;
			else
			yy=(m.y-50)/30+1;
			if(qipan[xx][yy]==0)
			{
			putimage(xx*30+35,yy*30+35, &baizi);
			mciSendString("seek mymusic to start", 0, 0, 0);
			mciSendString("play mymusic", NULL, 0, NULL);
			}
			else continue;
			qipan[xx][yy]=1;
			if(judge(qipan,1)==0)
			{
			Sleep(500);
			ai();              //每下一颗白子，执行一次ai函数落个黑子。
			judge(qipan,1);
			jilu[2]=xx;
			jilu[3]=yy;
			}
			}

		}
		break;

	}

	}
}

void ai (void)
{
	int k,i,j,s,t,max,p;
	int score_c[19][19]={0};             //两个额外的数组记录每个空白点的对应分数。
	int score_p[19][19]={0};             //分别为电脑的分数，和玩家的分数

	for(i=1;i<19;i++)
	{
		for(j=1;j<19;j++)
		{
			if(qipan[i][j]==0)
			{
				qipan[i][j]=1;
				score_p[i][j]+=score(i,j,1); // 记录如果玩家下在此处，得到多少分
				qipan[i][j]=2;
				score_c[i][j]+=score(i,j,-1); // 记录如果电脑下在此处，得到多少分
				qipan[i][j]=0;
			}
		}
	}
// 找到能下棋的空位置中，假设电脑和人下在此处，得到分数中最大值
	for(s=t=i=1,max=score_c[1][1];i<19;i++)
	{
		for(j=1;j<19;j++)
		{
			if(score_c[i][j]>max)
			{
				max=score_c[i][j];        //每次空点都分别计算。 电脑 玩家下载此处的值
				s=i;
				t=j;
			}
		}
	}
	for(i=1;i<19;i++)
	{
		for(j=1;j<19;j++)
		{
			if(score_p[i][j]>max)      //将最大值传递给max，并且将最大的坐标传递给s，t  用在对应的qipan上
			{
				max=score_p[i][j];
				s=i;
				t=j;
			}
		}
	}
	qipan[s][t]=2; // 在最高分处落棋
	putimage(s*30+35,t*30+35,&heizi);
	mciSendString("seek mymusic to start", 0, 0, 0);
	mciSendString("play mymusic", NULL, 0, NULL);
	jilu[0]=s;
	jilu[1]=t;
}

int score (int m,int n,int k)     //计分函数
{
	int i,j,p=0,q=0,b[4]={0},x=0,shu,heng,zuoxie,youxie;
	int s;
	if (k==1)
		s=1;
	else
		s=2;
	for(i=m;i<m+5,i<19;i++)
	{
		if(qipan[i][n]!=s)
		{
			if(qipan[i][n]==0)
			{
				b[0]++;
			}
			break;
		}
		else
			p++;        //朝一个方向执行，每次遇到相同颜色的都加1分
	}
	for(i=m-1;i>m-5,i>0;i--)
	{
		if(qipan[i][n]!=s)
		{
			if(qipan[i][n]==0)
			{
				b[0]++;
			}
			break;
		}
		else
			q++;   // 同样 先向左再向右， 左右的分数加起来，即为此点在横方向上的分数
	}
	heng=p+q;
	for(j=n,p=0;j<n+5.,j<19;j++)
	{
		if(qipan[m][j]!=s)
		{
			if(qipan[m][j]==0)
			{
				b[1]++;
			}
		break;
		}
		else
			p++;
	}
	for(j=n-1,q=0;j>n-5,j>0;j--)
	{
		if(qipan[m][j]!=s)
		{
			if(qipan[m][j]==0)
			{
				b[1]++;
			}
		break;
		}
		else
			q++;
	}
	shu=p+q;
	for(i=m,j=n,p=0;i<19,i<m+5,j<19;i++,j++)
	{
		if(qipan[i][j]!=s)
		{
			if(qipan[i][j]==0)
			{
				b[2]++;
			}
		break;
		}
		else
			p++;
	}
	for(i=m-1,j=n-1,q=0;i>0,i>m-5,j>0;i--,j--)
	{
		if(qipan[i][j]!=s)
		{
			if(qipan[i][j]==0)
			{
				b[2]++;
			}
			break;
		}
		else
			q++;
	}
	zuoxie=p+q;
	for(i=m,j=n,p=0;i>0,i>m-5,j<19;i--,j++)
	{
		if(qipan[i][j]!=s)
		{
			if(qipan[i][j]==0)
			{
				b[3]++;
			}
			break;
		}
		else
			p++;
	}
	for(i=m+1,j=n-1,q=0;i<19,i<m+5,j>0;i++,j--)
	{
		if(qipan[i][j]!=s)
		{
			if(qipan[i][j]==0)
			{
				b[3]++;
			}
			break;
		}
		else
			q++;
	}
	youxie=p+q;
	if(heng>4||shu>4||zuoxie>4||youxie>4)   //如果有某个方向上分数超过四分，则此处下棋就赢，用x记录分数 ，等于100；
	{
		x=100;
	}
	else
	{
		for(i=0;i<4;i++)
	{
	if(b[i]==0)           //b[]等于零说明在这空白点的附近的空白点的附近同样没有同色棋子，故分数减20
	{
		b[i]=-20;
	}
}
	x=heng+b[0];
	if(shu+b[1]>x)
		x=shu+b[1];
	if(zuoxie+b[2]>x)
		x=zuoxie+b[2];
	if(youxie+b[3]>x)
		x=youxie+b[3];     //在四个方向中选择分数最大的方向执行
}
return x;           //返回此点的分数
}


/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/******************软件一班*******************/
/*****************第六组制作******************/
/***************解鑫睿 2013242053*************/
/***************韩少华 2013242041*************/
/***************郝伟杰 2013242045*************/
/***************刘晓杰 2013242080*************/
/****************李颖  2013242069*************/
/***************侯倩茹 2013242049*************/
/***************柴慧超 2013242005*************/
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
