from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MplWidget(QWidget):
    def __init__(self, parent= None):
        QWidget.__init__(self, parent)
        #Crea el lienzo de la figura de MatplotLib
        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.axes.set_xlabel('Tiempo')
        self.canvas.axes.set_ylabel('Aceleracion')
        self.setLayout(vertical_layout)

        
