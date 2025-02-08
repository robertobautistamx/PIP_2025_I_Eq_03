import statistics
import sys
import os
from statistics import variance, stdev

import mean
from PyQt5 import uic, QtWidgets

qtCreatorFile = "Proyecto_Unidad1.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #ingresa los numeros
        self.btn_aceptar.clicked.connect(self.aceptar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Lista de numeros
        self.btn_reiniciar.clicked.connect(self.reiniciar)
        self.btn_calcular.clicked.connect(self.calcular)

        #Tendencia central y medidas de dispersion
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cargar.clicked.connect(self.cargar)

        self.btn_salir.clicked.connect(self.salir)

        self.numeros = []
        self.ruta_archivo="../Archivos/listaNumeros.csv"

    def aceptar(self):
        num_texto=self.txt_numero.text().strip()

        try:
            num=float(num_texto)
            self.numeros.append(num)
            self.txt_numero.clear()

            with open(self.ruta_archivo, "a") as archivo:
                archivo.write(f"{num}\n")
            self.mostrar_numeros()

        except ValueError:
            QtWidgets.QMessageBox.warning(self, "ERROR", "Ingresa un numero valido")

    #ListaNumeros (CUADRO)
    def mostrar_numeros(self):
        try:
            archivo=open(self.ruta_archivo)
            contenido=archivo.readlines()
            archivo.close()

            nums=[]
            for i in contenido:
                nums.append(float(i.strip()))
            self.txt_listaNumeros.setText(str(self.numeros))

        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "ERROR", "El archivo no existe.")
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "ERROR", "El archivo contiene datos inválidos.")

    def cancelar(self):
         self.numeros.pop()
         self.txt_numero.clear()
         self.mostrar_numeros()
         self.msj("correcto", f"Ultimo numero eliminado")


    def reiniciar(self):
        self.numeros=[]
        self.txt_listaNumeros.clear()
        self.txt_media.clear(), self.txt_mediana.clear(), self.txt_moda.clear()
        self.txt_valorMenor.clear(), self.txt_valorMayor.clear(), self.txt_varianza.clear(), self.txt_desviacionEstandar.clear()
        self.msj("Correcto", f"Lista reiniciada...")

    def calcular(self):
        #Tendencia central
        media=statistics.mean(self.numeros) #CALCULA LA MEDIA ARITMETICA
        self.txt_media.setText(str(media))

        mediana=statistics.median(self.numeros) #cacula mediana
        self.txt_mediana.setText(str(mediana))

        moda=statistics.mode(self.numeros) #CALCULA LA MODA
        self.txt_moda.setText(str(moda))

        #Medidas de dispersion
        valorMenor1=min(self.numeros)
        self.txt_valorMenor.setText(str(valorMenor1))

        valorMayor1=max(self.numeros)
        self.txt_valorMayor.setText(str(valorMayor1))

        varianza=variance(self.numeros)
        self.txt_varianza.setText(str(varianza))

        desviacionE=stdev(self.numeros)
        self.txt_desviacionEstandar.setText(str(desviacionE))
        self.msj("Correcto", f"Valores calculados.")

    def guardar(self):
        archivo = open("../Archivos/resultadosAnalisis.csv", "w")  # "w"=write (escritura / "a" = append
        for num in self.numeros:
            archivo.write(str(num) + "\n")
        archivo.flush()
        archivo.close()
        self.msj("Correcto", f"Archivo guardado correctamente.")

    def cargar(self):
        archivo = open("../Archivos/resultadosAnalisis.csv")
        contenido = archivo.readlines()  # lee el archivo completo

        nums=[]
        for i in contenido:
            nums.append(float(i))

        print(nums)
        self.numeros=nums
        self.txt_listaNumeros.setText(str(self.numeros))
        self.calcular()
        self.msj("Correcto", f"Archivo cargado.")

    def salir(self):
        self.close()

    def msj(self, title, txt):
        m = QtWidgets.QMessageBox()
        m.setIcon(QtWidgets.QMessageBox.Information)
        m.setWindowTitle(title)
        m.setText(txt)
        m.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
