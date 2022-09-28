import sys
import cv2
import sys
import json
import requests
import base64
import cv2
import time
import pandas as pd
from tqdm import tqdm
from PyQt5.QtCore import *
import pyaudio
import wave
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
import time
class RECOGNIZE(QtCore.QThread):#识别线程类
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
    def chepai_label(self,info):
        self.chepai_result = info
    def __init__(self,*args, **kwargs):
        super(RECOGNIZE, self).__init__(*args, **kwargs)
        self._isPause = ""
        self._value = 0
        self.count = 1
        self.img = ""
        self.set = ""
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        client_id = '9bK9dOeGAai3F8YAGUeGKYas'
        client_secret = 'aP2iRPQievTBHfHkikjB32nU71B4Ews7'
        self.host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
        self.response = requests.get(self.host)
        if self.response:
            self.token_info = self.response.json()
            self.token_key = self.token_info['access_token']
    def run(self):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        try:
            f = open("./123.jpg", 'rb')
            img = base64.b64encode(f.read())
            params = {"image": img}
            access_token = self.token_key
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            print("进行到此")
            response = requests.post(request_url, data=params, headers=headers)
            print("请求成功")
            if response:
                print(response.json())
                result = response.json()["words_result"]
                print("车牌", result["number"])
                print("画图所需点", result["vertexes_location"])
                x1 = result["vertexes_location"][3]["x"]
                y1 = result["vertexes_location"][3]["y"]
                x2 = result["vertexes_location"][1]["x"]
                y2 = result["vertexes_location"][1]["y"]
            self.chepai_result.setText(result["number"])
            img = cv2.imread("./123.jpg")
            result = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imwrite("./result.jpg", result)
            print("结果图片写入成功")
        except:
            print("图片不存在或打开失败")






class Runthread(QtCore.QThread):#播放显示线程类
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self,*args, **kwargs):
        super(Runthread, self).__init__(*args, **kwargs)
        self._isPause = ""
        self._value = 0
        self.count = 1
        self.img = ""
        self.movie_get = ""
        self.set = ""
        self.cond = QWaitCondition()
        self.mutex = QMutex()
    def get_info(self,info):
        self.set = info
    def get_movie_Camera(self,what):
        self.chance = what
    def get_movie_name(self,name):
        self.movie_name = name

    def get_img(self,bt,info):
        self.show_result = bt
        self.img = info
        print("正常连接")
    def pause_start(self):
        print("播放暂停")
        print("计数", self.count)
        if self.count == 1:
            self._isPause = True
            print("self._isPause", self._isPause)
            self.count += 1
        else:
            print("播放开始")
            self._isPause = False
            print(self._isPause)
            self.cond.wakeAll()
            self.count = 1
    def run(self):
        if self.chance == "camera":
            print("开启摄像头")
            self.cap = cv2.VideoCapture(0)
            while True:
                self.mutex.lock()
                if self._isPause:
                    pass
                else:
                    if self.img == 1:
                        flag, self.image = self.cap.read()
                        self.show = cv2.resize(self.image, (500, 500))
                        self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)
                        self.showImage = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                                      QtGui.QImage.Format_RGB888)
                        self.set.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                        self.showImage2 = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                                       QtGui.QImage.Format_RGB888)
                        self.show_result.setPixmap(QtGui.QPixmap.fromImage(self.showImage2))
                        cv2.imwrite("./123.jpg", self.image)
                        print("摄像头图片写入成功")
                        self.img = 0
                    else:
                        flag, self.image = self.cap.read()
                        self.show = cv2.resize(self.image, (500, 500))
                        self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)
                        self.showImage = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                                      QtGui.QImage.Format_RGB888)
                        self.set.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                self.mutex.unlock()
            self.cap.release()
        elif self.chance == "movie":
            print("开始播放电影")
            self.cap1 = cv2.VideoCapture(self.movie_name)
            while True:
                if self.img == 1:
                    flag1, self.image1 = self.cap1.read()
                    time.sleep(0.03)
                    if flag1 != False:
                        self.show1 = cv2.resize(self.image1, (500, 500))
                        self.show1 = cv2.cvtColor(self.show1, cv2.COLOR_BGR2RGB)
                        self.showImage1 = QtGui.QImage(self.show1.data, self.show1.shape[1], self.show1.shape[0],
                                                   QtGui.QImage.Format_RGB888)
                        self.set.setPixmap(QtGui.QPixmap.fromImage(self.showImage1))
                        self.showImage2 = QtGui.QImage(self.show1.data, self.show1.shape[1], self.show1.shape[0],
                                                       QtGui.QImage.Format_RGB888)
                        self.show_result.setPixmap(QtGui.QPixmap.fromImage(self.showImage2))
                        cv2.imwrite("./123.jpg", self.image1)
                        print("视频图片写入成功")
                        self.img = 0
                else:
                    flag, self.image1 = self.cap1.read()
                    time.sleep(0.03)
                    if flag != False:
                        self.show1 = cv2.resize(self.image1, (500, 500))
                        self.show1 = cv2.cvtColor(self.show1, cv2.COLOR_BGR2RGB)
                        self.showImage1 = QtGui.QImage(self.show1.data, self.show1.shape[1], self.show1.shape[0],
                                                   QtGui.QImage.Format_RGB888)
                        self.set.setPixmap(QtGui.QPixmap.fromImage(self.showImage1))
                    else:
                        self.cap1.release()



class QPushButtonDemo(QDialog,QWidget):
    def __init__(self,*args, **kwargs):
        super(QPushButtonDemo, self).__init__(*args, **kwargs)
        self.initUI()
    def initUI(self):
        self.resize(800,600)
        self.setStyleSheet("color:white;background:#2B2B2B;")
        self.setWindowTitle("车牌识别")
        #设置布局
        self.layout=QHBoxLayout(self)
        self.layout1 = QVBoxLayout(self)
        self.base = QLabel("基准")
        self.base.setStyleSheet("color:white;background:#2B2B2B;")
        self.result = QLabel("结果")
        self.result.setStyleSheet("color:white;background:#2B2B2B;")
        self.result.resize(500,500)
        self.open_cam = QPushButton("打开摄像头")
        self.open_cam.setStyleSheet( '''QPushButton{color:black;background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.open_movie = QPushButton("打开视频")
        self.open_movie.setStyleSheet('''QPushButton{color:black;background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.chepai = QLabel("车牌号码显示")
        self.chepai.setStyleSheet("color:white;background:#2B2B2B;font-size:50px;")
        self.stop = QPushButton("暂停")
        self.stop.setStyleSheet(
            '''QPushButton{color:black;background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.get = QPushButton("取帧")
        self.get.setStyleSheet('''QPushButton{color:black;background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.get.clicked.connect(self.get_photo)
        self.use_model= QPushButton("识别")
        self.use_model.setStyleSheet(
            '''QPushButton{color:black;background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.get1 = QPushButton("显示结果")
        self.get1.setStyleSheet(
          '''QPushButton{color:black;background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.layout1.addWidget(self.open_cam)
        self.layout1.addWidget(self.open_movie)
        self.layout1.addWidget(self.get)
        self.layout1.addWidget(self.use_model)
        self.layout1.addWidget(self.chepai)
        self.layout1.addWidget(self.stop)
        self.layout1.addWidget(self.get1)
        self.layout.addWidget(self.base)
        self.layout.addWidget(self.result)
        self.layout.addLayout(self.layout1)
        self.setLayout(self.layout)
        self.thread = Runthread(self)#开摄像头线程
        self.recognize = RECOGNIZE(self)#开识别线程
        self.get1.clicked.connect(self.show_result)
        self.open_cam.clicked.connect(self.open_camera)
        self.open_movie.clicked.connect(self.movie_start)
        self.use_model.clicked.connect(self.recognize_img)
        self.test1 = Runthread(self)

    def show_result(self):
        self.result.setMaximumSize(500, 500)
        self.result.setPixmap(QPixmap("./result.jpg"))
        self.result.setScaledContents(True)  # 让图片自适应label大小
        # lbl.setPixmap(QPixmap(""))#移除label上的图片
    def recognize_img(self):
        self.recognize.chepai_label(self.chepai)
        self.recognize.start()
    def open_camera(self):
        if self.thread.isRunning():
            print("有进程在跑,关闭进程再开")
            self.thread.terminate()
            self.thread = Runthread(self)
            self.stop.clicked.connect(self.thread.pause_start)
            self.thread.get_movie_Camera("camera")
            self.thread.get_info(self.base)
            self.thread.start()
        else:
            print("没有在运行的进程")
            self.thread.get_movie_Camera("camera")
            self.thread.get_info(self.base)
            self.stop.clicked.connect(self.thread.pause_start)
            self.thread.start()


    def movie_start(self):
        frame, _ = QFileDialog.getOpenFileName(self, "车牌识别", "./", "*.mp4")
        if frame == "":  # 未选择文件
            return
        if self.thread.isRunning():
            print("有进程在跑,关闭进程再开")
            self.thread.terminate()
            self.thread = Runthread(self)
            self.thread.get_movie_Camera("movie")
            self.thread.get_movie_name(frame)
            self.thread.get_info(self.base)
            self.thread.start()
            print("线程开启")
        else:
            print("开启视频播放线程")
            self.thread.get_movie_Camera("movie")
            self.thread.get_movie_name(frame)
            self.thread.get_info(self.base)
            self.thread.start()




    def get_photo(self):
        self.thread.get_img(self.result,1)#self.result:结果展示label
    def open_movie(self):
        self.cap = cv2.VideoCapture(0)
        flag, self.image = self.cap.read()
        # face = self.face_detect.align(self.image)
        # if face:
        #     pass
        while True:
            show = cv2.resize(self.image, (200, 200))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.base.setPixmap(QtGui.QPixmap.fromImage(self.showImage))

    def get_file_name(self):
        #得到打开文件名                           窗口标题    路径       限制条件    QFileDialog.getOpenFileName:返回一个选定的文件名 Names:可多选返回多个
        frame,_=QFileDialog.getOpenFileName(self,"高达","D:/","*.mp4") #frame:为文件路径, _为限制条件
        print(frame)#frame为文件路径
        # self.label.setPixmap(QPixmap(frame))

if __name__ =='__main__':
    app=QApplication(sys.argv)
    main=QPushButtonDemo()
    main.show()
    sys.exit(app.exec())