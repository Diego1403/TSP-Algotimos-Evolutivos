import math
import numpy as np
from controladores.C_Archivos import read_tsp_file
from classes.Info_Ejecucion import  Info_Ejecucion

if __name__ == "__main__":
    #cargamos informacion 
    tsp_data = read_tsp_file("input_data/ch130.tsp")
    IE = Info_Ejecucion(tsp_data.get('NAME'),tsp_data.get('TYPE'),tsp_data.get('COMMENT'),tsp_data.get('DIMENSION'), tsp_data.get('EDGE_WEIGHT_TYPE'))

    #coger nodos
    for nodo in tsp_data.get('NODE_COORD_SECTION', []):
       IE.add_nodo(nodo) # el nodo guarda su (numero,latitud,longitud)
                         # esto no usa la clase nodo (no hace falta)
    
    #matriz distancias
    IE.calcular_matriz_distancias()
    


    #pass

