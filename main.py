import random
import time
import numpy as np
from controladores.C_Archivos import archivo_save_output, read_tsp_file
from classes.Info_Ejecucion import  Info_Ejecucion

def grasp(gen_aleatorio,matriz_distancias,tam_problema):
    
    lista_mejores = np.zeros(tam_problema)
    completo = False

    while not completo:
        
        m = gen_aleatorio.randrange(0,tam_problema)
        while lista_mejores[m] != 0:
            m = gen_aleatorio.randrange(0,tam_problema)
    
        mejores = sorted(matriz_distancias[m]) #lista de las mejores
        mejor = mejores[gen_aleatorio.randrange(0,4)]
        lista_mejores[m] = matriz_distancias[m].tolist().index(mejor)

        completo = True

        for l in lista_mejores:
            if  l == 0:
                completo = False

    return lista_mejores


def inicializar_poblacion(num_individuos, num_ciudades):
    poblacion = []
    for _ in range(num_individuos):
        individuo = list(range(num_ciudades))
        random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion

def calcular_fitness(individuo, matriz_distancias):
    total_distance = 0
    num_ciudades = len(individuo)
    for i in range(num_ciudades):
        current_city = individuo[i]
        next_city = individuo[(i + 1) % num_ciudades]
        total_distance += matriz_distancias[current_city, next_city]
        
    return total_distance

def seleccion_torneo(poblacion, kBest, matriz_distancias):
    seleccionados = random.sample(poblacion, kBest)
    seleccionados.sort(key=lambda ind: calcular_fitness(ind, matriz_distancias))
    return seleccionados[0]
 

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

def algoritmo_genetico(matriz_distancias, num_generaciones, tam_poblacion, n_elites, kBest):
    poblacion = inicializar_poblacion(tam_poblacion, len(matriz_distancias))
    mejor_global = poblacion[0]  # Keep track of the best solution ever found
    start_time= time.time()
    for _ in range(num_generaciones):
        #todo : Guardar los elites
        
        nueva_poblacion = []
        
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_torneo(poblacion, kBest, matriz_distancias)
            padre2 = seleccion_torneo(poblacion, kBest, matriz_distancias)
            if random.random() < 0.7:
                hijo1 = cruzar_OX2(padre1, padre2)
            
            # Mutar
            if random.random() < 0.1:
                hijo1 = mutar_2opt(hijo1)

            nueva_poblacion.extend(hijo1)

        nueva_poblacion.sort(key=lambda ind: calcular_fitness(ind, matriz_distancias))
        # Replace worst if needed
        if calcular_fitness(mejor_global, matriz_distancias) < calcular_fitness(nueva_poblacion[-1], matriz_distancias):
            nueva_poblacion[-1] = mejor_global

        poblacion = nueva_poblacion[:tam_poblacion]  # Ensure the population size remains constant
        
        # Update global best if needed
        mejor_actual = min(poblacion, key=lambda ind: calcular_fitness(ind, matriz_distancias))
        if not mejor_global or calcular_fitness(mejor_actual, matriz_distancias) < calcular_fitness(mejor_global, matriz_distancias):
            mejor_global = mejor_actual
            
        if time.time() - start_time > 30:
            print("Tiempo límite alcanzado, terminando evolución.")
            return mejor_global
        

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

    print(grasp(IE.aleatorio,IE.matriz_distancias,IE.dimension))   

    mejor_solucion = algoritmo_genetico(IE.matriz_distancias, IE.evaluaciones, 50,IE.E,IE.kBest)
    
    # Encontrar la mejor solución
    mejor_distancia = calcular_fitness(mejor_solucion, IE.matriz_distancias)
    
    print("Mejor solución encontrada:", mejor_solucion)
    print("Distancia de la mejor solución:", mejor_distancia)

