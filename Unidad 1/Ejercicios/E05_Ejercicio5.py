import sys
from PyQt5 import uic, QtWidgets

qtCreatorFile = "E05_Ejercicio5.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_aceptar.clicked.connect(self.aceptar)
        self.btn_salir.clicked.connect(self.salir)

    # slots
    def aceptar(self):
        try:
            edad1=self.txt_edad.text().strip()

            edad = int(edad1)
            if edad>=18:
                self.msj("Resultado", "Eres mayor de edad")
            else:
                self.msj("Resultado", "Eres menor de edad")

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
