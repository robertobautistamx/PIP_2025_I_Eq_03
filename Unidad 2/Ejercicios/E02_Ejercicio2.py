import sys
from PyQt5 import uic, QtWidgets
import Recursos_rc
qtCreatorFile = "E02_Ejercicio2.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los Signals
        self.btn_calcular.clicked.connect(self.calcular)
        self.btn_reiniciar.clicked.connect(self.reiniciar)
        self.btn_salir.clicked.connect(self.salir)

    # Área de los Slots
    def calcular(self):
        try:
            hora = int(self.txt_horas.text())
            minuto = int(self.txt_minutos.text())

            if not (0 <= hora < 24 and 0 <= minuto < 60):
                raise ValueError("Hora fuera de rango")

            segundos_totales = (hora * 3600) + (minuto * 60)
            self.txt_resultado.setText("{:,}".format(segundos_totales))
        except ValueError:
            self.msj("Error... Ingresa valores numéricos válidos.")

    def reiniciar(self):
        self.txt_horas.clear()
        self.txt_minutos.clear()
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