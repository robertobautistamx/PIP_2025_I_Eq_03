import math
import sys
from PyQt5 import uic, QtWidgets

qtCreatorFile = "E01_Ejercicio1.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_calcular.clicked.connect(self.calcular)
        self.btn_salir.clicked.connect(self.salir)

    def calcular(self):
        try:
            x1_text=self.txt_x1.text().strip()
            y1_text=self.txt_y1.text().strip()
            x2_text=self.txt_x2.text().strip()
            y2_text=self.txt_y2.text().strip()

            if not self.es_numero(x1_text) or not self.es_numero(y1_text) or not self.es_numero(x2_text) or not self.es_numero(y2_text):
                self.msj("Error", "Por favor, ingresa numeros validos.")
                return

            x1=float(x1_text)
            y1=float(y1_text)
            x2=float(x2_text)
            y2=float(y2_text)

            distancia=math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            self.txt_resultado.setText(f"{distancia:.2f}")
        except Exception as e:
            self.msj("Error", f"Ocurrió un error: {str(e)}")

    def es_numero(self, texto):
        try:
            float(texto)
            return True
        except ValueError:
            return False

    def msj(self, titulo, mensaje):
        m = QtWidgets.QMessageBox()
        m.setIcon(QtWidgets.QMessageBox.Information)
        m.setWindowTitle(titulo)
        m.setText(mensaje)
        m.exec_()

    def salir(self):
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
