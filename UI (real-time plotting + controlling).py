import random
import sys
import pyqtgraph as pg
import time
from PyQt5 import QtGui, QtCore
import serial
from numpy import *
import queue

port = serial.Serial("COM6",1000000)
port.flushInput()


class MyThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(object)
    send1 = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent=parent)
        

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        self.state = 0
        self.Xm = linspace(0,0,1000)
        
        
        while port.writable() and self.state==0:
            port.write(b'1\r\n')
            self.state=1
            print('send')
            
        while port.readable():
            self.value = port.readline().decode()
            self.data1 = self.value.split('\r\n')
            self.data = self.data1[0].split('-')
            print(self.data)
            self.length = len(self.data)
            i=0
            while (i<self.length):
                if(self.data[i]!='' and self.data[i] !='\n'):
                    self.Xm[:-1] = self.Xm[1:]
                    self.Xm[-1] = int(self.data[i])
                i=i+1
            self.signal.emit(self.Xm)



class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)

        self.myThread = MyThread()
        layout = QtGui.QHBoxLayout()
        seclayout = QtGui.QVBoxLayout()
        self.tb = QtGui.QToolBar()
        self.times = QtCore.QTime()

        self.startbutton = QtGui.QPushButton('Start Plotting')
        self.stopbutton = QtGui.QPushButton('Stop Plotting')
        self.button50 = QtGui.QPushButton('5Hz')
        self.button100 = QtGui.QPushButton('10Hz')
        self.button150 = QtGui.QPushButton('20Hz')
        self.button200 = QtGui.QPushButton('40Hz')
        seclayout.addWidget(self.startbutton)
        seclayout.addWidget(self.stopbutton)
        seclayout.addWidget(self.button50)
        seclayout.addWidget(self.button100)
        seclayout.addWidget(self.button150)
        seclayout.addWidget(self.button200)
        
        layout.addLayout(seclayout)
        
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)
        self.setLayout(layout)

        self.curve = self.plot.getPlotItem().plot()
        
        self.startbutton.clicked.connect(self.start)
        self.stopbutton.clicked.connect(self.stop)
        self.button50.clicked.connect(self.send3)
        self.button100.clicked.connect(self.send4)
        self.button150.clicked.connect(self.send5)
        self.button200.clicked.connect(self.send6)

        self.windowWidth = 1000
        self.Xms = linspace(0,0,1000)
        
        
        self.X = linspace(0,0,self.windowWidth)
        self.ptr=0

        self.finished = True
        self.run = False


    def plotter(self, data):
        if self.run==True:
            self.Xms = data
            if self.finished == True:
                self.finished = False
                self.curve.setData(self.Xms)
                self.finished = True
        
    def start(self):
        self.run = True
        self.times.start()
        self.myThread.start()
        self.myThread.signal.connect(self.plotter)

    def stop(self):
        self.run = False
        
    def send3(self):
        if port.writable():
            port.write(b'3\r\n')
            print('a')

    def send4(self):
        if port.writable():
            port.write(b'4\r\n')
            print('b')

    def send5(self):
        if port.writable():
            port.write(b'5\r\n')
            print('c')

    def send6(self):
        if port.writable():
            port.write(b'6\r\n')
            print('d')


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.centralwidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.login_widget_1 = LoginWidget(self)
        self.horizontalLayout.addWidget(self.login_widget_1)


       
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle('Simultaneous Neural Recording and Stimulation')
    w.show()
    sys.exit(app.exec_())
