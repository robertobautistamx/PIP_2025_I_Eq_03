import sys

from PyQt5 import uic, QtWidgets
qtCreatorFile = "E03_Ejercicio3.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_calcular.clicked.connect(self.calcular)
        self.btn_salir.clicked.connect(self.salir)
#slots
    def calcular(self):
        try:
            area=self.txt_lado.text().strip()
            lado=float(area)
            resultado=lado*lado
            self.msj("Area de un cuadrado ", f"El resultado es {resultado} ")

        except ValueError:
            self.msj("Error", "Ingresa un numero")

    def msj(self, title, txt):
        m = QtWidgets.QMessageBox()
        m.setIcon(QtWidgets.QMessageBox.Information)
        m.setWindowTitle(title)
        m.setText(txt)
        m.exec_()

    def salir(self):
            QtWidgets.QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())