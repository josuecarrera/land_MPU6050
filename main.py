from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import random
import serial

class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("qt_designer.ui", self)

        #Configuracion la conexion serial con Arduino 
        self.ser = serial.Serial('COM3', 115200, timeout=1)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        # Crea la variable del boton
        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)
        # crea la variable de la venta de graficas
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas,self.MplWidget_2.canvas, self))
        

        #Inicia el temporizador para actualizar la grafica
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)

    def update_graph(self):

        data = self.ser.readline().decode('utf-8').rstrip()
        # fs = 500
        # f = random.randint(1, 100)
        # ts = 1/fs
        # lenght_of_signal = 100
        # t = np.linspace(0,1,lenght_of_signal)

        # cosinus_signal = np.cos(2*np.pi*f*t)
        # sinus_signal = np.sin(2*np.pi*f*t)
        if data:
            values = data.split(',')
            if len(values) == 4:
                x = float(values[0])
                y = float(values[1])
                z = float(values[2])
                magnitude = float(values[3])
                print(magnitude)

                self.MplWidget.canvas.axes.clear()
                self.MplWidget.canvas.axes.plot([1,2,3], [x,y,z])
                self.MplWidget_2.canvas.axes.plot([1, 2, 3], [magnitude, magnitude, magnitude])
                self.MplWidget.canvas.axes.legend(('aceleracion', 'magnitud'), loc=('upper right'))
                self.MplWidget.canvas.axes.set_title('Aceleracion')
                self.MplWidget_2.canvas.axes.set_title('Magnitud signal')
                self.MplWidget.canvas.draw()
                self.MplWidget_2.canvas.draw()
        
                self.update_soil_type(magnitude)
                self.update_axes_type(x,y,z)

    def update_soil_type(self, magnitude):
        if magnitude < 8:
            soil_type = "Firme"
        elif magnitude < 10:
            soil_type = "Blando"
        elif magnitude < 12:
            soil_type = "Líquido"
        else:
            soil_type = "Desconocido"

        self.label_soil_type.setText(soil_type)

    def update_axes_type(self, x,y,z):
        axes_type_x = str(x)
        axes_type_y = str(y)
        axes_type_z = str(z)

        self.label_axis_x.setText(axes_type_x)
        self.label_axis_y.setText(axes_type_y)
        self.label_axis_z.setText(axes_type_z)

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()

