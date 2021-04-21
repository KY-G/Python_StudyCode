'''''''''''''''''''''''''''''''''2021.03.10''''''''''''''''''''''''''''''''''''''
简单的小球运动程序
    全屏显示，大小可调
    按下开始按钮小球开始横向位移，再次点击按钮小球停止，再次点击即运动
    点击复位后，小球回到原点，再次等待点击开始
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''2021.03.11''''''''''''''''''''''''''''''''''''''
通过串口接收来自Tobii的凝视点数据，并在凝视点处打点
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''2021.03.12''''''''''''''''''''''''''''''''''''''
点击复位按钮，幕布上打出的所有凝视点全部清空
添加功能，在列表中保存所有眼动数据，最后再挨个读取。
再添加两个按钮，一个是在小球运动时屏幕上不打点，但数据在后台保存，最后一起打印出来
            另一个按钮是显示眼动的分析结果
显示分析的结果，分析时将所有读到的点打印图形在屏幕上显示
    简单分析坐标点之间的关系：求出每两个点之间的直线距离和。换算成mm单位
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''2021.03.26''''''''''''''''''''''''''''''''''''''
加入校准程序
    通过调用 os 类库，执行shell命令，进行Tobii的快捷校准
        此校准是临时校准，掉电、重启丢失，校准数据保持原来的用户校准（上一次用正式校准校出的头模数据）
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
下一步计划：
        未知
尚存问题：
    求解出的两个点之间的直线距离累加和好像不太准。
    校准，用模拟快捷键的方式调用Tobii自带的正式校准（Ctrl+Shift+F10）
        校准后会新建一个用户数据，替代当前正式校准用户，掉电、重启不丢失。
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from tkinter import *
import random
import time
import serial
import math
import os

start_flag = 0
ballRun_flag = 0

gaze_point_flag = 0
gaze_start_print = 0
GazePoint_Alldistance = 0
gaze_point_listX = []
gaze_point_listY = []
gaze_pictureID_list = []

data_x = 0
data_y = 0
ball_id = 0
data_StartRecrive = False
start_button_flag = False
NoRectangle_button_flag = False

DataAnalysis_count = 0
Data_text_id = 0

Calibration_complete = False

#定义点的类
class Point:
  def __init__(self,x=0,y=0):
    self.x=x
    self.y=y
  def getx(self):
    return self.x
  def gety(self):
    return self.y

#定义直线类
class Getlen:
  def __init__(self,p1,p2):
    self.x=p1.getx()-p2.getx()
    self.y=p1.gety()-p2.gety()
    #用math.sqrt（）求平方根
    self.len= math.sqrt((self.x**2)+(self.y**2))
  #定义得到直线长度的函数
  def getlen(self):
    return self.len

#创建凝视点类
class Eyes_gaze_point:
    def __init__(self,canvas, color):
        self.canvas = canvas# 把参数canvas赋值给对象变量canvas
        #self.id = canvas.create_rectangle(0, 0, 10, 10, fill="red")
        #self.canvas.move(self.id, 800, 0)  # 代表凝视点移动的初始位置，图形用id表示
        self.x = 0  # 设置对象变量x，初始值为0.也就是图形先不移动
        self.y = 0  # 设置对象变量y，初始值为0.也就是图形先不移动
        self.canvas_width = self.canvas.winfo_width()  # 获取画布的宽度
        self.canvas.bind_all("<Button-1>", self.Gaze_point_Move)  # 初始化时将事件‘鼠标左键单击’和函数移动绑定
        #self.canvas.bind_all('<KeyPress-Right>', self.turn_right)  # 初始化时将事件‘按下右键’和函数向右移动绑定
        self.canvas_height = self.canvas.winfo_height()  # 获取画布的高度，画布高度是从上到下计量的
        self.canvas_width = self.canvas.winfo_width()  # 获取画布的宽度


    def Gaze_point_Move(self,event):
        pass
        #if event.num == 1:
            #print("鼠标点击有效")
            #print(event.x)
            #print(event.y)
            #print(event)
            #self.id = canvas.create_rectangle(0, 0, 5, 5, fill="green")
            #self.canvas.move(self.id, event.x, event.y)  # 代表凝视点移动的初始位置，图形用id表示
            # self.x = 1
            # self.y = 0
            #print(self.canvas_height)
            #print(self.canvas_width)

    def draw(self,data_x,data_y):  # 定义凝视点的画图动作
        global gaze_point_flag,gaze_pictureID_list
        if(gaze_point_flag == 1 and gaze_start_print == 1):
            self.id = canvas.create_rectangle(0, 0, 5, 5, fill="green")
            #print("凝视点id：%d"%self.id)#从3开始全都是
            gaze_pictureID_list.append(self.id)  #将所有画过的图形id放入队列中
            self.canvas.move(self.id, data_x, data_y)  # 代表凝视点移动的初始位置，图形用id表示
            pos = self.canvas.coords(self.id)  # 获取凝视点图形的左上和右下角坐标值
            gaze_point_flag =0
            if pos[0] <= 0:  # 如果左上角水平分量x，即球拍左边已经到达左边框
                self.x = 0  # 球拍不像小球一样需要自动回弹，所以设置水平分量x为0,即让它停止运动
            elif pos[2] >= self.canvas_width:  # 如果右下角水平分量x，即球拍右边已经到达右边框
                self.x = 0  # 同样设置为0，停止运动

# 创建ball类
class Ball:
    def __init__(self, canvas, color):  # 初始化函数，包含画布canvas和颜色color参数
        global ball_id
        rectangle_x1 = (window_width*0.02)
        rectangle_y1 = (window_height*0.2)
        rectangle_x2 = (window_width*0.78)
        rectangle_y2 = (window_height*0.78)
        self.canvas = canvas  # 把参数canvas赋值给对象变量canvas
        self.id = canvas.create_rectangle(rectangle_x1, rectangle_y1, rectangle_x2, rectangle_y2, dash=(4, 4))#在画布边缘画虚线
        #print("画布虚线id：%d" % self.id) # 1
        oval_x1 = -40
        oval_y1 = 250#(window_height * 0.22)
        oval_x2 = oval_x1+80
        oval_y2 = oval_y1+80
        self.ball_id = canvas.create_oval(oval_x1, oval_y1, oval_x2, oval_y2, fill=color)  # 创建椭圆，左上角和右下角xy坐标，返回代表图形的ID
        #print("圆球id：%d" % self.ball_id) # 2
        self.canvas.move(self.ball_id, oval_x1, oval_y1)  # 把画好的椭圆形移动的画布中心，图形用id表示
        #print("任务id号：%d"%self.id)

        self.x = 1  # 对象变量x就是水平移动的初始值，等价于不动，在下面画图函数中调用
        self.y = 0  # 对象变量y就是垂直移动的初始值，等价于向上移动，在下面画图函数中调用
        self.canvas_height = self.canvas.winfo_height()  # 获取画布的高度，画布上高度是从上到下测量的

    def draw(self):  # 定义画图动作
        global start_flag,ballRun_flag,ball_id
        if(start_flag == 0):
            self.canvas.move(self.ball_id,0,0)#停止，0,1 下移动
            ballRun_flag = 1
        if(start_flag == 1):
            self.canvas.move(self.ball_id, self.x, self.y)  # 按照x和y定义的步长来移动小球
            # pos = self.canvas.coords(self.id)  # coords函数通过id返回画布上画好东西的xy坐标值
            # if pos[2] <= 0:  # pos返回一个列表[x1,y1,x2,y2]，分别代表椭圆左上角和右下角的xy坐标
            #     self.x = -1  # 当球右下角x2坐标小于等于0，说明碰到画布右，重新设置对象变量x为-1，开始垂直向左移动
            # if pos[0] >= self.canvas_height:  # 当球右下角y2坐标超过画布高度，重新设置对象变量y为-1，开始垂直向上移动
            #     self.y = -1
            ballRun_flag = 0

def Start_AutoMove():
    global start_flag,ballRun_flag,gaze_start_print,start_button_flag,data_StartRecrive
    if (ballRun_flag == 1):
        data_StartRecrive = True
        start_flag = 1
        gaze_start_print = 1
    if(ballRun_flag == 0):
        data_StartRecrive = False
        start_flag = 0
        gaze_start_print = 0
        start_button_flag = True
    # print("凝视点X坐标长度：%d"%len(gaze_point_listX))
    # print("凝视点Y坐标长度：%d" % len(gaze_point_listY))
    # print("凝视点存放数据为：")
    # print(gaze_point_listX)
    # print(gaze_point_listY)
    #gaze_point_listX.clear()
    #gaze_point_listY.clear()

def NoRectangle_AutoMove():
    global start_flag,ballRun_flag,gaze_start_print,NoRectangle_button_flag,data_StartRecrive
    gaze_start_print = 0
    if (ballRun_flag == 1):
        data_StartRecrive = True
        start_flag = 1
    if(ballRun_flag == 0):
        data_StartRecrive = False
        start_flag = 0
        NoRectangle_button_flag = True
    if (start_button_flag == True):#删除所有存在的凝视点图形，放止点完Start后点击测试按钮
        for i in range(0, len(gaze_pictureID_list)):
            canvas.delete(gaze_pictureID_list[i])
        gaze_pictureID_list.clear()

def Circle_AutoRestart():
    global start_flag, ballRun_flag,gaze_pictureID_list,gaze_start_print,gaze_point_listX,gaze_point_listY
    #####复位后停止移动
    start_flag = 0
    gaze_start_print = 0
    ball_place = canvas.coords(2)
    place_move = ball_place[0]
    canvas.move(2,-place_move-80,0)
    for i in range(0,len(gaze_pictureID_list)):#删除所有存在的凝视点图形
        canvas.delete(gaze_pictureID_list[i])
    gaze_pictureID_list.clear()
    gaze_point_listX.clear()
    gaze_point_listY.clear()

def DataAnalysis():
    global gaze_point_listX,gaze_point_listY,start_button_flag,NoRectangle_button_flag,gaze_pictureID_list,GazePoint_Alldistance,DataAnalysis_count,Data_text_id
    if(DataAnalysis_count == 0):
        canvas.create_text(0, 50, text='凝视点分析：', font=('微软雅黑', 20, 'bold'), anchor=W, justify=LEFT)
        Data_text_id = canvas.create_text(40, 80, text='凝视点总的间差和为：', font=('微软雅黑', 14, 'bold'), anchor=W, justify=LEFT)
        DataAnalysis_count=DataAnalysis_count+1
    if(start_button_flag == True):
        ball_place = canvas.coords(2)
        place_move = ball_place[0]
        canvas.move(2, -place_move, 0)
        start_button_flag = False
        print("测试按钮点击有效。")
        for i in range(0, (len(gaze_point_listX)) - 1):
            GazePoint_1 = Point(gaze_point_listX[i], gaze_point_listY[i])
            GazePoint_2 = Point(gaze_point_listX[i + 1], gaze_point_listY[i + 1])
            GazePoint_line = Getlen(GazePoint_1, GazePoint_2)
            # 获取两点之间直线的长度
            GazePoint_distance = GazePoint_line.getlen()
            GazePoint_Alldistance = GazePoint_distance + GazePoint_Alldistance
            print(GazePoint_distance)
        print("总间差为：%d" % GazePoint_Alldistance)

    if(NoRectangle_button_flag == True):
        for i in range(0,len(gaze_point_listX)):
            id = canvas.create_rectangle(0, 0, 5, 5, fill="green")
            gaze_pictureID_list.append(id)
            canvas.move(id, gaze_point_listX[i], gaze_point_listY[i])
        ball_place = canvas.coords(2)
        place_move = ball_place[0]
        canvas.move(2, -place_move, 0)
        NoRectangle_button_flag = False
        print("无图形测试点击有效")
        for i in range (0,(len(gaze_point_listX))-1):
            GazePoint_1 = Point(gaze_point_listX[i],gaze_point_listY[i])
            GazePoint_2 = Point(gaze_point_listX[i+1],gaze_point_listY[i+1])
            GazePoint_line = Getlen(GazePoint_1, GazePoint_2)
            # 获取两点之间直线的长度
            GazePoint_distance = GazePoint_line.getlen() * 0.265 #转化为mm单位
            GazePoint_Alldistance = GazePoint_distance + GazePoint_Alldistance
            print(GazePoint_distance)
        print("总间差为：%d"%GazePoint_Alldistance)
    GazePoint_Alldistance_str = '凝视点总的间差和为：' + str(format(GazePoint_Alldistance, '.1f')) + 'mm'
    canvas.itemconfig(Data_text_id, text = GazePoint_Alldistance_str)
    #canvas.insert(Data_text_id, 12, "new ")#在文字中间插入？？
    GazePoint_Alldistance = 0
    gaze_point_listX.clear()
    gaze_point_listY.clear()

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        #sleep(0.003)
    return data

def code_close():
    global run
    run = False

# 创建游戏的桌布
EyeMove_window = Tk()  # 用Tk（）类创建一个tk对象，它就是一个基本窗口，可以在其上增加其他东西
EyeMove_window.title("眼动轨迹")  # 给Tk对象窗口加一个标题
#EyeMove_window.resizable(0, 0)  # tk窗口大小不可调整
EyeMove_window.wm_attributes("-topmost", 1)  # 告诉tkinter把窗口放到最前面

window_width = EyeMove_window.winfo_screenwidth()
window_height = EyeMove_window.winfo_screenheight()
EyeMove_window.geometry("%dx%d"%(window_width,window_height))#这里%dx%d不能写成%d*%d，会报错
print("当前屏幕的宽度为：%dpx"%(EyeMove_window.winfo_screenwidth()))
print("当前屏幕的长度为：%dpx"%EyeMove_window.winfo_screenheight())
canvas = Canvas(EyeMove_window,width=(window_width*0.8), heigh=(window_height*0.8), bd=0, highlightthickness=0)
                                                            # 设置画布（即滑块可显示的范围，
                                                            # .geometry范围更大的话，超出此设置范围被吃掉）
canvas.pack()  # 按照上面一行指定的宽度高度参数调整其自身大小

EyeMove_window.update()

# 画一个蓝色的球
ball = Ball(canvas, 'blue')  # 用Ball类在画布上画一个蓝色的球
gaze_point = Eyes_gaze_point(canvas, 'red')

start_button = Button(EyeMove_window, width=20,height=2,text='开始',bg = 'black',fg = 'white',command=Start_AutoMove)#设置按钮属性，text表示按钮文本，bg、fg分别表示文本和背景颜色
 #start_button.grid(row=2,column=1) #放置按钮
start_button.pack(fill = Y,side = LEFT)
NoRectangle_button = Button(EyeMove_window, width=20,height=2,text='测试',bg = 'green',fg = 'white',command=NoRectangle_AutoMove)#设置按钮属性，text表示按钮文本，bg、fg分别表示文本和背景颜色
 #start_button.grid(row=2,column=1) #放置按钮
NoRectangle_button.pack(fill = Y,side = LEFT)
restart_button = Button(EyeMove_window, width=20,height=2,text='复位',bg = 'red',fg = 'white',command=Circle_AutoRestart)#设置按钮属性，text表示按钮文本，bg、fg分别表示文本和背景颜色
 #start_button.grid(row=2,column=1) #放置按钮
restart_button.pack(fill = Y,side = RIGHT)
DataAnalysis_button = Button(EyeMove_window, width=20,height=2,text='分析',bg = 'blue',fg = 'white',command=DataAnalysis)#设置按钮属性，text表示按钮文本，bg、fg分别表示文本和背景颜色
 #start_button.grid(row=2,column=1) #放置按钮
DataAnalysis_button.pack(fill = Y,side = RIGHT)

EyeMove_window.protocol("WM_DELETE_WINDOW", code_close)  #解决窗口关闭时报错：“.!canvas”
                                                        #由窗口右上角的关闭按钮引起的，这是您必须停止脚本的唯一方法。
# 单击关闭按钮后，窗口被破坏，因此不存在画布之类的小部件。您可以设置一个标志来标识while循环是否应该在窗口关闭按钮事件的处理程序中停止并退出。
run = True

serial = serial.Serial('COM3', 9600, timeout=0.5)  # 打开COM并设置波特率为115200，COM1只适用于Windows
# ser.timeout＝0.5  # 读超时设置
# ser.writeTimeout＝0.5  # 写超时
if serial.isOpen():
    print("open success")
else:
    print("open failed")

# 主循环，让tkinter不停地重画屏幕
while run:
    if(Calibration_complete == False):
        Calibration_value = os.system('c: && cd \Program Files (x86)\Tobii\Tobii Configuration && Tobii.Configuration.exe -Q')  # 加&&可执行多条语句
        if(Calibration_value == 0):
            Calibration_complete = True
    if(data_StartRecrive == True):
        data = recv(serial)
        if data != b'':
            if len(data) == 8:
                gaze_point_flag = 1
                dat_x = data[2] * 256
                dat_x = (dat_x + data[3])
                dat_y = data[4] * 256
                dat_y = (dat_y + data[5])
                if(192<=dat_x<=1728 and 0 <= dat_y <= 864):
                    data_x = dat_x-192
                    #print(data_x)
                    data_y = dat_y
                    # print(data_y)
                    gaze_point_listX.append(data_x)
                    gaze_point_listY.append(data_y)
                #print("数据传输成功")

    ball.draw()  # 调用Ball类的作画函数
    gaze_point.draw(data_x,data_y)
    EyeMove_window.update_idletasks()#可有可无，不知道这个干吗的；只有这个程序无法运行会死机
    EyeMove_window.update()
        #update（）可以接收用户改变程序进程；
        #update_idletasks（）不能接收用户改变程序进程
        #但他们都可以实现标签刷新。
    time.sleep(0.005)

EyeMove_window.destroy()
