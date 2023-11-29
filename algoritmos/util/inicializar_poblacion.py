def inicializar_poblacion(num_individuos, num_ciudades,aleatiorio):
    poblacion = []
    for _ in range(num_individuos):
        individuo = list(range(num_ciudades))
        aleatiorio.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion
