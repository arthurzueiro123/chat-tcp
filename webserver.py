import socket
from threading import Thread


class WebServer:

    def __init__(self, address='0.0.0.0', port=80):
        self.port = port
        self.address = address
        
        self.users =[]
        self.online =[]


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.address, self.port))
            s.listen(10)

            while True:
                print('Aguardando conexoes...')
                conn, addr = s.accept()
                req = Request(conn, addr,self)
                req.start()

    
#class HandleConnection:



class Request(Thread):

    def __init__(self, conn, addr, websock):
        super(Request, self).__init__()
        self.conn = conn
        self.addr = addr
        self.websock = websock
        self.CRLF = '\r\n'
        self.buffer_size = 4096

    def run(self):
        request = self.conn.recv(self.buffer_size)
        print(request.decode())
        decodereq = request.decode()
        #decodificar esse request
        #teste = 'Sec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document'
        
        header = decodereq.split("\r\n")
        method = header[0].strip()
        msgctd = header[-1]

        header = header[1:len(header)-2]
        print(header)

        dictionary = {} 
        for testando in  header:
            print(testando.split(":"))
            res = testando.split(":")
            aux = res[1]
            if len(res)>2:#cao tenha mai de 1 : na linha
                aux = res[1]+" "+res[2]
                
            dictionary[res[0]] = aux

        print(dictionary)
        
        #dictionary = dict(subString.split(":") for subString in teste.split("\r\n")) 
        #dictionary = dict(subString.split(":") for subString in  headerNprocess) 
        #for subString in headerNprocess:
        # key=[]
        # values=[]
        # dictionary = {} 
        # for i in range(0,len(headerNprocess)): 
        #     aux = headerNprocess[i].split(":")
        #     key[i] = aux[0]
        #     print(aux[0])
        #     values[i]= " ".join(aux[1:-1])
        #     dictionary[keys[i]] = values[i]
        #     print(dictionary)

        #x = " ".join(myTuple)
        print(method)
        print(dictionary) 
        print(dictionary['usuario']) 
        for u in self.websock.users:
            print(u)

        #method = method[0]
        if method == 'create':
            jaExist = False
            for u in self.websock.users:
                if dictionary['usuario'] == u.usuario:
                    #retorna usuario ja existente
                    print('usuario ja existe')
                    jaExist = True
                    response = Response(self.conn, self.addr, 'status:1')
                    response.processRespose()
                    # self.conn.close()
            if jaExist == False:
                print("adicionando")
                print(self.websock.users)
                self.websock.users.append(User(self.conn, self.addr, dictionary['usuario'] , dictionary['senha']))
                print(self.websock.users)
                response = Response(self.conn, self.addr, 'status:0')
                response.processRespose()    
                
        if method == 'login':
            login = False
            for k in self.websock.users:
                if dictionary['usuario'] == k.usuario:
                    if dictionary['senha'] == k.senha:
                        login =True

            if login == True:
                response = Response(self.conn, self.addr, 'status:0')
                #adicional a uma lista de online
                self.websock.online.append(User(self.conn, self.addr, dictionary['usuario'] , dictionary['senha']))
            else:
                response = Response(self.conn, self.addr, 'status:5')
                print("usuario ou senha incorretos")
            response.processRespose()
            #self.conn.close()

        if method == 'logout':
            print("logout: encerando conexao")
            response = Response(self.conn, self.addr, 'status:0')
            response.processRespose()
            #self.websock.online.remove()
            self.conn.close()
        
        if method == 'msg':
            response2 = Response(self.conn, self.addr, 'status:2')
            #(response2)retorno para o usuario que iniciou a requisição
            if dictionary['destiny'] == "all":
                for u in self.websock.online:
                    if not u.usuario == dictionary['usuario']:#se for diferente do usuario que enviou inicialmente a mensagem
                        response = Response(u.conn, u.addr, msgctd)
                        response2 = Response(self.conn, self.addr, 'status:0')
                        response.processRespose()#para enviar para cada usuario online tem que ser enviado essa resposta para todos os outros usuarios
                        
            else:
                for u in self.websock.users:
                    if u.usuario == dictionary['destiny']:
                        response = Response(u.conn, u.addr, msgctd)
                        response2 = Response(self.conn, self.addr, 'status:0')
                        response.processRespose()
                    else:
                        print("usuario nao encontrado")
                        response2 = Response(self.conn, self.addr, 'status:2')
            
            
            response2.processRespose()
            # self.conn.close()

        # self.conn.close()
            
        # logout
        # self.conn.close()

        #ultimo campo file tera valor quando eu quser retornar algo
        # response = Response(self.conn, self.addr, '')
        # response.processRespose()
        # self.conn.close()


class Response:

    def __init__(self, conn, addr, msg):
        self.conn = conn
        self.addr = addr
        self.msg = msg.encode('utf-8')

    def processRespose(self):
        #if self.me


        aux = self.msg
        self.conn.sendall(aux)

class User:
    def __init__(self, conn, addr, usuario, senha):
        super(User, self).__init__()
        self.conn = conn
        self.addr = addr
        self.usuario = usuario
        self.senha = senha


#    request = self.conn.recv(self.buffer_size)
#         print(request.decode())
#         decodereq = request.decode()
#         #decodificar esse request
#         #teste = 'Sec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document'
#         headerNprocess = decodereq.split("\r\n")
#         if headerNprocess[0] !='':#se a requsição nao vinher vazia
#             print("primeira linha:"+headerNprocess[0])
#             firstLine = headerNprocess[0].split(' ')
#             print(firstLine)

#             method = firstLine[0]
#             url = firstLine[1]
#             version = firstLine[2]
#             body=''
#             content='text/html'
#             status = '200 OK'
#             if method =="GET":
#                 headerNprocess = headerNprocess[1:-1]
#                 fimHeaderPos = len(headerNprocess)
#                 for i in range(0,len(headerNprocess)) :
#                     if headerNprocess[i] == '':
#                         fimHeaderPos =i
#                         print("encontradovazio:"+str(i))

#                 headerNprocess = headerNprocess[0:fimHeaderPos]

#                 dictionary = {} 
#                 for testando in  headerNprocess:
#                     print(testando.split(":"))
#                     res = testando.split(":")
#                     aux = res[1]
#                     if len(res)>2:#cao tenha mai de 1 : na linha
#                         aux = res[1]+":"+res[2]
                        
#                     dictionary[res[0]] = aux

#                 print(dictionary)