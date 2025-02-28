import sys
from PyQt5 import uic, QtWidgets
import random
import Recursos_rc
qtCreatorFile = "E09_Ejercicio9.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.numero_secreto = random.randint(1, 10)

        # Área de los Signals
        self.btn_adivinar.clicked.connect(self.adivinar)
        self.btn_reiniciar.clicked.connect(self.reiniciar)
        self.btn_salir.clicked.connect(self.salir)

    # Área de los Slots
    def adivinar(self):
        try:
            numero = int(self.txt_numero.text())

            if numero < self.numero_secreto:
                self.txt_resultado.setText("Demasiado bajo. Intenta de nuevo.")
            elif numero > self.numero_secreto:
                self.txt_resultado.setText("Demasiado alto. Intenta de nuevo.")
            else:
                self.txt_resultado.setText("¡Felicidades! Has adivinado el numero.")
        except ValueError:
            self.msj("Error... Ingresa un numero válido.")

    def reiniciar(self):
        self.txt_numero.clear()
        self.txt_resultado.clear()

    def salir(self):
        self.close()

    def msj(self, txt):
        m = QtWidgets.QMessageBox()
        m.setText(txt)
        m.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())