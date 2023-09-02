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

    def transformaciones(theta, x, y, z):

        rotx = np.array([[1, 0, 0, 0],
                        [0, np.cos(theta), -np.sin(theta), 0],
                        [0, np.sin(theta), np.cos(theta), 0],
                        [0, 0, 0, 1]])
        roty = np.array([[np.cos(theta), 0, np.sin(theta), 0],
                        [0, 1, 0, 0],
                        [-np.sin(theta), 0, np.cos(theta), 0],
                        [0, 0, 0, 1]])
        rotz = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                         [np.sin(theta), np.cos(theta), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

        tras = np.array[[1, 0, 0, x],
                        [0, 1, 0, y],
                        [0, 0, 1, z],
                        [0, 0, 0, 1]]
        return []

    def plot_3d(self):
        fig = self.canvas.figure
        ax = fig.add_subplot(111, projection='3d')

        # # Datos de ejemplo
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)

        # Definir límites de los ejes
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)

        # Sistema de coordenadas fijo
        ax.quiver(0, 0, 0, 2, 0, 0, color='r', label='X')
        ax.quiver(0, 0, 0, 0, 2, 0, color='g', label='Y')
        ax.quiver(0, 0, 0, 0, 0, 2, color='b', label='Z')

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
