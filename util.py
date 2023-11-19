
# Función para inicializar una población de recorridos
import random


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
def seleccion_torneo_binario(poblacion,kbest):
    pool_selection = poblacion[:kbest]
    padre1 = random.sample(pool_selection, kbest)[0][0]
    padre2 = random.sample(pool_selection, kbest)[0][0]
    return padre1, padre2



# Función para mutación usando el algoritmo 2-opt
def mutar_2opt(individuo):
    size = len(individuo)
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a
    individuo[a:b] = reversed(individuo[a:b])
    return individuo

