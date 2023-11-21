import random
import time

import numpy as np

# Suponemos que Info_Ejecucion y read_tsp_file están definidos en los módulos dados
from classes.Info_Ejecucion import Info_Ejecucion
from controladores.C_Archivos import read_tsp_file

def grasp(gen_aleatorio,matriz_distancias,tam_problema,tam_lista):

    lista_mejores = np.zeros(tam_problema)
    completo = False

    while not completo:

        m = gen_aleatorio.randrange(0,tam_problema)
        while lista_mejores[m] != 0:
            m = gen_aleatorio.randrange(0,tam_problema)

        mejores = sorted(matriz_distancias[m]) #lista de las mejores
        mejor = mejores[gen_aleatorio.randrange(0,4)]
        lista_mejores[m] = matriz_distancias[m].tolist().index(mejor)

        completo = True

        for l in lista_mejores:
            if  l == 0:
                completo = False

    lista_sol = lista_mejores[:tam_lista]

    return lista_mejores

# Función para inicializar una población de recorridos
def inicializar_poblacion(num_individuos, num_ciudades):
    poblacion = []
    for _ in range(num_individuos):
        individuo = list(range(num_ciudades))
        random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion

# Función para calcular la aptitud (fitness) de un individuo (la distancia total del recorrido)
def calcular_fitness(individuo, matriz_distancias):
    return sum(matriz_distancias[individuo[i]][individuo[i - 1]] for i in range(len(individuo)))

# Función para realizar la selección de torneo binario en la población
def seleccion_torneo_binario(poblacion,kbest,aleatorio):
    sample1 = aleatorio.sample(poblacion, kbest)
    sample2 = aleatorio.sample(poblacion, kbest)
    padre1 = min(sample1, key=lambda x: x[1])[0]
    padre2 = min(sample2, key=lambda x: x[1])[0]
    return padre1, padre2

def get_kworst(poblacion,kworst,aleatorio):
    sample1 = aleatorio.sample(poblacion, kworst)
    sample2 = aleatorio.sample(poblacion, kworst)
    padre1 = max(sample1, key=lambda x: x[1])[0]
    padre2 = max(sample2, key=lambda x: x[1])[0]
    return padre1, padre2

# Función para realizar el cruzamiento OX2 entre dos padres para producir dos descendientes

def cruzamiento_OX2(padre1, padre2,aleatorio):
    punto_cruce1 = aleatorio.randint(0, len(padre1) - 1)
    punto_cruce2 = aleatorio.randint(punto_cruce1 + 1, len(padre1))

    hijo1 = [None] * len(padre1)


    hijo1[punto_cruce1:punto_cruce2] = padre1[punto_cruce1:punto_cruce2]


    for i in range(len(padre1)):
        if hijo1[i] is None:
            for gen in padre2:
                if gen not in hijo1:
                    hijo1[i] = gen
                    break
                    
    punto_cruce1 = aleatorio.randint(0, len(padre1) - 1)
    punto_cruce2 = aleatorio.randint(punto_cruce1 + 1, len(padre1))

    hijo2 = hijo1
    hijo2.reverse()
    return hijo1, hijo2

# Función para mutación usando el algoritmo 2-opt
def mutar_2opt(individuo,aleatorio):
    size = len(individuo)
    a, b = aleatorio.sample(range(size), 2)
    individuo[a:b] = reversed(individuo[a:b])
    return individuo

#TODO: cruce MOC y arreglar cosas
# Función principal que ejecuta el algoritmo genético
def algoritmo_genetico(IE):
    matriz_distancias=IE.matriz_distancias
    evaluaciones = IE.evaluaciones
    tam_poblacion=IE.tam_poblacion
    n_elites = IE.E
    kBest = IE.kBest
    aleatorio = IE.aleatorio
    prob_cruce = IE.prob_cruce
    prob_mutacion = IE.prob_mutacion
    best_solution = None
    best_distance = float('inf')
    done = False
    ciclo = 0
    start_time = time.time()  # Guardamos el tiempo inicial
    
    population = inicializar_poblacion(tam_poblacion-5, len(matriz_distancias))
    poulation.append(grasp(aleatorio,matriz_distancias,len(matriz_distancias),5))


    while not done:
        # Calculamos la aptitud de cada individuo de la población
        fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in population]
        # Ordenamos la población basada en la aptitud (mejor a peor)
        population_sorted = sorted(fitness_population, key=lambda x: x[1])
        # Conservamos a los individuos élite
        elites = population_sorted[:n_elites]
        new_population = [ind[0] for ind in elites]
        
        #-----------SELECCIONAR---------------
        padre1, padre2 = seleccion_torneo_binario(population_sorted,kBest,aleatorio)
        #-----------RECOMBINAR---------------

        if aleatorio.random() < prob_cruce:  
            hijo1, hijo2 = cruzamiento_OX2(padre1, padre2)
        else :
            hijo1=padre1
            hijo2=padre2
        #-----------MUTAR---------------
        if aleatorio.random() < prob_mutacion:        
            hijo1 = mutar_2opt(hijo1,aleatorio)
            
        #-----------EVALUAR---------------   
        current_best_solution, current_best_distance = population_sorted[0]
        
        if ciclo % 1000 == 0:  #  imprimir cada 100 ciclos
            print(best_distance)
        
        if current_best_distance < best_distance:
            best_solution = current_best_solution
            best_distance = current_best_distance
            
        #-----------REMPLAZAR---------------   
        #hijo1,hijo2= get_kworst(population_sorted,IE.kWorst)
        new_population.extend([hijo1, hijo2])
        
        population = new_population[:tam_poblacion]  # Nos aseguramos de no exceder el tamaño de población
        

        ciclo += 1
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 60 or ciclo>evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
    return best_solution,best_distance


def recombinacion_ternaria(padre,aleatorio_1,aleatorio_2):

    return

#TODO: HACER ESTO EN CONDICIONES
#mode es el modo para elegir entre 'A' y 'B'
def algoritmo_diferencial_evolutivo(IE, mode):
    matriz_distancias=IE.matriz_distancias
    evaluaciones = IE.evaluaciones
    tam_poblacion=IE.tam_poblacion
    n_elites = IE.E
    kBest = IE.kBest
    aleatorio = IE.aleatorio
    prob_cruce = IE.prob_cruce
    prob_mutacion = IE.prob_mutacion
    best_solution = None
    best_distance = float('inf')
    done = False
    ciclo = 0
    start_time = time.time()  # Guardamos el tiempo inicial
    
    population = inicializar_poblacion(tam_poblacion-5, len(matriz_distancias))
    poulation.append(grasp(aleatorio,matriz_distancias,len(matriz_distancias),5))

    while not done:

        #-----------SELECCIONAR---------------
        for i in range(tam_poblacion):

            padre1 = matriz_distancias[i] #elegir padre1 de forma secuencial

            if(mode = 'A'):

                #elegir otros dos padres de forma aleatoria
                padre2 = matriz_distancias[aleatorio.randrange(0,tam_poblacion)]
                padre3 = matriz_distancias[aleatorio.randrange(0,tam_poblacion)]
                
                #nodo objetivo con kbest 2
                objetivo = seleccion_torneo_binario(population_sorted,2,aleatorio) 

                #elegir otra vez si no son distintos
                while not (padre1!=padre2!=padre3!=objetivo):
                    objetivo = seleccion_torneo_binario(population_sorted,2,aleatorio) 
                    padre2 = matriz_distancias[aleatorio.randrange(0,tam_poblacion)]
                    padre3 = matriz_distancias[aleatorio.randrange(0,tam_poblacion)]
            
            if(mode = 'B'):

                #elegir los tres por torneo con kbest 3
                padre2, padre3, objetivo = seleccion_torneo_binario(population_sorted,3,aleatorio)
                
                #elegir otra vez si no son distintos
                while not (padre1!=padre2!=padre3!=objetivo):
                    padre2, padre3, objetivo = seleccion_torneo_binario(population_sorted,3,aleatorio)
            
        #-----------RECOMBINAR---------------

            #recorrer todos los genes de cada individuo
            for genes in n_genes
                if (aleatorio.random>prob_cruce):
                    final = recombinacion_ternaria(padre1,padre2,padre3)
            
        #-----------EVALUAR + REEMPLAZAR---------------

        #si el recombinado mejora al padre lo reemplaza
        if distancia_final > distancia_objetivo:
            padre1 = final

        ciclo += 1
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 60 or ciclo>evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
    return best_solution,best_distance


if __name__ == "__main__":
    # Cargar los datos del TSP y preparar la información de ejecución
    tsp_data = read_tsp_file("input_data/ch130.tsp") 
    IE = Info_Ejecucion(tsp_data.get('NAME'), tsp_data.get('TYPE'), tsp_data.get('COMMENT'), tsp_data.get('DIMENSION'), tsp_data.get('EDGE_WEIGHT_TYPE'))

    # Cargar nodos
    for nodo in tsp_data.get('NODE_COORD_SECTION', []):
        IE.add_nodo(nodo)

    # Cargar configuración y calcular la matriz de distancias
    IE.load_configuration("config.ini")
    
    IE.calcular_matriz_distancias()

    # Ejecutar el algoritmo genético
    mejor_solucion,mejor_distancia = algoritmo_genetico(IE)
    
    
    # Imprimir la mejor solución y su distancia
    print("Mejor solución encontrada:", mejor_solucion)
    print("Distancia de la mejor solución:", mejor_distancia)
