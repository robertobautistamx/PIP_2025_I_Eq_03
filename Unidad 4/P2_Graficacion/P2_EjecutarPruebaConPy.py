import sys
from PyQt5 import uic, QtWidgets
#qtCreatorFile = "Plantilla_Grafica.ui"  # Nombre del archivo aquí.
#Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

import P1_EjecutarPrueba as interfaz
class MyApp(QtWidgets.QMainWindow, interfaz.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        interfaz.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los Signals

    # Área de los Slots
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())