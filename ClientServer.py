import socket 
from threading import Thread 
from socketserver import ThreadingMixIn
import socket
import pickle

running = True

def startClientServer():
    class Server(Thread): 
 
        def __init__(self,ip,port): 
            Thread.__init__(self) 
            self.ip = ip 
            self.port = port
            print('Request received from Client IP : '+ip+' with port no : '+str(port)+"\n")        
         
        def run(self):
            data = conn.recv(10000)
            data = pickle.loads(data)
            request_type = data[0]
            if request_type == "save":#cloud receive request to save encrypted data
                sid = data[1]
                dd = data[2]
                cname = data[3]
                conn.send("Client Server Data Received".encode())
                print("Client Server: Student Attendance Received for ID = "+sid+" Time = "+dd)                              
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(('localhost', 2222))
    print("Client Server Started\n\n")
    while running:
        server.listen(4)
        (conn, (ip,port)) = server.accept()
        newthread = Server(ip,port) 
        newthread.start() 
    
def startServer():
    Thread(target=startClientServer).start()

startServer()

