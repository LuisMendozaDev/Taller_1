import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow,  QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        loadUi("Grafica3D.ui", self)

        self.setWindowTitle("Gráfica 3D con PyQt5 y Matplotlib")

        self.t_matrix = np.identity(4)
        self.vector = np.array([0, 0, 0])

        self.is_tras = False
        self.is_rot = False


        self.set_zero()
        self.fill_table()
        self.rd_fijo.setChecked(True)


        # self.matriz_trans.setItem(1, 1,  QTableWidgetItem("2"))

        # Spin para realizar traslaciones
        self.tras_x.valueChanged.connect(self.traslation)
        self.tras_y.valueChanged.connect(self.traslation)
        self.tras_z.valueChanged.connect(self.traslation)

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

    def set_zero(self):
        self.A = np.identity(4)
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

        self.rot_x.setValue(0)
        self.rot_y.setValue(0)
        self.rot_z.setValue(0)

        self.tras_x.setValue(0)
        self.tras_y.setValue(0)
        self.tras_z.setValue(0)

        self.spin_state(False)
        self.rot_x.setDisabled(False)
        self.rot_y.setDisabled(False)
        self.rot_z.setDisabled(False)

    def fill_table(self):
        for i in range(4):
            for j in range(4):
                self.matriz_trans.setItem(
                    i, j,  QTableWidgetItem(str(round(self.t_matrix[i][j], 3))))
        self.matriz_trans.resizeColumnsToContents()

        for i in range(3):
            self.vector_origen.setItem(
                    i, 0,  QTableWidgetItem(str(round(self.vector[i], 3))))
        self.matriz_trans.resizeColumnsToContents()

    def traslation(self):
        self.is_tras = True

        self.trasx = self.tras_x.value()
        self.trasy = self.tras_y.value()
        self.trasz = self.tras_z.value()

        self.tras = np.array([[1, 0, 0, self.trasx],
                             [0, 1, 0, self.trasy],
                             [0, 0, 1, self.trasz],
                             [0, 0, 0, 1]])

        self.rot_x.setDisabled(True)
        self.rot_y.setDisabled(True)
        self.rot_z.setDisabled(True)

    def spin_state(self, value):
        self.tras_x.setDisabled(value)
        self.tras_y.setDisabled(value)
        self.tras_z.setDisabled(value)

    def reset(self):
        self.canvas.figure.clear()
        self.set_zero()
        self.t_matrix = np.identity(4)
        self.lb_mov.setText("MOVIMIENTO: " + str((self.iteration+1)))
        self.plot_3d()
        self.fill_table()

    def get_rot_x(self, event):
        self.is_rot = True
        self.is_tras = False
        self.theta_x = np.radians(event)
        self.lb_rotx.setText(str(event) + "°")

        self.rot_y.setDisabled(True)
        self.rot_z.setDisabled(True)

        self.spin_state(True)
        self.rotx = np.array([[1, 0, 0, 0],
                              [0, np.cos(self.theta_x), -
                               np.sin(self.theta_x), 0],
                              [0, np.sin(self.theta_x),
                               np.cos(self.theta_x), 0],
                              [0, 0, 0, 1]])
        # self.theta = event

    def get_rot_y(self, event):
        self.is_rot = True
        self.is_tras = False
        self.theta_y = np.radians(event)
        self.lb_roty.setText(str(event) + "°")

        self.rot_x.setDisabled(True)
        self.rot_z.setDisabled(True)

        self.spin_state(True)

        self.roty = np.array([[np.cos(self.theta_y), 0, np.sin(self.theta_y), 0],
                              [0, 1, 0, 0],
                              [-np.sin(self.theta_y), 0,
                               np.cos(self.theta_y), 0],
                              [0, 0, 0, 1]])
        # self.theta = event

    def get_rot_z(self, event):
        self.is_rot = True
        self.is_tras = False
        self.theta_z = np.radians(event)
        self.lb_rotz.setText(str(event) + "°")

        self.rot_x.setDisabled(True)
        self.rot_y.setDisabled(True)

        self.spin_state(True)

        self.rotz = np.array([[np.cos(self.theta_z), -np.sin(self.theta_z), 0, 0],
                              [np.sin(self.theta_z), np.cos(
                                  self.theta_z), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        # self.theta = event

    def calculate(self):
        self.canvas.figure.clear()

        if (self.is_tras):
            self.A = self.tras
        else:
            if (self.rot_x.isEnabled()):
                self.A = self.rotx
            elif (self.rot_y.isEnabled()):
                self.A = self.roty
            else:
                self.A = self.rotz

        if (self.rd_fijo.isChecked()):
            self.t_matrix = self.A@self.t_matrix
        else:
            self.t_matrix = self.t_matrix@self.A

        self.rot_x.setDisabled(False)
        self.rot_y.setDisabled(False)
        self.rot_z.setDisabled(False)

        self.spin_state(False)

        self.iteration += 1
        self.lb_mov.setText("MOVIMIENTO: " + str((self.iteration+1)))
        self.plot_3d()
        self.fill_table()
        self.set_zero()

    def plot_3d(self):
        fig = self.canvas.figure
        ax = fig.add_subplot(111, projection='3d')

        # Definir límites de los ejes
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(-10, 10)

        # Sistema de coordenadas fijo
        ax.quiver(0, 0, 0, 2, 0, 0, color='r', label='X')
        ax.quiver(0, 0, 0, 0, 2, 0, color='g', label='Y')
        ax.quiver(0, 0, 0, 0, 0, 2, color='b', label='Z')

        x, y, z, scale = self.t_matrix@np.array([0, 0, 0, 1])
        self.vector = [x, y, z]
        u, v, w, scale = self.t_matrix@[1, 0, 0, 1]
        _u, _v, _w, scale = self.t_matrix@[0, 1, 0, 1]
        __u, __v, __w, scale = self.t_matrix@[0, 0, 1, 1]

        ax.quiver(0, 0, 0, x, y, z, color='#7e2f8e')

        # Sistema de coordenadas móvil
        ax.quiver(x, y, z, u-x, v-y, w-z, color='#beee3b', label='X\'')
        ax.quiver(x, y, z, _u-x, _v-y, _w-z, color='#00c9d2', label='Y\'')
        ax.quiver(x, y, z, __u-x, __v-y, __w-z, color='#006465', label='Z\'')

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
