import math
import numpy as np

class Info_Ejecucion:
    def __init__(self,nombre_lugar,tipo , comentario,dimension,ewt) :
        self.nombre_lugar = nombre_lugar
        self.tipo = tipo
        self.comentario = comentario
        self.dimension = dimension
        self.ewt = ewt
        self.nodos = []
        self.matriz_distancias = []
    
    def add_nodo(self,nodo):
        self.nodos.append(nodo)
    
    #función para calcular la matriz de distancias
    def calcular_matriz_distancias(self):

        self.matriz_distancias = np.zeros((self.dimension,self.dimension))

        def distancia_euclidea(nodo1, nodo2):
            return math.sqrt((nodo2[1] - nodo1[1]) ** 2 + (nodo2[2] - nodo2[1]) ** 2)

        for i in range(self.dimension):
            for j in range(self.dimension):
                self.matriz_distancias[i][j] = distancia_euclidea(self.nodos[i],self.nodos[j])
    
