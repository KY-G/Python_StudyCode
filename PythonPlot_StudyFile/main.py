import cv2
import numpy as np
import matplotlib.pyplot as plt


def PlotDemo1():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400], [0, 0.2, 0.68, 1.16, 1.44, 1.52, 1.44, 1.16, 0.8, 0.28, -0.2, -0.68, -1.04, -1.2, -1.24, -1.16, -0.88, -0.4, -0.2, -0.08, 0])
    plt.show()


# 定义x、y散点坐标
x = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
x = np.array(x)
print('x is :\n', x)
num = [0, 0.2, 0.68, 1.16, 1.44, 1.52, 1.44, 1.16, 0.8, 0.28, -0.2, -0.68, -1.04, -1.2, -1.24, -1.16, -0.88, -0.4, -0.2, -0.08, 0]
y = np.array(num)
print('y is :\n', y)
# 用3次多项式拟合
f1 = np.polyfit(x, y, 3)
print('f1 is :\n', f1)

p1 = np.poly1d(f1)
print('p1 is :\n', p1)

#也可使用yvals=np.polyval(f1, x)
yvals = p1(x)  #拟合y值
print('yvals is :\n', yvals)
#绘图
plot1 = plt.plot(x, y, 's', label='original values')
plot2 = plt.plot(x, yvals, 'r', label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=4) #指定legend的位置右下角
plt.title('polyfitting')
plt.show()


#PlotDemo1()
cv2.destroyAllWindows()
