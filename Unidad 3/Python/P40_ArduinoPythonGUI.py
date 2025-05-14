import sys
from PyQt5 import uic, QtWidgets, QtCore
import serial as placa


qtCreatorFile = "P40_ArduinoPythonGUI.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los Signals
        # poner 3 en el cuadro


        self.arduino = None
        self.btn_accion.clicked.connect(self.accion)

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturas)

        self.btn_control.clicked.connect(self.control)


    # Área de los Slots
    def control(self):
     if self.arduino.isOpen():
        texto = self.btn_control.text()
        if texto == "PRENDER":
            self.btn_control.setText("APAGAR")
            self.arduino.write("1".encode())
        else:
            self.btn_control.setText("PRENDER")
            self.arduino.write("0".encode())

    def lecturas(self):
        if self.arduino.isOpen():
            if self.arduino.inWaiting():
                lectura = self.arduino.readline().decode().strip()
                if lectura !="":
                  print(lectura) #marca error sin el
                  ######
                  #PROCESAMIENTO DE LOS DATOS
                  lectura = lectura.split("@")
                  lectura = lectura[:-1]

                  lectura =[int(i) for i in lectura]


                  #####
                  # self.lista_datos.addItem(str(lectura))
                  # self.lista_datos.setCurrentRow(self.lista_datos.count()-1)
                  self.lista_datos.addItem(str(lectura[0]))
                  self.lista_datos.setCurrentRow(self.lista_datos.count() - 1)
                  self.lista_datos2.addItem(str(lectura[1]))
                  self.lista_datos2.setCurrentRow(self.lista_datos2.count() - 1)
                  self.lista_datos3.addItem(str(lectura[2]))
                  self.lista_datos3.setCurrentRow(self.lista_datos3.count() - 1)
                  self.lista_datos4.addItem(str(lectura[3]))
                  self.lista_datos4.setCurrentRow(self.lista_datos4.count() - 1)


    def accion(self):
        try:
            texto = self.btn_accion.text()
            if texto == "CONECTAR": #Inicia la comunicacion y la apertura
                com = "COM3" + self.txt_com.text() #quitar el 3
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("CONECTADO")
                self.arduino = placa.Serial(com,baudrate=9600,timeout=1)
                self.segundoPlano.start(100)

            elif texto == "DESCONECTAR": #cierra la comunicacion
                self.btn_accion.setText("RECONECTAR")
                self.txt_estado.setText("DESCONECTADO")
                self.segundoPlano.stop()
                self.arduino.close()

            else: #Reapertura comunicacion
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("RECONECTADO")
                self.arduino.open()
                self.segundoPlano.start(100)
        except Exception as error:
            print(error)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

    # cd Archivos,  una vez en el proyecto
    # pyrcc5 Recursos.qrc -o Recursos_rc.py
    # Los archivos generados siempre son nombre_rc.py,  en caso de problema ponerle ese nombre y pasarlo a la misma carpeta el .py
