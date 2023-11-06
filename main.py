import random
import time
import numpy as np
from controladores.C_Archivos import archivo_save_output, read_tsp_file
from classes.Info_Ejecucion import  Info_Ejecucion

def inicializar_poblacion(num_individuos, num_ciudades):
    poblacion = []
    for _ in range(num_individuos):
        individuo = list(range(num_ciudades))
        random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion

def calcular_fitness(individuo, matriz_distancias):
    return sum(matriz_distancias[individuo[i], individuo[(i+1) % len(individuo)]] for i in range(len(individuo)))

def seleccion_torneo(poblacion, k, matriz_distancias):
    seleccionados = random.sample(poblacion, k)
    seleccionados.sort(key=lambda ind: calcular_fitness(ind, matriz_distancias))
    return seleccionados[0]

def modified_order_crossover(parent1, parent2):
    size = len(parent1)
    
    # Choose a random crossover point
    crossover_point = random.randint(0, size - 1)
    # Create empty children
    child1 = [None] * size
    child2 = [None] * size
    
    # Copy the right substrings from each parent to the corresponding child
    child1[crossover_point:] = parent1[crossover_point:]
    child2[crossover_point:] = parent2[crossover_point:]
    
    # Fill the left part of the children
    
    for i in range(crossover_point):
        for city in parent2:
            if city not in child1:
                child1[i] = city
                break
            
        for city in parent1:
            if city not in child2:
                child2[i] = city
                break
    
    return child1, child2

def cruzar_OX2(padre1, padre2):
    hijo = [-1] * len(padre1)
    start, end = sorted(random.sample(range(len(padre1)), 2))
    hijo[start:end] = padre1[start:end]
    pos = end
    for gene in padre2:
        if gene not in hijo:
            if pos >= len(hijo):
                pos = 0
            hijo[pos] = gene
            pos += 1
    return hijo

def mutar_2opt(individuo):
    a, b = random.sample(range(len(individuo)), 2)
    individuo[a], individuo[b] = individuo[b], individuo[a]
    return individuo

def algoritmo_genetico(matriz_distancias, num_generaciones, tam_poblacion):
    poblacion = inicializar_poblacion(tam_poblacion, len(matriz_distancias))
    start_time = time.time()
    for _ in range(num_generaciones):
        nueva_poblacion = []
        k = 3
        
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_torneo(poblacion, k, matriz_distancias)
            padre2 = seleccion_torneo(poblacion, k, matriz_distancias)
            hijo = cruzar_OX2(padre1, padre2)
            if random.random() < 0.1:  # Probabilidad de mutación
                hijo = mutar_2opt(hijo)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
        
        if time.time() - start_time > 60:
            print("Tiempo límite alcanzado, terminando evolución.")
            return poblacion
        
        
    return poblacion

if __name__ == "__main__":
    #cargamos informacion 
    tsp_data = read_tsp_file("input_data/ch130.tsp")
    IE = Info_Ejecucion(tsp_data.get('NAME'),tsp_data.get('TYPE'),tsp_data.get('COMMENT'),tsp_data.get('DIMENSION'), tsp_data.get('EDGE_WEIGHT_TYPE'))

    #coger nodos
    for nodo in tsp_data.get('NODE_COORD_SECTION', []):
       IE.add_nodo(nodo) # el nodo guarda su (numero,latitud,longitud)
                         # esto no usa la clase nodo (no hace falta)
    
    #matriz distancias
    
    IE.load_configuration("config.ini")
    print(IE.evaluaciones)
    IE.calcular_matriz_distancias()
    

    poblacion = algoritmo_genetico(IE.matriz_distancias, IE.evaluaciones, 50)
    
    # Encontrar la mejor solución
    mejor_solucion = min(poblacion, key=lambda individuo: calcular_fitness(individuo, IE.matriz_distancias))
    mejor_distancia = calcular_fitness(mejor_solucion, IE.matriz_distancias)
    
    print("Mejor solución encontrada:", mejor_solucion)
    print("Distancia de la mejor solución:", mejor_distancia)

