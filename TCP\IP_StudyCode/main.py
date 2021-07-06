import socket
#客户端 Client
#USB转网口的地址及接口：'192.180.1.78', 8345
HOST = '192.180.1.78'
PORT = 8345
BUFSIZ = 1024
ADDR = (HOST,PORT)
sk = socket.socket()
sk.connect(ADDR)   #连接到ADDR处的套接字
print(sk.recv(BUFSIZ))
while True:
    inp = input(">>>")
    if not inp:                                      #忽略空格回车
        continue
    sk.send(bytes(inp,"utf-8"))
    print(sk.recv(BUFSIZ))