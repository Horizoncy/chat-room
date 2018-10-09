import socket
import threading
#创建本地5550端口
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('localhost',5550) )
#监听端口
sock.listen(5)
print('Sever',socket.gethostbyname('localhost'),'listening...')
mydict=dict()
mylist=list()
#把saywhat传给了除了exceptnum的所有人
def tellothers(exceptnum,saywhat):
    for c in mylist :
        try:
            c.send(saywhat.encode())
        except:
            pass
#插入一个聊天线程(进入聊天室等步骤)
def subthreadin(myconnection,connumber):
    nickname=myconnection.recv(1024).decode()#昵称
    mydict[myconnection.fileno()]=nickname
    mylist.append(myconnection)
    print('connection',connumber,' has nickname:',nickname)
    tellothers(connumber,'系统提示:'+mydict[connumber]+'进入聊天室')
#判断是否仍然连接
    while True :
        try:
            recievedmsg=myconnection.recv(1024).decode()
            if recievedmsg:
                print(mydict[connumber]+' :'+recievedmsg)
        except(OSError,ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connumber],'exit, ',len(mylist),' person left')
            tellothers(connumber,'系统提示: '+mydict[connumber]+' 离开聊天室')
            myconnection.close()
            return 
while True:
    connection, addr=sock.accept()
    print('Accept a new connection',connection.getsockname(),connection.fileno())
    try:
        msg=connection.recv(1024).decode()
        if msg=='1':
            connection.send(b'welcome to sever!')
#为当前连接开辟一个新的线程
            mythread=threading.Thread(target=subthreadin,args=(connection,connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()
        else:
            connection.send(b'please go out')
            connection.close()
    except:
        pass
