
# Función principal que ejecuta el algoritmo genético
import time

import numpy as np
from algoritmos.cruzamiento.cruzamiento_moc import cruzamiento_MOC
from algoritmos.cruzamiento.cruzamiento_ox2 import cruzamiento_OX2

from algoritmos.mutacion.mutar_2opt import mutar_2opt
from algoritmos.seleccion.seleccion_torneo_binario import seleccion_torneo_binario
def inicializar_poblacion(num_individuos, num_ciudades,aleatiorio):
    poblacion = []
    for _ in range(num_individuos):
        individuo = list(range(num_ciudades))
        aleatiorio.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion
def calcular_fitness(individuo, matriz_distancias):
    return sum(matriz_distancias[individuo[i]][individuo[i - 1]] for i in range(len(individuo)))

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

    return lista_sol

def algoritmo_genetico_ox2(IE):
    matriz_distancias, tam_poblacion, n_elites, kBest = IE.matriz_distancias, 50, IE.E, IE.kBest
    random = IE.aleatorio
    population = inicializar_poblacion(tam_poblacion, len(matriz_distancias),random)
    #poblacion debe inicializarse con greedy aleatorizado???
    best_solution = None
    best_distance = float('inf')
    done = False
    start_time = time.time()  # Guardamos el tiempo inicial
    ciclo = 0
    fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in population]
    # Ordenamos la población basada en la mejor (mejor a peor)
    poblacion = sorted(fitness_population, key=lambda x: x[1])
    #for p in poblacion:
    #    print(p[1])
       
    while not done:

        nueva_poblacion = []
        # Conservamos a los individuos élite
        elites = poblacion[:n_elites]
        
        # Evaluación de la nueva población
        for e in elites:
                nueva_poblacion.append(e[0])
        #-----------SELECCIONAR---------------
        
        padre1, padre2 = seleccion_torneo_binario(poblacion,kBest, IE.aleatorio)
        #-----------RECOMBINAR---------------
 
        if random.random() < IE.prob_cruce:
            hijo1, hijo2 = cruzamiento_OX2(padre1, padre2, IE.aleatorio)
        else:
            hijo1, hijo2 = padre1,padre2
    #-----------MUTAR---------------
        if random.random() < IE.prob_mutacion:        
            hijo1 = mutar_2opt(IE.aleatorio,hijo1)
            hijo2 = mutar_2opt( IE.aleatorio,hijo2)
        nueva_poblacion.extend([hijo1, hijo2])
        
        #-----------EVALUAR---------------   
        current_best_solution, current_best_distance = elites[0]
        if current_best_distance < best_distance:
            best_solution = current_best_solution
            best_distance = current_best_distance
        

        #-----------REMPLAZAR---------------
        for p in poblacion:
            if p[0] not in nueva_poblacion  :  
                nueva_poblacion.append(p[0])
        # Calculamos la aptitud de cada individuo de la población
        fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in nueva_poblacion]
        # Ordenamos la población basada en la mejor (mejor a peor)
        #los elites por naturaleza van al principio 
        
        nueva_poblacion_sorted = sorted(fitness_population, key=lambda x: x[1])         
        poblacion = nueva_poblacion_sorted[:tam_poblacion]  # Nos aseguramos de no exceder el tamaño de población
        
        ciclo = ciclo +1
        if ciclo % 100 == 0:
            print(best_distance)
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time > 30 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
    return best_solution,best_distance