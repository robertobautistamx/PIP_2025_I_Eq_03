import sys
from PyQt5 import uic, QtWidgets

qtCreatorFile = "E07_Ejercicio7.ui"  # Nombre del archivo aquí.
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
            palabra = self.txt_palabra.text().strip()

            if palabra:
                num_caracteres=len(palabra)
                mensaje=(
                    f"Texto ingresado: {palabra}\n"
                    f"Cantidad de caracteres: {num_caracteres}\n"
                )
                self.msj("Resultado", mensaje)
            else:
                self.msj("Error", "Por favor ingresa una cadena de texto.")
        except Exception as e:
            self.msj("Error", f"Ocurrió un error")

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
