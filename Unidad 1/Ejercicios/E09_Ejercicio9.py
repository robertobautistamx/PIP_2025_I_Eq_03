import sys
from datetime import datetime, timedelta
from PyQt5 import uic, QtWidgets
import re

qtCreatorFile = "E09_Ejercicio9.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_calcular.clicked.connect(self.calcular)
        self.btn_salir.clicked.connect(self.salir)

        # slots
    def calcular(self):
        try:
            numero_texto = self.txt_numero.text().strip()
            if not numero_texto.isdigit():
                self.msj("Error", "Por favor ingresa un número entero positivo.")
                return

            numero = int(numero_texto)
            resultado = self.factorial(numero)

            self.txt_resultado.setText(f" {resultado}")
        except Exception as e:
            self.msj("Error", f"Ocurrió un error: {str(e)}")

    def factorial(self, n):
        if n==0 or n==1:
            return 1
        factorial = 1
        for i in range(2,n+1):
            factorial*=i
        return factorial

    def salir(self):
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
