"""
此文件主要是元组传参的用法


"""

import multiprocessing as mp
from time import sleep

a = 10

def worker(sec):
    print(a)
    sleep(sec)
    print('worker ......')
    print(a)


if __name__ == '__main__':    #虽然加上了这句话但只是用于Windows环境，并不是非要在main文件中才能运行
    p = mp.Process(name='child', target=worker, args=(5,))  # 元组传参,args（5，）将5作为参数传入worker中执行,这里传入的是单个参数

    # p进程对象的属性
    # p.daemon = True
    p.start()  # 启动进程
    print(p.pid)  # 创建的子进程的ＰＩＤ号
    print(p.name)  # 创建的进程的名称
    print(p.is_alive())  # 进程的状态
    a = 100000
    p.join()  # 主进程阻塞等待子进程的退出
    print("************main****************")
    worker(1)