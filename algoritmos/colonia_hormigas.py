import pprint
import time
import numpy as np
import random
def calcular_fitness(ruta, matriz_distancias):
    distancia_total = 0
    numero_ciudades = len(ruta)

    for i in range(numero_ciudades - 1):
        distancia_total += matriz_distancias[ruta[i]][ruta[i + 1]]

    # Añadir la distancia de regreso a la ciudad inicial para completar el ciclo
    distancia_total += matriz_distancias[ruta[-1]][ruta[0]]

    return distancia_total


def regla_transicion(ciudad_actual, mh, mf, alfa, beta, lista_ciudades_no_visitadas,lanzar_aleatorio):
    probabilidades = []
    feromonas = mf[ciudad_actual, lista_ciudades_no_visitadas]
    heuristicas = mh[ciudad_actual, lista_ciudades_no_visitadas]
    denominador = np.sum(np.power(feromonas, alfa) * np.power(heuristicas, beta))
    
    for j in lista_ciudades_no_visitadas:
        numerador = np.power(mf[ciudad_actual, j], alfa) * np.power(mh[ciudad_actual, j], beta)
        probabilidad = numerador / denominador
        probabilidades.append(probabilidad)
    if lanzar_aleatorio :
        return random.choices(lista_ciudades_no_visitadas, weights=probabilidades, k=1)[0]
    else :
        max_index = np.argmax(probabilidades)
        return lista_ciudades_no_visitadas[max_index]

    

def demonio(poblacion, matriz_feromonas, matriz_distancias, mejor_hormiga, tasa_evaporacion_global=0.1, tasa_evaporacion_local=0.1):
    # Depósito de feromonas global
    for hormiga in poblacion:
        deposito_global = 1 / calcular_fitness(hormiga, matriz_distancias)
        for i in range(len(hormiga) - 1):
            matriz_feromonas[hormiga[i]][hormiga[i + 1]] += deposito_global
        matriz_feromonas[hormiga[-1]][hormiga[0]] += deposito_global

    # Depósito local de feromonas
    deposito_local = 1 / calcular_fitness(mejor_hormiga, matriz_distancias)
    for hormiga in poblacion:
        for i in range(len(hormiga) - 1):
            matriz_feromonas[hormiga[i]][hormiga[i + 1]] += deposito_local
        matriz_feromonas[hormiga[-1]][hormiga[0]] += deposito_local

    # Evaporación de feromonas global
    matriz_feromonas *= (1 - tasa_evaporacion_global)

    # Evaporación de feromonas local
    matriz_feromonas += (1 - tasa_evaporacion_local) * np.where(matriz_distancias != 0, 1 / matriz_distancias, 0)
    
    
def greedy(matriz_distancias):
    numero_ciudades = len(matriz_distancias)
    ruta = [0]  # Start with the first city as the initial city

    ciudades_no_visitadas = set(range(1, numero_ciudades))  # Exclude the initial city

    while ciudades_no_visitadas:
        ciudad_actual = ruta[-1]
        distancias_disponibles = [(ciudad, matriz_distancias[ciudad_actual][ciudad]) for ciudad in ciudades_no_visitadas]
        distancias_disponibles.sort(key=lambda x: x[1])
        siguiente_ciudad = distancias_disponibles[0][0]
        ruta.append(siguiente_ciudad)
        ciudades_no_visitadas.remove(siguiente_ciudad)
        
    mejor = calcular_fitness(ruta,matriz_distancias)
    return mejor


def inicializar_hormigas(tam_poblacion,n_cuidades,random):
    poblacion = []
    for _ in range(tam_poblacion-1):
        ind = [-1]*n_cuidades
        ind[0] = random.randint(0,n_cuidades-1)
        poblacion.append(ind)
    return poblacion

    
def colonia_hormigas(IE,  alfa=1, beta=2):
    
    random = IE.aleatorio
    matriz_distancias, tam_poblacion = IE.matriz_distancias, IE.tam_poblacion
    tam_matriz_distancias = len(matriz_distancias)
    #carga inicial de feromonas
    valor_greedy = greedy(matriz_distancias)
    
    fInicial= 1/(tam_poblacion*valor_greedy);
    
    matriz_feromonas = np.full((tam_matriz_distancias, tam_matriz_distancias), fInicial)
    matriz_heuristica = np.where(matriz_distancias != 0, 1 / matriz_distancias, 0)
    # estamos minimizando distancias , pero maximizando heuristica 
    mejor_solucion_global = None
    mejor_distancia_global = float('inf')
    
    start_time = time.time()  # Guardamos el tiempo inicial
    ciclo = 0
    done = False
    while not done:
        poblacion = inicializar_hormigas(tam_poblacion, len(matriz_distancias),random)
        print("poblacion inicialzada correctamente:")
        #print("Matriz Feromonas:")
        #np.set_printoptions(precision=1)
        #pprint.pprint(matriz_feromonas)
        
            
        for hormiga in poblacion:
            
            ciudades_no_visitadas = set(range(len(matriz_distancias))) - set(hormiga)
            while ciudades_no_visitadas:
                ciudad_actual = hormiga[-1]
                if random.random() > 0.95:
                    siguiente_ciudad = regla_transicion(ciudad_actual, matriz_heuristica, matriz_feromonas, alfa, beta, list(ciudades_no_visitadas),True)
                else:
                    siguiente_ciudad = regla_transicion(ciudad_actual, matriz_heuristica, matriz_feromonas, alfa, beta, list(ciudades_no_visitadas),False)
                ciudades_no_visitadas.remove(siguiente_ciudad)
                hormiga.append(siguiente_ciudad)
                

        mejor_hormiga = None
        mejor_distancia = float('inf')
        for hormiga in poblacion:
            distancia = calcular_fitness(hormiga, matriz_distancias)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_hormiga = hormiga
        
        if mejor_distancia < mejor_distancia_global:
            mejor_distancia_global = mejor_distancia
            mejor_solucion_global = mejor_hormiga

        demonio(poblacion, matriz_feromonas, matriz_distancias, mejor_hormiga, tasa_evaporacion_global=0.1, tasa_evaporacion_local=0.1)

        
        poblacion.clear()
        ciclo = ciclo +1
        print(mejor_distancia)
        # Condición de terminación basada en el tiempo de ejecución
        print(time.time() - start_time)
        if (time.time() - start_time > 60) or (ciclo>= 10000):
            done=True
        
    return mejor_solucion_global, mejor_distancia_global
