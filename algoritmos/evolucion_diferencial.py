
# Función principal que ejecuta el algoritmo genético
import time
from algoritmos.cruzamiento.cruzamiento_moc import cruzamiento_MOC
from algoritmos.cruzamiento.cruzamiento_ox2 import cruzamiento_OX2
from algoritmos.recombinacion.recombinacion_ternaria import recombinacion_ternaria
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


def evolucion_diferencial(IE):
    matriz_distancias, tam_poblacion, n_elites, kBest = IE.matriz_distancias, 50, IE.E, IE.kBest
    random = IE.aleatorio
    population = inicializar_poblacion(tam_poblacion, len(matriz_distancias),random)
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
    padre = seleccion_torneo_binario(poblacion,kBest,random)[0]
       
    while not done:

        nueva_poblacion = []
        # Conservamos a los individuos élite
        
        #-----------SELECCIONAR---------------

        aleatorio1 = random.sample(poblacion,1)[0]
        aleatorio2 = random.sample(poblacion,1)[0]
        while aleatorio1 == aleatorio2:
            aleatorio2 = random.sample(poblacion,1)[0]
        objetivo = seleccion_torneo_binario(poblacion,kBest,random)[0]
        
        #------- RECOMBINAR--------------
        hijo = recombinacion_ternaria(padre, objetivo, aleatorio1, aleatorio2,IE.matriz_distancias)
        
        #-----------EVALUAR---------------   
        if (hijo[1]<best_distance):
            best_distance = hijo[1]
            best_solution= hijo[0] 
        
        #-----------REMPLAZAR---------------
        if(hijo[1]<padre[1]):
            nueva_poblacion.append(hijo)
        else:
            nueva_poblacion.append(padre)

        ciclo = ciclo +1
        if ciclo % 100 == 0:
            print(best_distance)
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 30 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
        
    return best_solution,best_distance
