"""
主要讲解Queue的使用
Queue是多进程安全的队列，可以使用Queue实现多进程之间的数据传递。
put方法用以插入数据到队列中，put方法还有两个可选参数：blocked和timeout。
如果blocked为True（默认值），并且timeout为正值，该方法会阻塞timeout指定的时间，直到该队列有剩余的空间。
                        如果超时，会抛出Queue.Full异常。
如果blocked为False，但该Queue已满，会立即抛出Queue.Full异常。

get方法可以从队列读取并且删除一个元素。同样，get方法有两个可选参数：blocked和timeout。
如果blocked为True（默认值），并且timeout为正值，那么在等待时间内没有取到任何元素，会抛出Queue.Empty异常。
如果blocked为False，有两种情况存在，如果Queue有一个值可用，则立即返回该值，
                                否则，如果队列为空，则立即抛出Queue.Empty异常。

"""

import multiprocessing
import time


def writer_proc(q):
    try:
        a=0
        #q.put(1, block = False)
        #q.put("Data Writer Successed")
        while True:
            a=a+3
            q.put(a)
            time.sleep(1)
    except:
        pass

def reader_proc(q):
    try:
        while True:
            if(q.empty() != True):
                print(q.get())
                time.sleep(0.01)
            if(q.empty() == True):
                print("yunxing ")
                time.sleep(0.2)

    except:
        pass

if __name__ == "__main__":
    q = multiprocessing.Queue()
    writer = multiprocessing.Process(target=writer_proc, args=(q,))
    writer.start()

    reader = multiprocessing.Process(target=reader_proc, args=(q,))
    reader.start()

    reader.join()
    writer.join()

"""
本部分程序主要关于队列的出队与入队
"""
"""
from queue import Queue

if __name__ == "__main__":

    kq = Queue(10)   #定义一个大小为10的队列

    for i in range(1,20):
        if kq.full():	#如果队列满了get()会把对头的data出队，先进先出
            cc = kq.get()
            print("out", cc)
        kq.put(i, block=False)	#非阻塞方式入队
        print("put[%d]---" % i, i)

    i = 0
    while not kq.empty():	#以此将队列出队
        print("get[%d]---" % i, kq.get())
        i += 1
"""