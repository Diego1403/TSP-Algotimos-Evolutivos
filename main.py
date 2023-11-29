
# Suponemos que Info_Ejecucion y read_tsp_file están definidos en los módulos dados
from configparser import ConfigParser
from classes.Info_Ejecucion import Info_Ejecucion
from colonia_hormigas import colonia_hormigas
from evolucion_diferencial import evolucion_diferencial
from evolucion_genetica import algoritmo_genetico
from util import *


import configparser

def main():
    # Cargar el archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extraer valores de la configuración

    kWorst = int(config.get('default', 'kWorst'))
    evaluaciones = int(config.get('default', 'evaluaciones'))
    semilla = int(config.get('default', 'semilla'))
    prob_cruce = float(config.get('default', 'prob_cruce'))
    prob_mutacion = float(config.get('default', 'prob_mutacion'))
    #inicializamos con informacion que no cambia
    IE =  Info_Ejecucion(prob_mutacion,prob_cruce,semilla,evaluaciones,kWorst)
    
    algoritmos = config.get('default', 'algoritmos').split()
    datasets = config.get('default', 'dataset').split()
    n_elites = [int(e) for e in config.get('default', 'E').split()]
    kBest = [int(k) for k in config.get('default', 'kBest').split()]
    n_individuos = [int(n) for n in config.get('default', 'M').split()]
    # Ejecutar operaciones para cada combinación de algoritmo y dataset
    data = []
    data["algoritmo"] = "" 
    data["dataset"] = ""
    data["tam_poblacion"] = ""
    data["E"] = ""
    data["kBest"] = ""
    data["tipo_diferencial"] = ""
    
    for dataset in datasets:
        data["dataset"]=dataset
        IE.update_dataset()
        
        for algoritmo in algoritmos:
            data["algoritmo"] = algoritmo
            
            print(f'Ejecutando {algoritmo} con {dataset}')
            if algoritmo == "GenOX2":
                for e in n_elites:
                    for kbest in kBest:
                        for tam_poblacion in n_individuos:
                            data["tam_poblacion"] = tam_poblacion
                            data["E"] = e
                            data["kBest"] = kbest
                            IE.update_data(data)
                            mejor_solucion,mejor_distancia = algoritmo_genetico(IE)
                
            if algoritmo == "EDA":                
                for tam_poblacion in n_individuos:
                    data["tam_poblacion"] = tam_poblacion
                    data["kBest"] = kbest
                    data["tipo_diferencial"] = "EDA"
                    IE.update_data(data)
                    mejor_solucion,mejor_distancia = evolucion_diferencial(IE)
            
            if algoritmo == "EDB":
                for tam_poblacion in n_individuos:
                    data["tam_poblacion"] = tam_poblacion
                    data["kBest"] = kbest
                    data["tipo_diferencial"] = "EDB"
                    IE.update_data(data)
                    mejor_solucion,mejor_distancia = evolucion_diferencial(IE)
                
            if algoritmo == "HORMIGAS":             
                #mejor_solucion,mejor_distancia = colonia_hormigas(IE)
                pass
            print("Mejor solución encontrada:", mejor_solucion)
            print("Distancia de la mejor solución:", mejor_distancia)




if __name__ == "__main__":
    main()

