import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
import random
import  serial 
import time
import threading

##ser = serial.Serial('COM6', baudrate=9600, timeout=10,
##                    stopbits=serial.STOPBITS_ONE,
##                    bytesize=serial.EIGHTBITS
##                    )

x=list()
y1=list()
y2=list()
i=0

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arduino Real Time Graph")
        self.setGeometry(50,50,1200,660)
        self.UI()
        

    def UI(self):
        self.setStyleSheet("background-color:white;font-size:12pt;font-family:Times;")
        mainLayout=QHBoxLayout()
        leftFormLayout=QFormLayout()
        rightLayout=QVBoxLayout()
        mainLayout.addLayout(leftFormLayout,30)
        mainLayout.addLayout(rightLayout,70)
        

        self.image=QLabel()
        self.image.setPixmap(QPixmap("robot.png"))
        self.port_label=QLabel("Port :")
        self.port=QComboBox()
        self.port.setStyleSheet("font-size:8pt;")
        self.list_port()
        self.frequency_label=QLabel("Frequency(Hz) :")
        self.frequency=QLineEdit()
        self.baudrate_label=QLabel("BaudRate :")
        self.baudrate=QComboBox()
        self.baudrate.addItems(["115200"])
        self.accx=QLabel("Acceloremeter X :")
        self.accx_value=QLabel("...")
        self.accx.setStyleSheet("color:red;")
        self.accx_value.setStyleSheet("color:red;")
        self.accy=QLabel("Filter X :")
        self.accy_value=QLabel("...")
        self.accy.setStyleSheet("color:green;")
        self.accy_value.setStyleSheet("color:green;")
        #self.accz=QLabel("Acceloremeter Z :")
        #self.accz_value=QLabel("...")
        #self.gyrox=QLabel("Gyro X          :")
        #self.gyrox_value=QLabel("...")
        #self.gyroy=QLabel("Gyro Y          :")
        #self.gyroy_value=QLabel("...")
        #self.gyroz=QLabel("Gyro Z          :")
        #self.gyroz_value=QLabel("...")
        #self.filter_x=QLabel("Filter X        :")
        #self.filter_x_value=QLabel("...")

        
        self.btn_connect=QPushButton("Enter",self)
        self.btn_connect.clicked.connect(self.connect_system)
        
        self.btn_exit=QPushButton("Exit",self)
        self.btn_exit.clicked.connect(self.exit)
        
        self.graphWidget = pg.PlotWidget()
        
        leftFormLayout.setContentsMargins(10,10,10,10)
        leftFormLayout.addRow(self.image)
        leftFormLayout.addRow(self.port_label,self.port)
        leftFormLayout.addRow(self.baudrate_label,self.baudrate)
        leftFormLayout.addRow(self.frequency_label,self.frequency)
        leftFormLayout.addRow(self.btn_connect,self.btn_exit)
        leftFormLayout.addRow(self.accx,self.accx_value)
        leftFormLayout.addRow(self.accy,self.accy_value)
        #leftFormLayout.addRow(self.accz,self.accz_value)
        #leftFormLayout.addRow(self.gyrox,self.gyrox_value)
        #leftFormLayout.addRow(self.gyroy,self.gyroy_value)
        #leftFormLayout.addRow(self.gyroz,self.gyroz_value)
        #leftFormLayout.addRow(self.filter_x,self.filter_x_value)
        rightLayout.addWidget(self.graphWidget)
        
        
        self.setLayout(mainLayout)

        self.timer=QTimer()
        self.timer.setInterval(195)
        self.timer.timeout.connect(self.draw)
        self.show()
        
        
    def list_port(self):
        ports = list(serial.tools.list_ports.comports())
        print(ports)
        for p in ports:
            print(p)
            self.port.addItems(p)
            
        
    def exit(self):
        self.timer.stop()
        sys.exit()
        
    def connect_system(self):
        global ser
        print("Connecting System")
        ser = serial.Serial(self.port.currentText(), 115200)
        print(str(self.port)+" Connecting Port")
        self.timer.start()


    def draw(self):
        global ser
        global i
        line = str(ser.readline())
##        print(line)
        data = line.split(",")
        self.accx_value.setText(str(data[1]))
        self.accy_value.setText(str(data[3]))
#        self.accz_value.setText(str(data[3]))
 #       self.gyrox_value.setText(str(data[4]))
#        self.gyroy_value.setText(str(data[5]))
#        self.gyroz_value.setText(str(data[6]))
#        self.gyroz_value.setText(str(data[6]))
#        self.filter_x_value.setText(str(data[7]))
        
        
        x.append(i)
##        y1.append(random.uniform(1,100))
##        y2.append(random.uniform(1,100))
        y1.append(float(data[1]))  #Xangle data
        y2.append(float(data[3]))  #X angle Filter data
        i = i+1
            
        pen = pg.mkPen(color=(255, 0, 0),width=1)
        pen2 = pg.mkPen(color=(0, 255, 0),width=1)
        self.graphWidget.setLabel('left', 'Gyro ', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Time', color='red', size=30)
            
        self.graphWidget.plot(x, y1,name="Data 1" ,pen=pen)
        self.graphWidget.plot(x, y2 ,name="Data 2",pen=pen2)
        

        
        

def main():
    App=QApplication(sys.argv)
    window=Window()
    sys.exit(App.exec_())
       


if __name__=='__main__':
    main()