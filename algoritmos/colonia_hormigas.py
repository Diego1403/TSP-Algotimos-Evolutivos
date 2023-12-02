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


def regla_transicion(ciudad_actual, mh, mf, alfa, beta, lista_ciudades_no_visitadas):
    probabilidades = []
    feromonas = mf[ciudad_actual, lista_ciudades_no_visitadas]
    heuristicas = mh[ciudad_actual, lista_ciudades_no_visitadas]
    denominador = np.sum(np.power(feromonas, alfa) * np.power(heuristicas, beta))

    for j in lista_ciudades_no_visitadas:
        numerador = np.power(mf[ciudad_actual, j], alfa) * np.power(mh[ciudad_actual, j], beta)
        probabilidad = numerador / denominador
        probabilidades.append(probabilidad)

    return random.choices(lista_ciudades_no_visitadas, weights=probabilidades, k=1)[0]


#actualizar feromonas
def demonio(poblacion, matriz_feromonas, matriz_distancias, mejor_hormiga, tasa_evaporacion, tasa_deposito):
    # Evaporación de feromonas
    matriz_feromonas *= (1 - tasa_evaporacion)

    # Depósito de feromonas
    for hormiga in poblacion:
        deposito = tasa_deposito / calcular_fitness(hormiga, matriz_distancias)
        for i in range(len(hormiga) - 1):
            matriz_feromonas[hormiga[i]][hormiga[i + 1]] += deposito
        # No olvidar la conexión del último elemento con el primero para completar el ciclo
        matriz_feromonas[hormiga[-1]][hormiga[0]] += deposito
    # Depósito adicional de la mejor hormiga global
    deposito_mejor = tasa_deposito / calcular_fitness(mejor_hormiga, matriz_distancias)
    for i in range(len(mejor_hormiga) - 1):
        matriz_feromonas[mejor_hormiga[i]][mejor_hormiga[i + 1]] += deposito_mejor
    matriz_feromonas[mejor_hormiga[-1]][mejor_hormiga[0]] += deposito_mejor


def inicializar_hormigas(tam_poblacion,n_cuidades,random):
    poblacion = []
    for _ in range(tam_poblacion-1):
        ind = [-1]*n_cuidades
        ind[0] = random.randint(0,n_cuidades-1)
        poblacion.append(ind)
    return poblacion

def colonia_hormigas(IE,  alfa=0.2, beta=0.1):
    
    random = IE.aleatorio
    matriz_distancias, tam_poblacion = IE.matriz_distancias, IE.tam_poblacion
    matriz_feromonas = np.ones_like(matriz_distancias)  # Inicializar con valores de 1
    #feromona inicial = 1/(greedy*numero_hormigas) 
    
    matriz_heuristica = 1 / (matriz_distancias + 1e-9)  # Evitar división por cero
    # estamos minimizando distancias , pero maximizando heuristica 
    
    

    mejor_solucion_global = None
    mejor_distancia_global = float('inf')
    
    start_time = time.time()  # Guardamos el tiempo inicial
    ciclo = 0
    done = False
    while not done:
        poblacion = inicializar_hormigas(tam_poblacion, len(matriz_distancias),random)
        print("poblacion inicialzada correctamente:")
        for hormiga in poblacion:
            ciudades_no_visitadas = set(range(len(matriz_distancias))) - set(hormiga)
            while ciudades_no_visitadas:
                ciudad_actual = hormiga[-1]
                
                if random.random() < 0.95:
                    siguiente_ciudad = regla_transicion(ciudad_actual, matriz_heuristica, matriz_feromonas, alfa, beta, list(ciudades_no_visitadas))
                    
                else :
                    pass# nos quedamos al arco mas prometedor podemos modificr la regla de transicion para que coja el mejor "el mayor prob"
                
                
                hormiga.append(siguiente_ciudad)
                ciudades_no_visitadas.remove(siguiente_ciudad)

        mejor_hormiga = None
        mejor_distancia = float('inf')
        for hormiga in poblacion:
            distancia = calcular_fitness(hormiga, matriz_distancias)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_hormiga = hormiga
            #aqui falta actualizar matriz_feromonas
        

        if mejor_distancia < mejor_distancia_global:
            mejor_distancia_global = mejor_distancia
            mejor_solucion_global = mejor_hormiga

        demonio(poblacion, matriz_feromonas, matriz_distancias, mejor_hormiga, tasa_evaporacion=0.01, tasa_deposito=1.0)
        ciclo = ciclo +1
        print(mejor_distancia)
        # Condición de terminación basada en el tiempo de ejecución
        if time.time() - start_time > 600 or ciclo>= 10000:
            done = True 
        
    return mejor_solucion_global, mejor_distancia_global
