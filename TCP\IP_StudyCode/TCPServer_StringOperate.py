# coding:UTF-8
import multiprocessing
import socket
import os
from multiprocessing import Queue
#import imutils
#服务端Server
def VideoPlay_Function(Queue_VideoPlayer):
    Start_VideoPlay = False
    while(True):
        VideoPlayer_isEmpty = Queue_VideoPlayer.empty()
        if VideoPlayer_isEmpty == False:
            Start_VideoPlay = Queue_VideoPlayer.get()
        if(Start_VideoPlay == True):
            Video_value = os.system(
                'd:\PotPlayer\PotPlayerMini64.exe e:\MyFile\Test_File\TestVideo.mp4')  # 加&&可执行多条语句#TestVideo.mp4
            if(Video_value == True):
                print("接收到视频播放指令。")
            Start_VideoPlay = False

if __name__ == '__main__':
    print("主进程开始启动！")
    Video_Player = False
    sk = socket.socket()
    # print(sk)
    # 串口转网口的地址及接口：'192.180.1.78', 8345 ;串口转网口做客户端
    HOST = '192.180.1.221'
    PORT = 8234  # 8345
    BUFSIZ = 1024

    print("创建一个子进程")
    Queue_VideoPlayer = multiprocessing.Queue()
    p = multiprocessing.Process(target=VideoPlay_Function, args=(Queue_VideoPlayer,))
    p.start()

    ADDR = (HOST, PORT)

    sk.bind(ADDR)  # 绑定到一个地址连接  ADDR地址的格式取决于地址族。在AF_INET下，以元组（host，port）的形式表示地址
    sk.listen(5)  # 开始监听传入连接。传入参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量（？？？什么东东）。该值至少为1，大部分应用程序设为5就可以了。
    print("waiting...")
    while True:
        conn, addr = sk.accept()  # 服务器端用。接受连接并返回（conn，address），
        # 其中conn是新的套接字对象(客户端连接过来就生成一个实例），可以用来接收和发送数据。
        # address是连接客户端的地址。
        ip, port = addr
        print("Got connection from", addr)
        conn.send(bytes("connected from %s:%s." % addr, "utf-8"))
        while True:
            data = conn.recv(BUFSIZ)  # 指定要接收的最大数据量
            if not data:
                break  # 直接回车退出本次连接
            print(data)
            if (data == b'StartPlay\r\n'):
                Video_Player = True
                Queue_VideoPlayer.put(Video_Player)
                Video_Player = False
            elif (data == b'ReSend\r\n'):
                Video_value = os.system('taskkill /im PotPlayerMini64.exe')

            conn.send(data)

    conn.close()  # 关闭连接。
    print('主进程结束！')




