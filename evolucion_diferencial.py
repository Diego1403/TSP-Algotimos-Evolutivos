
import time
from cruzamiento_ox2 import cruzamiento_OX2
from recombinacion_ternaria import recombinacion_ternaria
from util import calcular_fitness, inicializar_poblacion, mutar_2opt, seleccion_torneo_binario

def evolucion_diferencial(IE):
    matriz_distancias, tam_poblacion, kBest = IE.matriz_distancias, 50, IE.kBest
    random = IE.aleatorio
    population = inicializar_poblacion(tam_poblacion, len(matriz_distancias))
    best_solution = None
    best_distance = float('inf')
    done = False
    
    start_time = time.time()  # Guardamos el tiempo inicial
    ciclo = 0
    while not done:
        # Calculamos la aptitud de cada individuo de la población
        fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in population]
        # Ordenamos la población basada en la aptitud (mejor a peor)
        #esta guardado como coste, individuo
        population_sorted = sorted(fitness_population, key=lambda x: x[1])
        padre = seleccion_torneo_binario(population_sorted,kBest)[0]
        aleatorio1 = random.shuffle(padre) 
        aleatorio2 = random.shuffle(padre) 
        objetivo = []
        #-----------SELECCIONAR---------------
        padre1, padre2 = seleccion_torneo_binario(population_sorted,kBest)
        #-----------RECOMBINAR---------------
        if random.random() < IE.prob_cruce:
            hijo1, hijo2 = recombinacion_ternaria(padre1, padre2)
        
        #-----------MUTAR---------------
        if random.random() < IE.prob_mutacion:   
            hijo1 = mutar_2opt(hijo1)
            hijo2 = mutar_2opt(hijo2)
        #-----------EVALUAR---------------   
        current_best_solution, current_best_distance = population_sorted[0]

        if current_best_distance < best_distance:
            best_solution = current_best_solution
            best_distance = current_best_distance
        #-----------REMPLAZAR---------------   
        population.extend([hijo1, hijo2])
        population = population[:tam_poblacion]  # Nos aseguramos de no exceder el tamaño de población

        ciclo = ciclo +1
        if ciclo % 1000 == 0:
            print(best_distance)
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 30 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
    return best_solution,best_distance
