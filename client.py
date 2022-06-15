import socket

HOST = '127.0.0.1'
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
#s.sendall(str.encode('create\r\nusuario:c\r\nsenha:exemplo\r\ndestiny:all\r\nmsgsz:1291\r\n\r\najakjdkajdkajd....'))
#s.sendall(str.encode('login\r\nusuario:c\r\nsenha:exemplo\r\ndestiny:all\r\nmsgsz:1291\r\n\r\najakjdkajdkajd....'))
# while True:
#         data = s.recv(1024)
#         print(data.decode('utf-8'))
s.sendall(str.encode('msg\r\nusuario:a\r\nsenha:exemplo\r\ndestiny:all\r\nmsgsz:1291\r\n\r\najakjdkajdkajd....'))

            #s.sendall(str.encode('login\r\nusuario:jorel\r\nsenha:1234\r\ndestiny:all\r\nmsgsz:1291\r\n\r\najakjdkajdkajd....'))
#s.sendall(str.encode('logout\r\nusuario:jorel\r\nsenha:1234\r\ndestiny:all\r\nmsgsz:1291\r\n\r\najakjdkajdkajd....'))

#def receiveMsg():
    

