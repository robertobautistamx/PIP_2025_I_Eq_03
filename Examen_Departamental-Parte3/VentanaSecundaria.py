
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile3 = "Second_RecepcionInfo.ui"  # Nombre del archivo aquí.
Ui_dialog, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)


class MyDialog(QtWidgets.QDialog, Ui_dialog):
    def __init__(self,  rPrincipal):
        QtWidgets.QDialog.__init__(self)
        Ui_dialog.__init__(self)
        self.setupUi(self)

        # Área de los Signals / Configuracion
        self.acceso = rPrincipal
        self.Baceptar.clicked.connect(self.Aceptar)
        self.Tnombre.setText(self.acceso.NombreArchivo)



    # Área de los Slots
    def Aceptar(self):

        self.acceso.NombreArchivo = self.Tnombre.text()
        print(self.acceso.NombreArchivo)
        self.accept()  # <- importante, para que el exec_() en Guardar() sepa que se aceptó
