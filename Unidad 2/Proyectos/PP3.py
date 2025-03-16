import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTimer

qtCreatorFile = "PP3.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.ocultar_imagenes()

        self.secuencia_computadora=[]
        self.secuencia_usuario=[]
        self.puntaje=0
        self.actualizar_puntaje()

        # Botones
        self.btn_iniciar.clicked.connect(self.iniciar)
        self.btn_reiniciar.clicked.connect(self.reiniciar)
        self.btn_salir.clicked.connect(self.salir)

        # Clic en las imágenes
        self.gato.clicked.connect(lambda: self.boton_click("gato"))
        self.perro.clicked.connect(lambda: self.boton_click("perro"))
        self.hamster.clicked.connect(lambda: self.boton_click("hamster"))
        self.conejo.clicked.connect(lambda: self.boton_click("conejo"))

    def iniciar(self):
        print("JUEGO INICIADO")
        QtWidgets.QMessageBox.warning(self, "Recuerda y GANA", "Juego comienza en 3 ... 2 ... 1 ... GO")
        self.secuencia_computadora=[]
        self.secuencia_usuario=[]
        self.nueva_secuencia()

    def reiniciar(self):
        print("Reiniciando juego...")
        self.secuencia_computadora=[]
        self.secuencia_usuario=[]
        self.ocultar_imagenes()
        self.btn_iniciar.setEnabled(True)
        self.puntaje=(0)
        self.actualizar_puntaje()
        QtWidgets.QMessageBox.warning(self, "BIEN", "JUEGO REINICIADO")

    def salir(self):
        self.close()

    def ocultar_imagenes(self):
        self.gato.setStyleSheet("border-image: none;")  #esconde la imagen (none)
        self.perro.setStyleSheet("border-image: none;")
        self.hamster.setStyleSheet("border-image: none;")
        self.conejo.setStyleSheet("border-image: none;")

    def mostrar_imagen(self, imagen):
        if imagen=="gato":
            self.gato.setStyleSheet("border-image: url(:/Imagenes/images.jpeg);")
        elif imagen=="perro":
            self.perro.setStyleSheet("border-image: url(:/Imagenes/cachorro.jpg);")
        elif imagen=="hamster":
            self.hamster.setStyleSheet("border-image: url(:/Imagenes/Goldhamster_terrarium.jpg);")
        elif imagen=="conejo":
            self.conejo.setStyleSheet("border-image: url(:/Imagenes/conejo.jpeg);")

    def nueva_secuencia(self):
        self.ocultar_imagenes()
        self.secuencia_computadora.append(self.obtener_imagen_aleatoria()) #imagen aleatoria
        print("Secuencia de la computadora:", self.secuencia_computadora)
        self.mostrar_secuencia_computadora(0) #lo muestra al usuario

    def obtener_imagen_aleatoria(self):
        import random
        return random.choice(["gato", "perro", "hamster", "conejo"]) #imagenes existentes en el qt designer

    def mostrar_secuencia_computadora(self, index):
        if index<len(self.secuencia_computadora):
            imagen=self.secuencia_computadora[index]

            self.mostrar_imagen(imagen)  #mostrar imagen
            QTimer.singleShot(1000, self.ocultar_imagenes)  #1segundo de espera
            QTimer.singleShot(1500, lambda: self.mostrar_secuencia_computadora(index+1)) #sig imagen

        else:
            print("Secuencia completada. Ahora es tu turno.")
            self.secuencia_usuario=[] #reiniciar secuencia
            self.btn_iniciar.setEnabled(False)

    def boton_click(self, imagen):
        #validar secuencia del usuario

        if len(self.secuencia_usuario)<len(self.secuencia_computadora):
            self.secuencia_usuario.append(imagen)
            print("Secuencia del usuario:", self.secuencia_usuario)

            #si la secuencia del usuario es correcta hasta ahora
            if self.secuencia_usuario==self.secuencia_computadora[:len(self.secuencia_usuario)]:
                if len(self.secuencia_usuario)==len(self.secuencia_computadora):
                    print("¡Secuencia correcta!")
                    self.secuencia_usuario=[] #reiniciar/repetir
                    self.puntaje+=1  #puntaje incrementa 1+
                    self.actualizar_puntaje()

                    QTimer.singleShot(1000, self.nueva_secuencia)  #break de 1segundos antes de mostyrar la nueva secuencia
            else:
                print("¡Secuencia incorrecta! Perdiste.")
                QtWidgets.QMessageBox.warning(self, "Perdiste:(", "Rayos, has perdido el juego :(")
                self.reiniciar()

    def actualizar_puntaje(self):
        self.puntaje_textedit.setPlainText(f"Puntaje: {self.puntaje}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
