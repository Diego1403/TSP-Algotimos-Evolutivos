
# Suponemos que Info_Ejecucion y read_tsp_file están definidos en los módulos dados
from classes.Info_Ejecucion import Info_Ejecucion
from evolucion_diferencial import evolucion_diferencial
from evolucion_genetica import algoritmo_genetico
from util import *





if __name__ == "__main__":
    
    IE = Info_Ejecucion("ch130.tsp")
    mejor_solucion,mejor_distancia = algoritmo_genetico(IE)
    
    #mejor_solucion,mejor_distancia = evolucion_diferencial(IE)

    print("Mejor solución encontrada:", mejor_solucion)
    print("Distancia de la mejor solución:", mejor_distancia)

