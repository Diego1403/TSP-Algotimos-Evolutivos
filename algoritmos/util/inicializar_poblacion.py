import numpy as np

def inicializar_poblacion(num_individuos, num_ciudades,aleatorio, matriz_distancias):
    poblacion = []

    #GENERACION ALEATORIA
    for _ in range(round(num_individuos*0.8)):
        individuo = list(range(num_ciudades))
        aleatorio.shuffle(individuo)
        poblacion.append(individuo)

    #GENERACION CON GREEEDY ALEATORIZADO
    for _ in range(round(num_individuos*0.2)):
        individuo = np.zeros(num_ciudades)
        pool = list(range(num_ciudades))
        for i in range(individuo):
            sample = aleatorio.sample(pool,5)
            mejor_coste = 999999
            for s in sample:
                if(matriz_distancias[i][s]>mejor_coste):
                    mejor_coste = matriz_distancias[i][s]
                    mejor = s        
            individuo[i] = mejor
            pool.remove(mejor)
        poblacion.append(individuo)

    return poblacion

