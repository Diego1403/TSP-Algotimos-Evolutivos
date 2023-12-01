
# DIFERENCIAL A
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


def evolucion_diferencial_a(IE):
    matriz_distancias, tam_poblacion, n_elites, kBest = IE.matriz_distancias, IE.tam_poblacion, IE.E, IE.kBest
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
    padre = seleccion_torneo_binario(poblacion,kBest,random)[0]
       
    while not done:

        for i in range(tam_poblacion):

            padre1 = poblacion[i][0] #elegir padre1 de forma secuencial
            #elegir otros dos padres de forma aleatoria
            padre2 = random.sample(poblacion,1)[0]
            padre3 = random.sample(poblacion,1)[0]
                
            #nodo objetivo con kbest 2
            objetivo = seleccion_torneo_binario(poblacion,2,random)[0] 

            #elegir otra vez si no son distintos
            while not (padre1!=padre2!=padre3!=objetivo):
                padre2 = random.sample(poblacion,1)[0]
                padre3 = random.sample(poblacion,1)[0]
                objetivo = seleccion_torneo_binario(poblacion,kBest,random)[0]

             #------- RECOMBINAR--------------
            hijo = recombinacion_ternaria(padre1, objetivo, padre2, padre3,IE.matriz_distancias)
        
            #-----------EVALUAR---------------   
            if (hijo[1]<best_distance):
                best_distance = hijo[1]
                best_solution= hijo[0] 
        
            #-----------REMPLAZAR---------------
            if(hijo[1]<padre1[1]):
                poblacion[i] = hijo

        ciclo = ciclo +1
        if ciclo % 100 == 0:
            IE.log(str(best_distance)+" ciclo ="+str(ciclo)+" tiempo="+str(time.time()-start_time))
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 30 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
        
    return best_solution,best_distance
