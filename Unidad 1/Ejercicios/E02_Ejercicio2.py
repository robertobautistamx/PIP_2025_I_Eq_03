import sys

from PyQt5 import uic, QtWidgets
qtCreatorFile = "E02_Ejercicio2.ui"  # Nombre del archivo aquí.
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
            entrada=self.txt_A.text().strip()
            numero=int(entrada)
            if numero%2==0:
                self.msj("Resultado", f"El número {numero} es par.")
            else:
                self.msj("Resultado", f"El número {numero} es impar.")
        except ValueError:
            self.msj("Error", "Ingresa un numero valido")

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