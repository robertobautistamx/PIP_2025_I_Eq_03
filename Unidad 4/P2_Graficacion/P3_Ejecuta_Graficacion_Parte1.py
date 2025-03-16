import sys
from PyQt5 import uic, QtWidgets

import Plantilla_Grafica as interfaz
import matplotlib.pyplot as plt

class MyApp(QtWidgets.QMainWindow, interfaz.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        interfaz.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los Signals

        self.btn_graficar.clicked.connect(self.graficar)

        #Valores por defecto:
        self.configuraciones= {
            "Estilo": ":",
            "color_linea":"black",
            "ancho_linea":1
        }

        self.limites={
            "x": [1,10,10], #min, max, divisiones
            "y": [1, 10,10] #min, max, divisiones
        }

    # Área de los Slots
    def graficar(self):
        polinomio=self.txt_polinomio.text()
        polinomio=polinomio.replace("^","**")

        #tabular ... valores de x con base en los cuales pueda obtener los valores
        X=[i for i in range(self.limite["x"][0], self.limite["x"][1])] #lista de compresion
        print ("valores de x: ")
        print(X)

        y=[eval(polinomio.replace("x","*("+str(x)+")")) for x in X]
        print("valores de y: ")
        print (y)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())