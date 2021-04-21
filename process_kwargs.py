"""
主要展示字典传参，kwargs
这样运行会上来就输出的5个a的值不太懂，kwargs注意{}。
开始时输出连续打印出100是由于子进程中sleep()所致，
当去掉时，连续执行数次（>3）时100均非连续；同时子进程PID号也是乱序（此也说明子进程相互独立）。
"""

import multiprocessing as mp
from time import sleep
import os

a = 100

def worker(sec,msg):
    print(a)
    sleep(sec) #保护性阻塞休眠？？程序先输出了5个a的值，又接着输出了后面的值。程序连续运行五次到第一句处，休眠结束再运行五遍后面的语句
    print(os.getppid(), '-------', os.getpid())
    print(msg)
    print(a)

if __name__ == '__main__':
    for i in range(5):
        p = mp.Process\
            (name='Child%d' % i, target=worker,
              #      args = (2,"child process"))
             kwargs={'sec': 2, 'msg': "child process"})  #这种传参方式跟args有啥区别？？好像都一样
        p.start()#这里创建了几个进程呢？？

    sleep(1)
    a = 100000
    print(a+1)

    p.join()
    print("************main****************")
    worker(1, "father process")