
# DIFERENCIAL A
import time
from algoritmos.recombinacion.recombinacion_ternaria import recombinacion_ternaria


def inicializar_poblacion(num_individuos, num_ciudades,aleatorio, matriz_distancias):
    poblacion = []

    #GENERACION ALEATORIA
    for _ in range(round(num_individuos*0.8)):
        individuo = list(range(num_ciudades))
        aleatorio.shuffle(individuo)
        poblacion.append(individuo)

    #GENERACION CON GREEEDY ALEATORIZADO
    for _ in range(round(num_individuos*0.2)):
        individuo = []
        pool = list(range(num_ciudades))
        punto_de_partida = aleatorio.choice(pool)
        individuo.append(punto_de_partida)
        pool.remove(punto_de_partida)

        while pool:
            if len(pool) > 5:
                muestra = aleatorio.sample(pool, 5)
            else:
                muestra = pool

            mejor_coste = float('inf')
            mejor_ciudad = None

            for ciudad in muestra:
                coste_actual = matriz_distancias[individuo[-1]][ciudad]
                if coste_actual < mejor_coste:
                    mejor_coste = coste_actual
                    mejor_ciudad = ciudad

            if mejor_ciudad is not None:
                individuo.append(mejor_ciudad)
                pool.remove(mejor_ciudad)
            else:
                # Mecanismo de escape: elegir una ciudad aleatoria de las restantes
                ciudad_aleatoria = aleatorio.choice(pool)
                individuo.append(ciudad_aleatoria)
                pool.remove(ciudad_aleatoria)

        poblacion.append(individuo)
    return poblacion

def calcular_fitness(individuo, matriz_distancias):
    return sum(matriz_distancias[individuo[i]][individuo[i - 1]] for i in range(len(individuo)))

def seleccion_torneo_binario(poblacion,kbest,aleatiorio):
    pool_selection = poblacion[:kbest]
    padre1 = aleatiorio.sample(pool_selection, kbest)[0][0]
    padre2 = aleatiorio.sample(pool_selection, kbest)[0][0]
    return padre1, padre2

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
       
    while not done:

        for i in range(tam_poblacion):
            padre1 = poblacion[i][0]
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
                #print(best_distance)
        
            #-----------REMPLAZAR---------------
            if(hijo[1]<padre1[1]):
                poblacion[i] = hijo[0]

        fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in population]
        # Ordenamos la población basada en la mejor (mejor a peor)
        poblacion = sorted(fitness_population, key=lambda x: x[1])
        poblacion = poblacion[:tam_poblacion]  # Nos aseguramos de no exceder el tamaño de población
        
        ciclo = ciclo +1
        if ciclo % 100 == 0:
            IE.log(str(best_distance)+" ciclo ="+str(ciclo)+" tiempo="+str(time.time()-start_time))
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 60 or ciclo>= IE.evaluaciones:
            done = True  # Terminamos si la ejecución supera los 30 segundos
        
    return best_solution,best_distance