# Función para calcular la aptitud (fitness) de un individuo (la distancia total del recorrido)
def calcular_fitness(individuo, matriz_distancias):
    return sum(matriz_distancias[individuo[i]][individuo[i - 1]] for i in range(len(individuo)))
