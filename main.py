import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        loadUi("Grafica3D.ui", self)
        self.setWindowTitle("Gráfica 3D con PyQt5 y Matplotlib")

        # Agregar el widget de Matplotlib al diseño
        self.canvas = FigureCanvas(plt.figure())
        self.plotWidget.addWidget(self.canvas)

        # Crear una gráfica 3D
        self.plot_3d()

    def transformaciones():
        
        return []

    def plot_3d(self):
        fig = self.canvas.figure
        ax = fig.add_subplot(111, projection='3d')

        # # Datos de ejemplo
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)

        # Definir límites de los ejes
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)

        # Sistema de coordenadas fijo
        # ax.plot([-1, 1], [0, 0], [0, 0], 'r', label='X')
        # ax.plot([0, 0], [-1, 1], [0, 0], 'g', label='Y')
        # ax.plot([0, 0], [0, 0], [-1, 1], 'b', label='Z')

        # Sistema de coordenadas móvil
        ax.quiver(0, 0, 0, 1, 0, 0, color='#beee3b', label='X\'')
        ax.quiver(0, 0, 0, 0, 1, 0, color='#00c9d2', label='Y\'')
        ax.quiver(0, 0, 0, 0, 0, 1, color='#006465', label='Z\'')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
