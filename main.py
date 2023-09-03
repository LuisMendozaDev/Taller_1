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

        self.iteration = 0
        self.trasx = 0
        self.trasy = 0
        self.trasz = 0

        self.rotx = 0
        self.roty = 0
        self.rotz = 0

        self.theta_x = 0
        self.theta_y = 0
        self.theta_z = 0

        # Slider para realizar rotaciones
        self.rot_x.valueChanged.connect(self.get_rot_x)
        self.rot_y.valueChanged.connect(self.get_rot_y)
        self.rot_z.valueChanged.connect(self.get_rot_z)

        # Botones
        self.bt_calcular.clicked.connect(self.calculate)
        self.bt_reset.clicked.connect(self.reset)

        # Agregar el widget de Matplotlib al diseño
        self.canvas = FigureCanvas(plt.figure())
        self.plotWidget.addWidget(self.canvas)

        # Crear una gráfica 3D
        self.canvas.figure.clear()
        self.plot_3d()

    def reset(self):
        self.rot_x.setValue(0)
        self.rot_y.setValue(0)
        self.rot_z.setValue(0)
        self.transformations()

    def get_rot_x(self, event):
        self.theta_x = np.radians(event)
        self.lb_rotx.setText(str(event) + "°")
        self.rot_y.setDisabled(True)
        self.rot_z.setDisabled(True)
        self.rotx = np.array([[1, 0, 0, 0],
                              [0, np.cos(self.theta_x), -
                               np.sin(self.theta_x), 0],
                              [0, np.sin(self.theta_x),
                               np.cos(self.theta_x), 0],
                              [0, 0, 0, 1]])
        # self.theta = event

    def get_rot_y(self, event):
        self.theta_y = np.radians(event)
        self.lb_roty.setText(str(event) + "°")
        self.rot_x.setDisabled(True)
        self.rot_z.setDisabled(True)

        self.roty = np.array([[np.cos(self.theta_y), 0, np.sin(self.theta_y), 0],
                              [0, 1, 0, 0],
                              [-np.sin(self.theta_y), 0,
                               np.cos(self.theta_y), 0],
                              [0, 0, 0, 1]])
        # self.theta = event

    def get_rot_z(self, event):
        self.theta_z = np.radians(event)
        self.lb_rotz.setText(str(event) + "°")
        self.rot_x.setDisabled(True)
        self.rot_y.setDisabled(True)

        self.rotz = np.array([[np.cos(self.theta_z), -np.sin(self.theta_z), 0, 0],
                              [np.sin(self.theta_z), np.cos(
                                  self.theta_z), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        # self.theta = event

    def transformations(self, A, B):
        C = A@B
        print(C)

    def calculate(self):
        # self.canvas.figure.clear()

        self.rot_x.setDisabled(False)
        self.rot_y.setDisabled(False)
        self.rot_z.setDisabled(False)

        self.trasx = self.tras_x.value()
        self.trasy = self.tras_y.value()
        self.trasz = self.tras_z.value()

        self.tras = np.array([[1, 0, 0, self.trasx],
                             [0, 1, 0, self.trasy],
                             [0, 0, 1, self.trasz],
                             [0, 0, 0, 1]])

        print(self.iteration)
        self.iteration += 1
        if (self.iteration == 2):
            self.iteration = 0
        self.plot_3d()

    def plot_3d(self):
        fig = self.canvas.figure
        ax = fig.add_subplot(111, projection='3d')

        # Definir límites de los ejes
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)

        # Sistema de coordenadas fijo
        ax.quiver(0, 0, 0, 2, 0, 0, color='r', label='X')
        ax.quiver(0, 0, 0, 0, 2, 0, color='g', label='Y')
        ax.quiver(0, 0, 0, 0, 0, 2, color='b', label='Z')

        # Sistema de coordenadas móvil
        ax.quiver(self.theta_x, self.theta_y, self.theta_z,
                  1, 0, 0, color='#beee3b', label='X\'')
        ax.quiver(self.theta_x, self.theta_y, self.theta_z,
                  0, 1, 0, color='#00c9d2', label='Y\'')
        ax.quiver(self.theta_x, self.theta_y, self.theta_z,
                  0, 0, 1, color='#006465', label='Z\'')

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
