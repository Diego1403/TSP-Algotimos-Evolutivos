# Función principal que ejecuta el algoritmo genético
import time

import numpy as np
from algoritmos.cruzamiento.cruzamiento_moc import cruzamiento_MOC
from algoritmos.cruzamiento.cruzamiento_ox2 import cruzamiento_OX2

from algoritmos.mutacion.mutar_2opt import mutar_2opt
from algoritmos.seleccion.seleccion_torneo_binario import seleccion_torneo_binario
from algoritmos.seleccion.seleccion_torneo_binario import seleccion_torneo_perdedores
def inicializar_poblacion(num_individuos, num_ciudades,aleatorio, matriz_distancias):
    poblacion = []

    #GENERACION ALEATORIA
    for _ in range(round(num_individuos*0.8)):
        individuo = list(range(num_ciudades))
        aleatorio.shuffle(individuo)
        poblacion.append(individuo)

    #GENERACION CON GREEEDY ALEATORIZADO
    for _ in range(round(num_individuos*0.2)):
        individuo = list(range(num_ciudades))
        pool = list(range(num_ciudades))
        for i in range(len(individuo)):
            if(len(pool)>5):
                sample = aleatorio.sample(pool,5)
            else:
                sample = pool
                aleatorio.shuffle(sample)
            mejor_coste = 999999
            mejor = -1
            for s in sample:
                if(matriz_distancias[i][s]<mejor_coste):
                    mejor_coste = matriz_distancias[i][s]
                    mejor = s        
            individuo[i] = mejor
            pool.remove(mejor)
        poblacion.append(individuo)
    return poblacion
def calcular_fitness(individuo, matriz_distancias):
    return sum(matriz_distancias[individuo[i]][individuo[i - 1]] for i in range(len(individuo)))

def algoritmo_genetico_moc(IE):
    matriz_distancias, tam_poblacion, n_elites, kBest, kWorst = IE.matriz_distancias, IE.tam_poblacion, IE.E, IE.kBest, IE.kWorst
    random = IE.aleatorio
    population = inicializar_poblacion(tam_poblacion, len(matriz_distancias),random,matriz_distancias)
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
        
        padre1, padre2 = seleccion_torneo_binario(poblacion,kBest,IE.aleatorio)
        #-----------RECOMBINAR---------------
 
        if random.random() < IE.prob_cruce:
            hijo1, hijo2 = cruzamiento_MOC(padre1, padre2, IE.aleatorio)
        else:
            hijo1, hijo2 = padre1,padre2
    #-----------MUTAR---------------
        if random.random() < IE.prob_mutacion:        
            hijo1 = mutar_2opt(IE.aleatorio,hijo1)
            hijo2 = mutar_2opt(IE.aleatorio,hijo2)
        nueva_poblacion.extend([hijo1, hijo2])
        
        #-----------EVALUAR---------------   
        current_best_solution, current_best_distance = elites[0]
        if current_best_distance < best_distance:
            best_solution = current_best_solution
            best_distance = current_best_distance
        

        #-----------REMPLAZAR---------------
        #utilizar Kworst para reemplazar el peor en caso de que el mejor de los élites no estén
        for e in elites:
            if e[0] not in nueva_poblacion:
                peor = seleccion_torneo_perdedores(nueva_poblacion, kWorst, IE.aleatorio)
                poblacion = nueva_poblacion_sorted.remove(peor)

        # Calculamos la aptitud de cada individuo de la población
        fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in nueva_poblacion]
        # Ordenamos la población basada en la mejor (mejor a peor)
        #los elites por naturaleza van al principio 
        
        nueva_poblacion_sorted = sorted(fitness_population, key=lambda x: x[1])         
        poblacion = nueva_poblacion_sorted[:tam_poblacion]  # Nos aseguramos de no exceder el tamaño de población
        
        ciclo = ciclo +1
        if ciclo % 100 == 0:
            IE.log(str(current_best_distance)+" ciclo ="+str(ciclo)+" tiempo="+str(time.time()-start_time))
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time > 30 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
    return best_solution,best_distance
