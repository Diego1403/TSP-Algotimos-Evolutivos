import configparser
import math
import numpy as np
import random
import logging 

from controladores.C_Archivos import archivo_save_output, read_tsp_file

class Info_Ejecucion:
    def __init__(self,prob_mutacion,prob_cruce,semilla,evaluaciones,kWorst):
        self.kWorst = kWorst
        self.evaluaciones = evaluaciones
        self.semilla = semilla
        self.aleatorio = random.Random(self.semilla)
        self.prob_cruce = prob_cruce
        self.prob_mutacion = prob_mutacion

        
    
    def update_data(self,file_path,data) :
        self.algoritmo= data["algoritmo"]
        self.dataset= data["dataset"]
        self.tam_poblacion= data["tam_poblacion"]
        self.E = data["E"]
        self.kBest= data["kBest"]
        self.tipo_diferencial = data["tipo_diferencial"]
        logging.basicConfig(filename=self.algoritmo+self.dataset+".log", 
        format='%(asctime)s %(message)s', 
		filemode='w') 
        self.logger=logging.getLogger() 
        self.logger.setLevel(logging.DEBUG) 
    
    def log(self,msg):
        self.logger.info(msg) 

    def update_dataset(self,file_path):
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
    
   