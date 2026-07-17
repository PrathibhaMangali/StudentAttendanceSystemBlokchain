from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import json
from web3 import Web3, HTTPProvider
import base64
import pandas as pd #pandas to read and explore dataset
import numpy as np
import io
import socket
import pickle
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import numpy as np
from PIL import Image
import cv2
from keras.models import load_model
from numpy import dot
from numpy.linalg import norm
from datetime import datetime
import timeit

global username, studentList, attendanceList
global contract, web3, mtcnn_model, facenet_model, features, names
hybrid = []
p2p = []
client_server = []

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Attendance.json' #Attendance contract file
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getStudentList():
    global studentList, contract
    studentList = []
    count = contract.functions.getStudentCount().call()
    for i in range(0, count):
        sid = contract.functions.getID(i).call()
        sname = contract.functions.getName(i).call()
        course = contract.functions.getCourse(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        address = contract.functions.getAddress(i).call()
        studentList.append([sid, sname, course, phone, email, address])

def getAttendanceList():
    global attendanceList, contract
    attendanceList = []
    count = contract.functions.getAttendanceCount().call()
    for i in range(0, count):
        sid = contract.functions.getStdID(i).call()
        attended_date = contract.functions.getAttendanceDate(i).call()
        class_name = contract.functions.getClassName(i).call()
        attendanceList.append([sid, attended_date, class_name])

getStudentList()
getAttendanceList()

def ViewStudentAttendance(request):
    if request.method == 'GET':
        global studentList
        output = '<tr><td><font size="3" color="black">Choose&nbsp;Student&nbsp;ID</td><td><select name="t1">'
        for i in range(len(studentList)):
            slist = studentList[i]
            output += '<option value="'+slist[0]+'">'+slist[0]+'</option>'
        output += '</select></td></tr>'
        context = {'data1': output}
        return render(request, 'ViewStudentAttendance.html', context)

def ViewStudentAttendanceAction(request):
    if request.method == 'POST':
        global studentList, attendanceList
        sid = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Student ID</font></th>'
        output+='<th><font size=3 color=black>Attended Date</font></th>'
        output+='<th><font size=3 color=black>Class Name</font></th>'
        output+='<th><font size=3 color=black>Student Image</font></th></tr>'
        for i in range(len(attendanceList)):
            alist = attendanceList[i]
            if alist[0] == sid:
                output+='<tr><td><font size=3 color=black>'+alist[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(alist[2])+'</font></td>'
                output+='<td><img src="/static/faces/'+alist[0]+'.png" width="200" height="200"></img></td></tr>' 
        output+="</table><br/><br/><br/><br/>"
        context= {'data':output}
        page = 'FacultyScreen.html'
        if username == "hod":
            page = "HodScreen.html"
        return render(request, page, context)                


def ViewStudent(request):
    if request.method == 'GET':
        global studentList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Student ID</font></th>'
        output+='<th><font size=3 color=black>Student Name</font></th>'
        output+='<th><font size=3 color=black>Course Name</font></th>'
        output+='<th><font size=3 color=black>Phone No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Student Address</font></th>'
        output+='<th><font size=3 color=black>Student Photo</font></th></tr>'
        for i in range(len(studentList)):
            plist = studentList[i]
            output+='<tr><td><font size=3 color=black>'+plist[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+str(plist[2])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(plist[3])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(plist[4])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(plist[5])+'</font></td>'
            output+='<td><img src="/static/faces/'+plist[0]+'.png" width="200" height="200"></img></td></tr>' 
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)

#get face embedding using facenet
def get_embedding(face_pixels, facenet_model):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    embedding = facenet_model.predict(samples)
    return embedding[0]

def extract_face(filename, mtcnn_model):
    image = Image.open(filename)
    image = image.convert('RGB')
    pixels = np.asarray(image)
    results = mtcnn_model.detect_faces(pixels)
    return results, pixels

def trainModel():
    global features, names
    features = []
    names = []
    mtcnn_model = MTCNN()
    facenet_model = load_model('model/facenet_keras.h5')
    for root, dirs, directory in os.walk("AttendanceApp/static/faces"):
        for j in range(len(directory)):
            results, pixels = extract_face(root+"/"+directory[j], mtcnn_model)
            print(len(results))
            if len(results) > 0:
                x1, y1, width, height = results[0]['box']
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height
                face = pixels[y1:y2, x1:x2]
                image = Image.fromarray(face)
                image = image.resize((160, 160))
                img = np.asarray(image)            
                embedding = get_embedding(img, facenet_model)
                features.append(embedding)
                name = directory[j].split(".")
                names.append(name[0])
    features = np.asarray(features)
    names = np.asarray(names)
    print("Total faces = "+str(features.shape)+" "+str(names.shape))

trainModel()    

def index(request):
    if request.method == 'GET':
        return render(request,'index.html', {})

def AddStudent(request):
    if request.method == 'GET':
        return render(request,'AddStudent.html', {})

def FacultyLogin(request):
    if request.method == 'GET':
       return render(request, 'FacultyLogin.html', {})
    
def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def Graph(request):
    if request.method == 'GET':
        global hybrid, p2p, client_server
        index = []
        for i in range(len(hybrid)):
            index.append(i+1)
        plt.plot(index, hybrid, label="Hybrid Blockchain")
        plt.plot(index, p2p, label="Peer 2 Peer")
        plt.plot(index, client_server, label="Client Server")
        plt.legend()
        plt.title("Cost Computation Time Chart")
        plt.xlabel("Technique Name")
        plt.ylabel("Computation Time")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()    
        context= {'data':"Cost Computation Time Chart", 'img': img_b64}
        page = 'FacultyScreen.html'
        if username == "hod":
            page = "HodScreen.html"
        return render(request, page, context)   

def MarkAttendanceAction(request):
    if request.method == 'POST':
        global studentList, attendanceList, features, names
        global hybrid, p2p, client_server
        class_name = request.POST.get('t1', False)
        filename = request.FILES['t2'].name
        image = request.FILES['t2'].read() #reading uploaded file from user
        sid = str(len(studentList) + 1)
        if os.path.exists("AttendanceApp/static/test.png"):
            os.remove("AttendanceApp/static/test.png")
        with open("AttendanceApp/static/test.png", "wb") as file:
            file.write(image)
        file.close()
        mtcnn_model = MTCNN()
        facenet_model = load_model('model/facenet_keras.h5')
        results, pixels = extract_face("AttendanceApp/static/test.png", mtcnn_model)
        output = "Error in marking attendance"
        if len(results) > 0:
            x1, y1, width, height = results[0]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            face = pixels[y1:y2, x1:x2]
            image = Image.fromarray(face)
            image = image.resize((160, 160))
            img = np.asarray(image)            
            embedding = get_embedding(img, facenet_model)
            embedding = embedding.ravel()
            print(embedding.shape)
            max_accuracy = 0
            index = -1
            for i in range(len(features)):
                predict_score = dot(features[i], embedding)/(norm(features[i])*norm(embedding))
                if predict_score > max_accuracy:
                    max_accuracy = predict_score
                    index = i
            print(max_accuracy)        
            start = timeit.default_timer()        
            sid = names[index]
            current_date = datetime.now()
            current_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
            current_date = str(current_date)
            output = "Student recognized with student id = "+sid+"<br/>Marked Attendance on "+current_date
            attendanceList.append([sid, current_date, class_name])
            msg = contract.functions.saveAttendance(sid, current_date, class_name).transact()
            end = timeit.default_timer()
            hybrid.append((end - start))
            start = timeit.default_timer()  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 2222))
            data = ["save", sid, current_date, class_name]
            data = pickle.dumps(data)
            s.sendall(data)
            data1 = s.recv(100)
            data1 = data1.decode()
            end = timeit.default_timer()
            client_server.append((end - start))
            start = timeit.default_timer()  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 3333))
            s.sendall(data)
            data1 = s.recv(100)
            data1 = data1.decode()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 4444))
            s.sendall(data)
            data1 = s.recv(100)
            data1 = data1.decode()
            end = timeit.default_timer()            
            p2p.append((end - start))
            print(hybrid)
            print(p2p)
            print(client_server)
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        else:
            output = "No face detected in uploaded image"
        context= {'data':'<font size="3" color="blue">'+output}
        page = 'FacultyScreen.html'
        if username == "hod":
            page = "HodScreen.html"
        return render(request, page, context)    

def MarkAttendance(request):
    if request.method == 'GET':
       return render(request, 'MarkAttendance.html', {})

def ViewAttendance(request):
    if request.method == 'GET':
        global studentList
        output = '<tr><td><font size="3" color="black">Choose&nbsp;Student&nbsp;ID</td><td><select name="t1">'
        for i in range(len(studentList)):
            slist = studentList[i]
            output += '<option value="'+slist[0]+'">'+slist[0]+'</option>'
        output += '</select></td></tr>'
        context = {'data1': output}
        return render(request, 'ViewAttendance.html', context)

def ViewAttendanceAction(request):
    if request.method == 'POST':
        global studentList, attendanceList
        sid = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Student ID</font></th>'
        output+='<th><font size=3 color=black>Attended Date</font></th>'
        output+='<th><font size=3 color=black>Class Name</font></th>'
        output+='<th><font size=3 color=black>Student Image</font></th></tr>'
        for i in range(len(attendanceList)):
            alist = attendanceList[i]
            if alist[0] == sid:
                output+='<tr><td><font size=3 color=black>'+alist[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(alist[2])+'</font></td>'
                output+='<td><img src="/static/faces/'+alist[0]+'.png" width="200" height="200"></img></td></tr>' 
        output+="</table><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)                

def AddStudentAction(request):
    if request.method == 'POST':
        global studentList
        std_name = request.POST.get('t1', False)
        course = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        filename = request.FILES['t6'].name
        image = request.FILES['t6'].read() #reading uploaded file from user
        sid = str(len(studentList) + 1)
        if os.path.exists("AttendanceApp/static/faces/"+str(sid)+".png"):
            os.remove("AttendanceApp/static/faces/"+str(sid)+".png")
        with open("AttendanceApp/static/faces/"+str(sid)+".png", "wb") as file:
            file.write(image)
        file.close()
        msg = contract.functions.saveStudent(sid, std_name, course, contact, email, address).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        studentList.append([sid, std_name, course, contact, email, address])
        trainModel()
        context= {'data':'<font size="3" color="blue">Student details added with student id = '+str(sid)+'<br/><br/>'+str(tx_receipt)}
        return render(request, 'AddStudent.html', context)
        
def AdminLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "AdminScreen.html", context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)
        
def FacultyLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'faculty' and password == 'faculty':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "FacultyScreen.html", context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'FacultyLogin.html', context)


def HodLogin(request):
    if request.method == 'GET':
       return render(request, 'HodLogin.html', {})        

def HodLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'hod' and password == 'hod':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "HodScreen.html", context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'HodLogin.html', context)
        
