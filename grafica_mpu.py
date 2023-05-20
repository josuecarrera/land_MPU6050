import sys
import serial
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QPoint
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('design1.ui', self)

        # Configurar la conexión serial con Arduino
        self.ser = serial.Serial('COM3', 115200, timeout=1)

        # Crear la figura de Matplotlib
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Aceleración')

        # Crear el lienzo de la figura de Matplotlib
        self.canvas = FigureCanvas(self.fig)

        # Agregar el lienzo a la ventana principal
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Iniciar el temporizador para actualizar la gráfica
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):
        # Leer los datos del sensor desde Arduino
        data = self.ser.readline().decode('utf-8').rstrip()
        if data:
            # Actualizar la gráfica con los nuevos datos
            values = data.split(',')
            if len(values) == 4:
                x = float(values[0])
                y = float(values[1])
                z = float(values[2])
                magnitude = float(values[3])

                self.ax.clear()
                self.ax.plot([1, 2, 3], [x, y, z], label='Aceleración')
                self.ax.set_xlabel('Eje')
                self.ax.set_ylabel('Aceleración')
                self.ax.legend()
                self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
