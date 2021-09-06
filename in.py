import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",1234))
f = open('test.xml','r')
data = f.read()
s.send(data.encode("utf-8"))