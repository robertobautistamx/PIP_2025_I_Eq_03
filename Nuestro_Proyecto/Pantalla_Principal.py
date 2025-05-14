import os

import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import serial as placa, random
import VentanaSecundaria
import VentanaConfiguracion

qtCreatorFile = "Pantalla_Principal.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Puertos en el comboBox
        puertos_comunes = ["COM3", "COM4", "COM5", "COM6", "COM7", "COM8"]
        self.CBpuertos.addItems(puertos_comunes)


        # Área de los Signals

        #Desactivar los datos falsos cuando se usen los sensores
        self.arduino = None
        self.Bconectar.clicked.connect(self.conectar)
        #self.Bconectar.clicked.connect(self.conectar_fake)

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturas)
        #self.segundoPlano.timeout.connect(self.lecturas_fake)
        #-------------------------------------------------------------
        self.RBpagina1.setChecked(True)
        self.RBpagina1.toggled.connect(self.cambiar_pagina)
        self.RBpagina2.toggled.connect(self.cambiar_pagina)
        self.RBpagina3.toggled.connect(self.cambiar_pagina)

        self.Bmostrar1.clicked.connect(self.AlternarBoton)
        self.Bmostrar2.clicked.connect(self.AlternarBoton)
        self.Bmostrar3.clicked.connect(self.AlternarBoton)
        self.Bguardar1.clicked.connect(self.Guardar)
        self.Bguardar2.clicked.connect(self.Guardar)
        self.Bguardar3.clicked.connect(self.Guardar)
        self.Bactuador1.clicked.connect(self.actuador)
        self.Bactuador2.clicked.connect(self.actuador)
        self.Bactuador3.clicked.connect(self.actuador)
        self.Bconfiguracion.clicked.connect(self.AbrirConfiguracion)

        self.configuracion_modos = [] #3
        self.configuracion_valores = [] #3



        #_____________________________________
        # Área de las gráficas
        self.figuras = []
        self.ejes = []
        self.canvases = []
        self.x_datas = []
        self.y_datas = []

        self.max_puntos = 50
        self.lineas = []
        colores = ['blue', 'purple', 'red']
        self.limitesY = [50, 1023, 400] #Valores esperados: 0-50 grados celsius, 0-1023 de luz, y  0-400 cm de distancia aunque suele ser menor a 300 cm.
        # ejemplo: 23@845@56
        for i in range(3):
            fig = Figure()
            ax = fig.add_subplot(111)
            ax.set_xlim(0, self.max_puntos) #Eje X, 50 valores mostrados al mismo tiempo
            ax.set_ylim(0, self.limitesY[i] ) # rango de valores de los sensores
            canvas = FigureCanvas(fig)

            linea, = ax.plot([], [], color=colores[i])

            self.figuras.append(fig)
            self.ejes.append(ax)
            self.canvases.append(canvas)
            self.x_datas.append([])
            self.y_datas.append([])
            self.lineas.append(linea)

        # Agregamos a cada widget su gráfica correspondiente
        self.QVcanvas1.addWidget(self.canvases[0])
        self.QVcanvas2.addWidget(self.canvases[1])
        self.QVcanvas3.addWidget(self.canvases[2])
        #________________________________________

    # Área de los Slots
    def Guardar(self):
     try:
        self.resetear_botones() #Capaz algun otro metodo que detenga el timer o la recepcion de los sensores
        boton = self.sender()
        carpeta_guardado = "Archivos_Guardados"
        if not os.path.exists(carpeta_guardado):
            os.makedirs(carpeta_guardado)

        # Definir nombre según botón
        if boton == self.Bguardar1:
            self.NombreArchivo = "Datos_riego"
            lista_origen = self.lista_datos1
            texto_inicial = "Lecturas del sensor temperatura y humedad:\n"
        elif boton == self.Bguardar2:
            self.NombreArchivo = "Datos_luz"
            lista_origen = self.lista_datos2
            texto_inicial = "Lecturas de sensor de la fotoresistencia:\n"
        else:
            self.NombreArchivo = "Datos_alarma"
            lista_origen = self.lista_datos3
            texto_inicial = "Lecturas del sensor de distnacias:\n"


        # Abrir diálogo secundario de forma modal (bloqueante)
        self.dialogo = VentanaSecundaria.MyDialog(self)
        resultado = self.dialogo.exec_()  # Bloquea aquí hasta cerrar

        if resultado == QtWidgets.QDialog.Accepted:
            ruta_archivo = os.path.join(carpeta_guardado, self.NombreArchivo + ".txt")

            with open(ruta_archivo, 'w') as archivo:
                archivo.write(texto_inicial)
                for i in range(lista_origen.count()):
                    dato = lista_origen.item(i).text()
                    archivo.write(dato + '\n')

     except Exception as error:
        print("Error al guardar el archivo:", error)


    def actualizar_grafica(self, numero_grafica, nuevo_valor):
        print("num ",numero_grafica )
        ax = self.ejes[numero_grafica]
        canvas = self.canvases[numero_grafica]
        y_data = self.y_datas[numero_grafica]
        linea = self.lineas[numero_grafica]

        y_data.append(nuevo_valor) # Agrega el nuevo valor a la lista de datos
        if len(y_data) > self.max_puntos: #Si ya son 50, se quita el primero para agregar el nuevo como el 50
            y_data.pop(0)

        x_data = list(range(len(y_data)))

        # Actualiza los datos de la línea, vuelve a dibujar los elementos de la gráfica, del 0 al 50 de la lista
        linea.set_data(x_data, y_data)

        # Actualiza los límites
        ax.set_xlim(0, self.max_puntos)
        ax.set_ylim(0, self.limitesY[numero_grafica])
        canvas.draw()

    def conectar_fake(self):
        texto = self.Bconectar.text()
        if texto == "CONECTAR":
            self.segundoPlano.start(100)
            self.Bconectar.setText("DESCONECTAR")
        elif texto == "DESCONECTAR":
            self.segundoPlano.stop()
            self.Bconectar.setText("RECONECTAR")
        else:
            self.segundoPlano.start(100)
            self.Bconectar.setText("DESCONECTAR")

    def lecturas_fake(self):
        # Simular una lectura tipo 23@845@56
        valores = [
            random.randint(0, 50),  # Temperatura
            random.randint(0, 1023),  # Luz
            random.randint(0, 300)  # Distancia
        ]
        lectura_str = "@".join(str(v) for v in valores) + "@"
        print(lectura_str)
        self.lectura = lectura_str.split("@")[:-1]
        print(self.lectura)
        self.lectura = [int(i) for i in self.lectura if i.strip().isdigit()]
        if self.Bmostrar1.text() == "APAGAR":
            valor = self.lectura[0]
            self.lista_datos1.addItem(str(valor))
            self.lista_datos1.setCurrentRow(self.lista_datos1.count() - 1)
            self.actualizar_grafica(0, valor)
        if self.Bmostrar2.text() == "APAGAR":
            valor = self.lectura[1]
            self.lista_datos2.addItem(str(valor))
            self.lista_datos2.setCurrentRow(self.lista_datos2.count() - 1)
            self.actualizar_grafica(1, valor)
        if self.Bmostrar3.text() == "APAGAR":
            valor = self.lectura[2]
            self.lista_datos3.addItem(str(valor))
            self.lista_datos3.setCurrentRow(self.lista_datos3.count() - 1)
            self.actualizar_grafica(2, valor)


    def lecturas(self):
        if self.arduino.isOpen():
            if self.arduino.inWaiting():
                self.lectura = self.arduino.readline().decode().strip()
                if self.lectura != "":
                    print(self.lectura)  # marca error sin el
                    ######
                    # PROCESAMIENTO DE LOS DATOS
                    self.lectura = self.lectura.split("@")
                    self.lectura = self.lectura[:-1]
                    print(self.lectura)  # marca error sin el
                    self.lectura = [int(i) for i in self.lectura if i.strip().isdigit()] #esto devuelve una lista de int
                    #####
                    if self.Bmostrar1.text() == "APAGAR":
                        valor = self.lectura[0]
                        self.lista_datos1.addItem(str(valor))
                        self.lista_datos1.setCurrentRow(self.lista_datos1.count() - 1)
                        self.actualizar_grafica(0, valor)

                    if self.Bmostrar2.text() == "APAGAR":
                        valor = self.lectura[1]
                        self.lista_datos2.addItem(str(valor))
                        self.lista_datos2.setCurrentRow(self.lista_datos2.count() - 1)
                        self.actualizar_grafica(1, valor)

                    if self.Bmostrar3.text() == "APAGAR":
                        valor = self.lectura[2]
                        self.lista_datos3.addItem(str(valor))
                        self.lista_datos3.setCurrentRow(self.lista_datos3.count() - 1)
                        self.actualizar_grafica(2, valor)
        else:
            print("Arduino no conectado")

    def conectar(self):
        try:
            texto = self.Bconectar.text()
            if texto == "CONECTAR": #Inicia la comunicacion y la apertura
                com = self.CBpuertos.currentText()
                self.arduino = placa.Serial(com,baudrate=9600,timeout=1)
                self.segundoPlano.start(100)
                self.Bconectar.setText("DESCONECTAR")

            elif texto == "DESCONECTAR": #cierra la comunicacion
                self.Bconectar.setText("RECONECTAR")
                self.segundoPlano.stop()
                self.arduino.close()

            else: #Reapertura comunicacion
                self.Bconectar.setText("DESCONECTAR")
                self.arduino.open()
                self.segundoPlano.start(100)
        except Exception as error:
            print(error)

    def AlternarBoton(self):
        boton = self.sender()
        texto = boton.text()
        if texto == "PRENDER":
            boton.setText("APAGAR")
        else:
            boton.setText("PRENDER")

    def resetear_botones(self):
        self.Bmostrar1.setText("PRENDER")
        self.Bmostrar2.setText("PRENDER")
        self.Bmostrar3.setText("PRENDER")

    def cambiar_pagina(self):
        try:
            boton = self.sender()
            if boton == self.RBpagina1:
                self.Stacked_paginas.setCurrentIndex(0)
                self.resetear_botones()
            elif boton == self.RBpagina2:
                self.Stacked_paginas.setCurrentIndex(1)
                self.resetear_botones()
            elif boton == self.RBpagina3:
                self.Stacked_paginas.setCurrentIndex(2)
                self.resetear_botones()
        except Exception as e:  print("Error en cambiar_pagina:", e)

    def actuador(self):
        try:
            if self.Bconectar.text() != "DESCONECTAR":
                return  # No se hace nada si no está conectado
            boton = self.sender()  # Detectamos qué botón se presionó

            # Desactivar el botón para evitar múltiples presiones
            boton.setEnabled(False)
            if boton == self.Bactuador1:  # Activar servomotor
                indice = 0
                valor = 1000 #1000 milisegundos
            elif boton == self.Bactuador2:  # Activar/Desactivar LED
                indice = 1
                if boton.text() == "Activar actuador":
                    valor = 1
                    boton.setText("Desactivar actuador")
                else:
                    valor = 0
                    boton.setText("Activar actuador")
            elif boton == self.Bactuador3:  # Activar alarma
                indice = 2
                valor = 500 # 500 milisegundos
            else:
                return  # No es un botón válido

            comando = f"{indice}@{valor}\n"
            self.arduino.write(comando.encode())
            self.arduino.flush()
            # Rehabilitar el botón después de un tiempo (por ejemplo, 2 segundos)
            QtCore.QTimer.singleShot(2000, lambda: self.reactivar_boton(boton))  # 2000 ms = 2 segundos
        except Exception as e:
            print("Error al activar el actuador:", e)

    def reactivar_boton(self, boton):
        # print("Reactivando botón...")
        boton.setEnabled(True)

    def AbrirConfiguracion(self):
        try:
            self.ventana_config = VentanaConfiguracion.MyDialog(self)
            resultado = self.ventana_config.exec_()

            if resultado == QtWidgets.QDialog.Accepted:
                print("Cambios aceptados")
            else:
                print("Configuración cancelada")
        except Exception as e:
            print("Error al abrir configuración:", e)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


# cosas extras
# def guardar_preferencias(self): #al cerrar
#     try:
#         with open("config.txt", "w") as archivo:
#             archivo.write(f"temperatura:{self.temperatura_preferencia}\n")
#             archivo.write(f"iluminacion:{self.iluminacion_preferencia}\n")
#             archivo.write(f"distancia:{self.distancia_preferencia}\n")
#     except Exception as e:
#         print("Error al guardar preferencias:", e)

# def cargar_preferencias(self): #en init
#     # Valores por defecto
#     self.temperatura_preferencia = 35
#     self.iluminacion_preferencia = 500
#     self.distancia_preferencia = 20
#     try:
#         with open("config.txt", "r") as archivo:
#             for linea in archivo:
#                 clave, valor = linea.strip().split(":")
#                 if clave == "temperatura":
#                     self.temperatura_preferencia = int(valor)
#                 elif clave == "iluminacion":
#                     self.iluminacion_preferencia = int(valor)
#                 elif clave == "distancia":
#                     self.distancia_preferencia = int(valor)
#     except FileNotFoundError:
#         print("Archivo de configuración no encontrado. Se usarán valores por defecto.")
#     except Exception as e:
#         print("Error al cargar preferencias:", e)

# def modo_automatico(self): #al timeout de segundo plano
#     if self.Bmodo.text() != "Automático":
#         return  # Solo actúa si el modo está activado
#
#     # Supón que ya tienes sensores leyendo valores como:
#     temp_actual = self.valor_temperatura
#     luz_actual = self.valor_iluminacion
#     dist_actual = self.valor_distancia
#
#     # Ejemplo de reacción automática
#     if dist_actual < self.distancia_preferencia:
#         print("¡Distancia baja! Activando alarma...")
#         comando = "2@1\n"  # Ejemplo: alarma ON
#         self.arduino.write(comando.encode())
#         self.arduino.flush()

