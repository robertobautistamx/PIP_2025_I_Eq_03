import os
import sys
import serial
from PyQt5 import uic, QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import VentanaSecundaria

qtCreatorFile = "Examen_Depa.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.CBpuertos.addItems(["COM3", "COM4", "COM5", "COM6"])
        self.Bconectar.clicked.connect(self.conectar)
        self.Bactuador1.clicked.connect(self.actuador)
        self.Bmostrar1.clicked.connect(self.AlternarBoton)
        self.Bguardar1.clicked.connect(self.Guardar)

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturas)

        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 100)
        self.linea, = self.ax.plot([], [], color='blue')
        self.x_data = []
        self.y_data = []
        self.max_puntos = 50
        self.QVcanvas1.addWidget(self.canvas)

    def conectar(self):
        try:
            if self.Bconectar.text() == "CONECTAR":
                puerto = self.CBpuertos.currentText()
                self.arduino = serial.Serial(puerto, baudrate=9600, timeout=1)
                self.segundoPlano.start(500)
                self.Bconectar.setText("DESCONECTAR")
            else:
                self.segundoPlano.stop()
                self.arduino.close()
                self.Bconectar.setText("CONECTAR")
        except Exception as e:
            print("Error al conectar:", e)

    def lecturas(self):
        try:
            if self.arduino.inWaiting():
                lectura = self.arduino.readline().decode().strip()

                if lectura.startswith("Distancia:"):
                    if self.Bmostrar1.text() == "APAGAR":
                        partes = lectura.split(" ")
                        distancia = int(partes[1])
                        print(f"Distancia: {distancia}")
                        self.lista_datos1.addItem(str(distancia))
                        self.lista_datos1.setCurrentRow(self.lista_datos1.count() - 1)
                        self.actualizar_grafica(distancia)

                        if distancia<10 and self.Bactuador1.isEnabled():
                            print("Distancia menor a 10: activando actuador...")
                            self.actuador(desde_timer=True)
        except Exception as e:
            print("Error en lectura:", e)

    def actualizar_grafica(self, valor):
        self.y_data.append(valor)
        if len(self.y_data)>self.max_puntos:
            self.y_data.pop(0)
        self.x_data=list(range(len(self.y_data)))
        self.linea.set_data(self.x_data, self.y_data)
        self.ax.set_xlim(0, self.max_puntos)
        self.ax.set_ylim(0, 100)
        self.canvas.draw()

    def actuador(self, desde_timer=False):
        try:
            print("activando actuador...")

            if self.Bconectar.text()!="DESCONECTAR":
                print("No está conectado al puerto COM.")
                return

            if desde_timer:
                print("Deteccion de 10 cm...")
                boton=self.Bactuador1
            else:
                boton=self.sender()
                print(f"Boton presionado: {boton.objectName()}")
            boton.setEnabled(False)
            if boton==self.Bactuador1:
                indice=0
                valor=1000
            else:
                print("Botón no válido")
                return

            comando=f"{indice}@{valor}\n"
            print(f"Enviando comando: {comando}")
            self.arduino.write(comando.encode())
            self.arduino.flush()

            QtCore.QTimer.singleShot(2000, lambda: self.reactivar_boton(boton))
        except Exception as e:
            print("Error al activar el actuador:", e)

    def reactivar_boton(self, boton):
        boton.setEnabled(True)

    def AlternarBoton(self):
        boton=self.sender()
        texto=boton.text()
        if texto=="PRENDER":
            boton.setText("APAGAR")
        else:
            boton.setText("PRENDER")

    def Guardar(self):
        try:
            self.resetear_botones()
            boton=self.sender()
            carpeta_guardado="Archivos_Guardados"
            if not os.path.exists(carpeta_guardado):
                os.makedirs(carpeta_guardado)

            if boton==self.Bguardar1:
                self.NombreArchivo="MedidorDistancias"
            lista_origen=self.lista_datos1
            texto_inicial="Lecturas del sensor\n"

            self.dialogo=VentanaSecundaria.MyDialog(self)
            resultado=self.dialogo.exec_()

            if resultado==QtWidgets.QDialog.Accepted:
                ruta_archivo=os.path.join(carpeta_guardado, self.NombreArchivo + ".txt")
                with open(ruta_archivo, 'w') as archivo:
                    archivo.write(texto_inicial)
                    for i in range(lista_origen.count()):
                        dato=lista_origen.item(i).text()
                        archivo.write(dato+'\n')
        except Exception as error:
            print("Error al guardar el archivo:", error)

    def resetear_botones(self):
        self.Bmostrar1.setText("PRENDER")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())