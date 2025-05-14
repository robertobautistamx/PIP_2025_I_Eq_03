
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile3 = "VentanaConfiguracion.ui"  # Nombre del archivo aquí.
Ui_dialog, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)


class MyDialog(QtWidgets.QDialog, Ui_dialog):
    def __init__(self,  rPrincipal):
        QtWidgets.QDialog.__init__(self)
        Ui_dialog.__init__(self)
        self.setupUi(self)

        # Área de los Signals / Configuracion
        self.acceso = rPrincipal
        self.Baceptar.clicked.connect(self.Aceptar)
        self.Brestablecer.clicked.connect(self.restablecer)


        # Área de los SpinBox, especificando el rango de valores de cada uno
        self.SB1.setRange(0, 50)   #temperatura en grados centigrados
        self.SB2.setRange(0, 1023) #nivel de iluminacion
        self.SB3.setRange(0, 300) #centimetros del sensor de distancia


    def restablecer(self):
        #SpinBox
        self.SB1.setValue(30)
        self.SB2.setValue(500)
        self.SB3.setValue(100)
        #Combobox
        self.CB1.setCurrentIndex(0)
        self.CB2.setCurrentIndex(0)
        self.CB3.setCurrentIndex(0)


    # Área de los Slots
    def Aceptar(self): #debera pasar los valores a las variables de la clase principal, deben estar definidas alla
        print("Holii")
        #self.acceso.variable = self.SB1.value()

