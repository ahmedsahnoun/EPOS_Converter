import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("127.0.0.1",1235))
s.listen()
while True:
   clientScoket, address = s.accept()
   data = clientScoket.recv(1024).decode("utf-8")
   print(data)