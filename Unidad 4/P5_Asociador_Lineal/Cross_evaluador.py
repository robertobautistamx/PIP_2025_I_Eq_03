import random

#Asociador Lineal

#X = Entradas
#Y = Salidas
#W = Y*XPseudoInversa

import numpy as n

def contar_registros_por_clase(listaY):
    return [len(sublista) for sublista in listaY]

def imprimir_fold(Fold):
    for i, fold in enumerate(Fold):
        print(f"--- Fold {i + 1} ---")
        for j, registro in enumerate(fold):
            print(f"Registro {j + 1}: {registro}")
        print()  # Línea en blanco entre folds

#Lectura del archivo, obtecion de X(entradas) y Y(salidas)
archivo = open("Instancia_Restaurante.txt")
contenido = archivo.readlines()

X = contenido[3:3+int(contenido[1])]
X = [i.split("\t") for i in X]
X = [list(map(int, i)) for i in X]
Y = contenido[3+int(contenido[1]):]
Y = [i.split("\t") for i in Y]
Y = [list(map(int, i)) for i in Y]

#60 filas que representan regirstros
X = n.array(X).T # 6 columnas que representan los atributos
Y = n.array(Y).T # 3 filas que representan las clases
print("X shape:", X.shape)
print("Y shape:", Y.shape)



#Proceso de agrupacion y seleccion, 60 registros / 3 clases = 20 folds
registros = Y.shape[0]
numeroDeClases = Y.shape[1]
numFolds = registros // numeroDeClases
print("Numero de Registros: ", registros)
print("Numero de Clases: ", numeroDeClases)
print("Numero de Folds: ", numFolds)


# Primero ordenaremos los registros en su sublista correspondiente  [ [c1s], [c2s], [c3s] ]
RegistrosPorClaseX  = [[] for _ in range(numeroDeClases)]
RegistrosPorClaseY  = [[] for _ in range(numeroDeClases)]
# RegistrosPorClaseX[0]) sublista con elementos de la clase 1,
# RegistrosPorClaseX[0][0] = registro 1: [distancias, horas, precios, calificaciones, horas, numIntegrantes],
# RegistrosPorClaseX[0][0][0] = distancias
for i in range(registros):
    for c in range(numeroDeClases):
        if Y[i][c] == 1:
            RegistrosPorClaseX[c].append(X[i])
            RegistrosPorClaseY[c].append(Y[i])
            break

#Repartir de forma aleatoria y equilibrada los registros en cada fold, son 20
FoldsX = [[] for _ in range(numFolds)] #20
FoldsY = [[] for _ in range(numFolds)] #20


# Mientras haya al menos un elemento en alguna clase
while any(len(clase) > 0 for clase in RegistrosPorClaseY):

    for fold_index in range(numFolds):  # Recorrido de cada fold

        # asegurar un maximo de 3, y en el regreso se llenaran los folds incompletos
        if len(FoldsX[fold_index]) >= numeroDeClases:
            continue

        for clase_index in range(numeroDeClases):  # Para poder insertar un registro de cada clase dentro de cada fold
            if len(RegistrosPorClaseY[clase_index]) > 0: #dejar de intentar insertar registros de una clase, la cual ya se quedo sin ejemplos
                indice = random.randint(0, len(RegistrosPorClaseY[clase_index]) - 1)
                # Sacamos el registro de forma aleatoria
                y = RegistrosPorClaseY[clase_index].pop(indice)
                x = RegistrosPorClaseX[clase_index].pop(indice)
                # Lo agregamos al fold correspondiente, solo se pondran 3 elementos en cada fold
                FoldsX[fold_index].append(x)
                FoldsY[fold_index].append(y)


#imprimir_fold( FoldsY)



# Proceso de evaluacion, un ciclo con 20 iteraciones, cada folds sera la prueba una vez
print("\n--- Validación Cruzada ---\n")

total_aciertos = 0
total_casos = 0
Clases = ["El asador ", "El lindero", "Casa laguna"]
for i in range(numFolds):
    print("Fold ", i)
    # 1. Separar fold i como prueba
    #(6, 3)  = [ dist[   4    2    2] horas[   3    1    2] dinero[2000 1300 3000] calif[   4    4    4] hora[  13   15   16] personas[   2    3    7] ]
    X_test = n.array(FoldsX[i]).T
    Y_test = n.array(FoldsY[i]).T  #(3, 3)

    # 2. Folds como entrenamiento
    X_train = []
    Y_train = []
    for j in range(numFolds):
        if j != i: #Todos menos el de prueba
            X_train.extend(FoldsX[j])
            Y_train.extend(FoldsY[j])
    X_train = n.array(X_train).T
    Y_train = n.array(Y_train).T

    # 3. Entrenamiento del modelo (W)
    Paso1 = X_train.dot(X_train.T)
    Paso2 = n.linalg.inv(Paso1)
    Xpseudo = X_train.T.dot(Paso2)
    W = Y_train.dot(Xpseudo)

    # 4. Probar con los datos de prueba
    for k in range(X_test.shape[1]):  # para cada caso en el fold de prueba
        casoi = X_test[:, k]
        Ycasoi = W.dot(casoi)
        Yreal = Y_test[:, k]

        pred = list(Ycasoi).index(max(Ycasoi))
        real = list(Yreal).index(max(Yreal))
        print("Caso ",total_casos," [Prediccion | Real -> ", Clases[pred], "___", Clases[real], "]")

        if pred == real:
            total_aciertos += 1
        total_casos += 1
    print()
# Resultado final
print(f"Total de casos evaluados: {total_casos}")
print(f"Total de aciertos: {total_aciertos}")
print(f"Eficiencia promedio: {total_aciertos / total_casos * 100:.2f}%")






