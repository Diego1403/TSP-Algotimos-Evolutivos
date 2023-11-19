import configparser
import math
import numpy as np
import random

from controladores.C_Archivos import archivo_save_output, read_tsp_file

class Info_Ejecucion:
    def __init__(self,file_path) :
        self.load_configuration("config.ini")
        tsp_data = read_tsp_file("input_data/"+file_path) 
        
        self.nombre_lugar = tsp_data.get('NAME')
        self.tipo = tsp_data.get('TYPE')
        self.comentario = tsp_data.get('COMMENT')
        self.dimension = tsp_data.get('DIMENSION')
        self.ewt = tsp_data.get('EDGE_WEIGHT_TYPE')
        self.nodos = []
        self.matriz_distancias = []
        self.file_path = file_path
        # Cargar nodos
        for nodo in tsp_data.get('NODE_COORD_SECTION', []):
            self.add_nodo(nodo)
            

        self.calcular_matriz_distancias()

    
    def add_nodo(self,nodo):
        self.nodos.append(nodo)
    
    #función para calcular la matriz de distancias
    def calcular_matriz_distancias(self):

        self.matriz_distancias = np.zeros((self.dimension,self.dimension))

        def distancia_euclidea(nodo1, nodo2):
            return math.sqrt((nodo1[2] - nodo2[2]) ** 2 + (nodo1[1] - nodo2[1]) ** 2)
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.matriz_distancias[i][j] = distancia_euclidea(self.nodos[i],self.nodos[j])
        return self.matriz_distancias
    
    
                
    def print_matriz_distancias(self):
        for row in self.matriz_distancias:
            archivo_save_output("test.csv", row)
    
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
            self.prob_cruce = config.getfloat('default', 'prob_cruce')
            self.prob_mutacion = config.getfloat('default', 'prob_mutacion')
            
            
            print("config.ini loaded correctly")
        except (configparser.NoOptionError, ValueError) as e:
            print(f"An error occurred: {e}")
            return None
