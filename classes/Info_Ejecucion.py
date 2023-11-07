import configparser
import math
import numpy as np
import random

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
        #self.print_matriz_distancias()
        return self.matriz_distancias
                
    def print_matriz_distancias(self):
        for row in self.matriz_distancias:
            print (row)
    
    def load_configuration(self,file_path):
        # Initialize the parser
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read(file_path)


        # Read values from the 'default' section
        try:

            self.algoritmos= config.get('default', 'algoritmos')
            self.dataset= config.get('default', 'dataset')
            self.tam_poblacion= config.getint('default', 'M')
            self.E = config.getint('default', 'E')
            self.kBest= config.getint('default', 'kBest')
            self.kWorst = config.getint('default', 'kWorst')
            self.evaluaciones = config.getint('default', 'evaluaciones')
            self.semilla = config.getint('default', 'semilla')
            self.aleatorio = random.Random(self.semilla)
            
            print("config.ini loaded correctly")
        except (configparser.NoOptionError, ValueError) as e:
            print(f"An error occurred: {e}")
            return None
