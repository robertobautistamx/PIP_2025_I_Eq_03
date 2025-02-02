import sys
from PyQt5 import uic, QtWidgets
qtCreatorFile = "P07_SumaDeMultiplesNumeros.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.btn_agregar.clicked.connect(self.agregar)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cargar.clicked.connect(self.cargar)
        self.numeros=[] #lista vacia, que puede ser utilizada en cualquier parte de la

    #slots
    def cargar(self):
        archivo = open("../Archivos/numeros.csv")
        contenido=archivo.readlines()#lee el archivo completo
        print(contenido)
       # nums=[float(i) for i in contenido]
        ##################
        nums=[]
        for i in contenido:
            nums.append(float(i))
        ###################
        print(nums)
        self.numeros=nums
        self.sumar()


    def agregar(self):
        num=float(self.txt_numero.text())
        self.numeros.append(num)
        self.sumar()

    def guardar(self):
        archivo=open("../Archivos/numeros.csv","w") #"w"=write (escritura / "a" = append
        for num in self.numeros:
            archivo.write(str(num)+ "\n")
        archivo.flush()
        archivo.close()

    def sumar(self):
        sumaaa=sum(self.numeros)
        self.txt_suma.setText(str(sumaaa))

    def msj(self, txt):
        m = QtWidgets.QMessageBox()
        m.setText(txt)
        m.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())