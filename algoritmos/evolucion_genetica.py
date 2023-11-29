
# Función principal que ejecuta el algoritmo genético
import time
from cruzamiento_moc import cruzamiento_MOC
from cruzamiento_ox2 import cruzamiento_OX2
from util import calcular_fitness, inicializar_poblacion, mutar_2opt, seleccion_torneo_binario


def algoritmo_genetico(IE):
    matriz_distancias, tam_poblacion, n_elites, kBest = IE.matriz_distancias, 50, IE.E, IE.kBest
    random = IE.aleatorio
    population = inicializar_poblacion(tam_poblacion, len(matriz_distancias))
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
        
        padre1, padre2 = seleccion_torneo_binario(poblacion,kBest)
        #-----------RECOMBINAR---------------
 
        if random.random() < IE.prob_cruce:
            hijo1, hijo2 = cruzamiento_OX2(padre1, padre2, IE.aleatorio)
        else:
            hijo1, hijo2 = padre1,padre2
    #-----------MUTAR---------------
        if random.random() < IE.prob_mutacion:        
            hijo1 = mutar_2opt(hijo1)
            hijo2 = mutar_2opt(hijo2)
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
