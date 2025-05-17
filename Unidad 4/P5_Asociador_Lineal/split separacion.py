import numpy as np
import random as rnd

def contar_clases(listaY):
    listaY = np.array(listaY)
    num_clases = listaY.shape[1] if len(listaY.shape) > 1 else 1
    conteo = [0] * num_clases
    for fila in listaY:
        for i in range(num_clases):
            if fila[i] == 1:
                conteo[i] += 1
                break  # asumiendo una sola clase activa por registro
    return conteo

# Cargar datos
archivo = open("Instancia_Restaurante.txt")
contenido = archivo.readlines()

# Se obtienen las entradas [ [Distancias:2 3	3	2	3	3, etc] , [Horas disponibles], [Precios], [Calificaciones], [Horas], [Num.Integrantes] ]
X = contenido[3:3+int(contenido[1])]
X = [i.strip().split("\t") for i in X]
X = [list(map(int, i)) for i in X]
#Se obtienen las salidas [ [El asador: 0,0,0,...,1,1,1,...,0,0,0], [[El lindero: 0,0,0,...,0,0,0,...,1,1,1], [Casa laguna: 1,1,1,...,0,0,0,...,0,0,0] ]
Y = contenido[3+int(contenido[1]):]
Y = [i.strip().split("\t") for i in Y]
Y = [list(map(int, i)) for i in Y]

X = np.array(X)
Y = np.array(Y)

print("X shape:", X.shape) #(atributos,registros) distancias[...60...],
print("Y shape:", Y.shape) #(clases,registros) El asador[...60...],

# División de datos
factorEntrenamiento = 0.8
num_total = X.shape[1]
regEntranamiento = int(factorEntrenamiento * num_total)
regPrueba = num_total - regEntranamiento
print("Registros entrenamiento:", regEntranamiento)
print("Registros prueba:", regPrueba)


#Proceso de seleccion, deben haber un balance en la cantidad de registros correspondientes a cada clase.
# En este caso  Entrenamiento [ 16 de clase1, 16 de clase2, 16 de clase3] y Prueba [ 4 de clase1, 4 de clase2, 4 de clase3]
#-----------------------------------------------------------------

# Selección aleatoria
datosEntrenamientoX = []
datosEntrenamientoY = []
datosPruebaX = []
datosPruebaY = []
# Crear copia
CX = [X[:, i] for i in range(X.shape[1])]
CY = [Y[:, i] for i in range(Y.shape[1])]


numero_clases = Y.shape[0] # 3 clases
numero_entrenamiento =  int (regEntranamiento / numero_clases)
numero_prueba = int(regPrueba / numero_clases)

# Selección entrenamiento: 16 rondas, un turno para cada clase (16 x 3 = 48 selecciones en total)
contador = 0
for ronda in range(numero_entrenamiento):
    for turno in range(numero_clases):
        while True:
            indice = rnd.randint(0, len(CY) - 1)
            if CY[indice][turno] == 1:
                datosEntrenamientoX.append(CX.pop(indice))
                datosEntrenamientoY.append(CY.pop(indice))
                contador += 1
                print("Seleccion (", contador,"/", numero_entrenamiento * numero_clases, ")")
                break
print("Datos de entrenamiento seleccionados")
# Selección de pruebas: 4 rondas, un turno para cada clase (4 x 3 = 12 selecciones en total)

faltantes = contar_clases(CY)
cantidad_faltantes = sum(faltantes)
contador = 0
while sum(faltantes) > 0:
    for turno in range(numero_clases):
        if faltantes[turno] == 0:
            continue
        while True:
            indice = rnd.randint(0, len(CY) - 1)
            if CY[indice][turno] == 1:
                datosPruebaX.append(CX.pop(indice))
                datosPruebaY.append(CY.pop(indice))

                contador += 1
                faltantes[turno] -= 1
                print("Seleccion (", contador, "/", cantidad_faltantes, ")")
                break

print("Datos de prueba seleccionados")

#-----------------------------------------------------------------
# Trasposicion para dejar de la misma forma. Filas son atributos/clases y columnas registros
datosEntrenamientoX = np.array(datosEntrenamientoX).T
datosEntrenamientoY = np.array(datosEntrenamientoY).T
datosPruebaX = np.array(datosPruebaX).T
datosPruebaY = np.array(datosPruebaY).T

print("X entrenamiento shape:", datosEntrenamientoX.shape)
print("Y entrenamiento shape:", datosEntrenamientoY.shape)
print("X prueba shape:", datosPruebaX.shape)
print("Y prueba shape:", datosPruebaY.shape)


with open("split_instancia_restaurantes_training.txt", "w") as f:
    f.write("Instancia Restaurantes - Training\n")
    f.write(str(datosEntrenamientoX.shape[0]) + "\n")
    for fila in datosEntrenamientoX:
        f.write("\t".join(map(str, fila)) + "\n")
    for fila in datosEntrenamientoY:
        f.write("\t".join(map(str, fila)) + "\n")

with open("split_instancia_restaurantes_test.txt", "w") as f:
    f.write("Instancia Restaurantes - Test\n")
    f.write(str(datosPruebaX.shape[0]) + "\n")
    for fila in datosPruebaX:
        f.write("\t".join(map(str, fila)) + "\n")
    for fila in datosPruebaY:
        f.write("\t".join(map(str, fila)) + "\n")

