import socket
import time
import threading
#连接sever端
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('localhost',5550))
sock.send(b'1')
#输入昵称
print(sock.recv(1024).decode())
nickname=input('input your nickname: ')
sock.send(nickname.encode())
#线程语言文字发送
def sendthreadfun():
    while True:
        try:
            myword=input()
            sock.send(myword.encode())
        except ConnectionAbortedError:
            print('sever closed this connection!')
#接受sever端数据
def recievethreadfun():
    while True:
        try:
            personword=sock.recv(1024)
            if personword:
                print(personword.decode())
            else :
                pass
        except ConnectionResetError:
            print('sever is closed')
#开启两个一个接受一个发送线程
thread1=threading.Thread(target=sendthreadfun)
thread2=threading.Thread(target=recievethreadfun)
threads=[thread1,thread2]

for th in threads:
    th.setDaemon(True)
    th.start()
th.join()

             

