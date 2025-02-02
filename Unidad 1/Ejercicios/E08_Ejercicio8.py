import sys
from datetime import datetime, timedelta
from PyQt5 import uic, QtWidgets
import re

qtCreatorFile = "E08_Ejercicio8.ui"  # Nombre del archivo aquí.
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
            hA = self.txt_horaActual.text().strip()

            # Validar el formato de la hora actual con una expresión regular
            if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", hA):
                self.msj("Error", "Por favor ingresa una hora válida en formato HH:MM (24 horas).")
                return

            # Convertir hora actual a un objeto datetime
            hora_actual = datetime.strptime(hA, "%H:%M")

            final_del_dia = datetime.strptime("23:59", "%H:%M")  # Última hora del día
            horas_restantes = final_del_dia - hora_actual

            # Obtener el número de horas restantes
            horas_restantes_en_horas = horas_restantes.total_seconds() / 3600  # Convertir a horas
            mensaje = f"Quedan {horas_restantes_en_horas:.2f} horas."

            self.txt_resultado.setText(mensaje)
        except Exception as e:
            self.msj("Error", f"Ocurrió un error: {str(e)}")

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
