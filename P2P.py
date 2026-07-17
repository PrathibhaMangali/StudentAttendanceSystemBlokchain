import socket 
from threading import Thread 
from socketserver import ThreadingMixIn
import socket
import pickle

running = True

def startP2P1():
    class Server1(Thread): 
 
        def __init__(self,ip,port): 
            Thread.__init__(self) 
            self.ip = ip 
            self.port = port
            print('Request received from Peer IP : '+ip+' with port no : '+str(port)+"\n")        
         
        def run(self):
            data = conn.recv(10000)
            data = pickle.loads(data)
            request_type = data[0]
            if request_type == "save":#cloud receive request to save encrypted data
                sid = data[1]
                dd = data[2]
                cname = data[3]
                conn.send("P2P 1 Data Received".encode())
                print("P2P 1: Student Attendance Received for ID = "+sid+" Time = "+dd)                              
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(('localhost', 3333))
    print("P2P1 Started\n\n")
    while running:
        server.listen(4)
        (conn, (ip,port)) = server.accept()
        newthread = Server1(ip,port) 
        newthread.start()

def startP2P2():
    class Server2(Thread): 
 
        def __init__(self,ip,port): 
            Thread.__init__(self) 
            self.ip = ip 
            self.port = port
            print('Request received from Peer IP : '+ip+' with port no : '+str(port)+"\n")        
         
        def run(self):
            data = conn.recv(10000)
            data = pickle.loads(data)
            request_type = data[0]
            if request_type == "save":#cloud receive request to save encrypted data
                sid = data[1]
                dd = data[2]
                cname = data[3]
                conn.send("P2P 2 Data Received".encode())
                print("P2P 2: Student Attendance Received for ID = "+sid+" Time = "+dd)                              
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(('localhost', 4444))
    print("P2P2 Started\n\n")
    while running:
        server.listen(4)
        (conn, (ip,port)) = server.accept()
        newthread = Server2(ip,port) 
        newthread.start()         
    
def runP2P1():
    Thread(target=startP2P1).start()

def runP2P2():
    Thread(target=startP2P2).start()    

runP2P1()
runP2P2()
