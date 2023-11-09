import random
import time

# Suponemos que Info_Ejecucion y read_tsp_file están definidos en los módulos dados
from classes.Info_Ejecucion import Info_Ejecucion
from controladores.C_Archivos import read_tsp_file

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
def seleccion_torneo_binario(poblacion):
    padre1 = min(random.sample(poblacion, 2), key=lambda x: x[1])
    padre2 = min(random.sample(poblacion, 2), key=lambda x: x[1])
    return padre1[0], padre2[0]

# Función para realizar el cruzamiento OX2 entre dos padres para producir dos descendientes
def cruzamiento_OX2(padre1, padre2):
    size = min(len(padre1), len(padre2))
    hijo1, hijo2 = [-1]*size, [-1]*size
    indices = sorted(random.sample(range(size), 2))
    set1, set2 = set(padre1[indices[0]:indices[1]]), set(padre2[indices[0]:indices[1]])

    hijo1[indices[0]:indices[1]], hijo2[indices[0]:indices[1]] = padre1[indices[0]:indices[1]], padre2[indices[0]:indices[1]]
    
    pos1, pos2 = indices[1], indices[1]
    for i in range(size):
        if padre2[(i+indices[1])%size] not in set1:
            hijo1[pos1%size] = padre2[(i+indices[1])%size]
            pos1 += 1
        if padre1[(i+indices[1])%size] not in set2:
            hijo2[pos2%size] = padre1[(i+indices[1])%size]
            pos2 += 1

    return hijo1, hijo2

# Función para mutación usando el algoritmo 2-opt
def mutar_2opt(individuo):
    size = len(individuo)
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a
    individuo[a:b] = reversed(individuo[a:b])
    return individuo

# Función principal que ejecuta el algoritmo genético
def algoritmo_genetico(matriz_distancias, num_generaciones, tam_poblacion, n_elites, kBest):
    population = inicializar_poblacion(tam_poblacion, len(matriz_distancias))
    best_solution = None
    best_distance = float('inf')
    done = False
    start_time = time.time()  # Guardamos el tiempo inicial

    while not done:
        # Calculamos la aptitud de cada individuo de la población
        fitness_population = [(individuo, calcular_fitness(individuo, matriz_distancias)) for individuo in population]
        # Ordenamos la población basada en la aptitud (mejor a peor)
        population_sorted = sorted(fitness_population, key=lambda x: x[1])
        # Conservamos a los individuos élite
        elites = population_sorted[:n_elites]
        new_population = [ind[0] for ind in elites]

        padre1, padre2 = seleccion_torneo_binario(population_sorted)
        hijo1, hijo2 = cruzamiento_OX2(padre1, padre2)
        hijo1 = mutar_2opt(hijo1)
        hijo2 = mutar_2opt(hijo2)
        new_population.extend([hijo1, hijo2])

        population = new_population[:tam_poblacion]  # Nos aseguramos de no exceder el tamaño de población

        current_best_solution, current_best_distance = population_sorted[0]
        print(best_distance)
        if current_best_distance < best_distance:
            best_solution = current_best_solution
            best_distance = current_best_distance

        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time    > 30:
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
    mejor_solucion,mejor_distancia = algoritmo_genetico(IE.matriz_distancias, IE.evaluaciones, 50, IE.E, IE.kBest)
    
    
    # Imprimir la mejor solución y su distancia
    print("Mejor solución encontrada:", mejor_solucion)
    print("Distancia de la mejor solución:", mejor_distancia)
