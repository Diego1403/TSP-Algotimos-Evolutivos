import numpy as np

def greedy_aleatorizado(gen_aleatorio,matriz_distancias,tam_problema,tam_lista):

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

    lista_sol = lista_mejores[:tam_lista]
    print(lista_sol)

    return lista_sol

def inicializar_poblacion(num_individuos, num_ciudades,aleatiorio):
    poblacion = []
    for _ in range((num_individuos)):
        individuo = list(range(num_ciudades))
        aleatiorio.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion

