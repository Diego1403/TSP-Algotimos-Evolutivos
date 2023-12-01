
# DIFERENCIAL B
import time
from algoritmos.cruzamiento.cruzamiento_moc import cruzamiento_MOC
from algoritmos.cruzamiento.cruzamiento_ox2 import cruzamiento_OX2
from algoritmos.recombinacion.recombinacion_ternaria import recombinacion_ternaria
from algoritmos.mutacion.mutar_2opt import mutar_2opt
from algoritmos.seleccion.seleccion_torneo_binario import seleccion_torneo_binario

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

def evolucion_diferencial_b(IE):
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
        
        #-----------SELECCIONAR---------------
        
        padre1, padre2 = seleccion_torneo_binario(poblacion,kBest)
        
        posible_objetivo1 = []
        
        posible_objetivo2 = []
        # Seleccionando dos cromosomas distintos diferentes del padre
        while posible_objetivo1 != posible_objetivo2 and posible_objetivo1 != padre1 :
            posible_objetivo1 = random.sample(poblacion,1)
            posible_objetivo2 = random.sample(poblacion,1)
            
        if (posible_objetivo1[1] < posible_objetivo2[2]) :
            objetivo = posible_objetivo1
        else :
            objetivo = posible_objetivo2
            
        aleatorio1 = random.sample(poblacion,1)

        # Seleccionando otro cromosoma aleatorio diferente de los previamente seleccionados
        aleatorio2 = random.sample(poblacion,1)
        while aleatorio1 == aleatorio2:
            aleatorio2 = random.sample(poblacion,1)
        objetivo = seleccion_torneo_binario(poblacion,kBest)[0]

        hijo = recombinacion_ternaria(padre1, objetivo, aleatorio1, aleatorio2)
                    
        #-----------EVALUAR---------------   
        
        
        
        #-----------REMPLAZAR---------------
        if(hijo[1]<padre1[1]):
            nueva_poblacion.append(hijo)
        else:
            nueva_poblacion.append(padre1)

        ciclo = ciclo +1
        if ciclo % 100 == 0:
            print(best_distance)
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 30 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
        
    return best_solution,best_distance
