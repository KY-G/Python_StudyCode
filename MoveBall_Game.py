# 引入下列模块
from tkinter import *  # 画图模块
import random  # 随机数模块
import time  # 时间模块


# 创建ball类
class Ball:
    def __init__(self, canvas, paddle, color):  # 初始化函数，包含画布canvas和颜色color参数，并把paddle对象作为参数传给球
        self.canvas = canvas  # 把参数canvas赋值给对象变量canvas
        self.paddle = paddle  # 把球拍paddle参数赋值给对象变量paddle，引入球拍后就能在小球的类内定义击中球拍的函数
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)  # 创建椭圆，左上角和右下角xy坐标，返回代表图形的id
        self.canvas.move(self.id, 245, 100)  # 把椭圆形（球）移动的画布中心，图形用id表示
        starts = [-3, -2, -1, 1, 2, 3]  # 给一串x分量的起始值（x和y代表横坐标和纵坐标的分量）
        random.shuffle(starts)  # 随机混排序，赋值给对象变量x，让它起始的时候获得随机分量值，引起球每次起始角度都不同
        self.x = starts[0]  # 对象变量x就是水平分量移动的初始值，等价于左右移动，值代表移动多少像素点
        self.y = -3  # 对象变量y就是垂直分量移动的初始值，等价于上下移动，值代表移动多少像素点
        self.canvas_height = self.canvas.winfo_height()  # 获取画布的高度，画布高度是从上到下计量的
        self.canvas_width = self.canvas.winfo_width()  # 获取画布的宽度
        self.hit_bottom = False  # 定义一个游戏结束的因素：碰到底部，设置碰到底部变量初值为假

    def hit_paddle(self, pos):  # 定义击中球拍函数，传入小球位置pos坐标参数，用于和球拍位置坐标值作比较判断是否击中
        paddle_pos = self.canvas.coords(self.paddle.id)  # 由于在初始化函数中已经引入了paddle参数，就能够用球拍的id值来返回球拍的pos坐标值
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:  # 如果小球的右下角x2大于等于球拍左边框x1，并且小球左上角x1小于等于球拍右边框x2，说明碰到
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:  # 如果小球最底部在球拍顶边和底边之间（因为我们每次移动小球垂直分量的步长为3，可能会出现
                return True  # 已经超过球拍顶边一点点的情况，如果只是判断是否碰到顶边，球在这种情况下就只能继续飞过球拍了）
        return False  # 满足上述两种情况，返回真，即碰到球拍。如果不满足，返回假，即没碰到球拍

    def draw(self):  # 定义小球的画图动作
        self.canvas.move(self.id, self.x, self.y)  # 按照x和y定义的像素值来移动小球，比如3就是移动3个像素点位置
        pos = self.canvas.coords(self.id)  # coords函数通过id返回画布球的坐标列表，pos[x1,y1,x2,y2]，分别代表椭圆左上右下角的xy坐标
        if pos[1] <= 0:  # 当球左上角y1坐标小于等于0，即碰到画布顶部
            self.y = 3  # 重新设置对象变量y为3，开始垂直分量向下移动
        if pos[3] >= self.canvas_height:  # 当球右下角y2坐标超过画布高度（底部）
            self.hit_bottom = True  # 设置击中底部变量为真（刚开始定义对象变量y为-3，向上移动，但现在不让它动了，表示游戏结束）
        if self.hit_paddle(pos) == True:  # 当击中球拍函数为真时（pos反映了小球击中球拍时的位置坐标）
            self.y = -3  # 重新设置对象变量y为-3，开始垂直分量向上移动
        if pos[0] <= 0:  # 当球左上角x1坐标小于等于0，即碰到画布左边框
            self.x = 3  # 重新设置对象变量x为3，开始水平分量向右移动
        if pos[2] >= self.canvas_width:  # 当球右下角x2坐标超过画布有边框
            self.x = -3  # 重新设置对象变量x为-3，开始水平分量向左移动


# 创建Paddle类
class Paddle:
    def __init__(self, canvas, color):  # 初始化函数，包含画布canvas和颜色color参数
        self.canvas = canvas  # 把参数canvas赋值给对象变量canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)  # 创建长方形，左上角和右下角xy坐标，返回代表图形的id
        self.canvas.move(self.id, 200, 300)  # 把长方形（球拍）移动的初始位置，图形用id表示
        self.x = 0  # 设置对象变量x，初始值为0.也就是图形先不移动
        self.canvas_width = self.canvas.winfo_width()  # 获取画布的宽度
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)  # 初始化时将事件‘按下左键’和函数向左移动绑定
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)  # 初始化时将事件‘按下右键’和函数向右移动绑定

    def turn_left(self, evt):  # 定义使球拍向左移动的函数
        self.x = -4  # 每次向左移动4个像素，在画布上越来越向左，值越来越小，所以需要负数

    def turn_right(self, evt):  # 定义使球拍向右移动的函数
        self.x = 4  # 每次向右移动4个像素，在画布上越来越向右，值越来越大，所以需要正数

    def draw(self):  # 定义球拍的画图动作
        self.canvas.move(self.id, self.x, 0)  # 和小球配置大致相同，画图移动只在水平左右移动，所以y分量设置为0
        pos = self.canvas.coords(self.id)  # 获取球拍的左上和右下角坐标值
        if pos[0] <= 0:  # 如果左上角水平分量x，即球拍左边已经到达左边框
            self.x = 0  # 球拍不像小球一样需要自动回弹，所以设置水平分量x为0,即让它停止运动
        elif pos[2] >= self.canvas_width:  # 如果右下角水平分量x，即球拍右边已经到达右边框
            self.x = 0  # 同样设置为0，停止运动

def code_close():
    global run
    run = False

# 创建游戏窗口和画布
tk = Tk()  # 用Tk（）类创建一个tk对象，它就是一个基本窗口，可以在其上增加其他东西
tk.title("Game")  # 给Tk对象窗口加一个标题
tk.resizable(0, 0)  # tk窗口大小不可调整
tk.wm_attributes("-topmost", 1)  # 告诉tkinter把窗口放到最前面
canvas = Canvas(tk, width=500, heigh=400, bd=0, highlightthickness=0)  # Canvas是一个画布类
canvas.pack()  # 按照上面一行指定的宽度高度参数调整其自身大小
tk.update()  # update强制更新屏幕，即重画

# 创建球拍和小球对象
paddle = Paddle(canvas, 'blue')  # 用Paddle类创建蓝色球拍对象，球拍对象一定要优先创建，否则小球引用球拍参数时会报错
ball = Ball(canvas, paddle, 'red')  # 用Ball类创建画红色小球对象，并将球拍作为参数引入，用来在小球函数中判断是否击中球拍

tk.protocol("WM_DELETE_WINDOW", code_close)  # 解决窗口关闭时报错：“.!canvas”
    # 由窗口右上角的关闭按钮引起的，这是您必须停止脚本的唯一方法。
    # 单击关闭按钮后，窗口被破坏，因此不存在画布之类的小部件。您可以设置一个标志来标识while循环是否应该在窗口关闭按钮事件的处理程序中停止并退出。
run = True

# 主循环，让tkinter不停地重画屏幕
while run:
    if ball.hit_bottom == False:  # 如果碰到底部变量为假的时候
        ball.draw()  # 调用Ball类的作画函数
        paddle.draw()  # 调用Paddle类的作画函数
    tk.update_idletasks()  # updata_idletasks和updata这两个命令
    tk.update()  # 让tkinter快一点把画布上的东西画出来
    time.sleep(0.01)  # 延时让动画效果慢一点

tk.destroy()


