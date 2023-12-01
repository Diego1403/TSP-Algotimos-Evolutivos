def inicializar_poblacion(num_individuos, num_ciudades,aleatorio,matriz_distancias):
    poblacion=[]
    for _ in range(num_individuos):
        individuo = []
        pool = list(range(num_ciudades))
        punto_de_partida = aleatorio.choice(pool)
        individuo.append(punto_de_partida)
        pool.remove(punto_de_partida)

        while pool:
            if len(pool) > 5:
                muestra = aleatorio.sample(pool, 5)
            else:
                muestra = pool

            mejor_coste = float('inf')
            mejor_ciudad = None

            for ciudad in muestra:
                coste_actual = matriz_distancias[individuo[-1]][ciudad]
                if coste_actual < mejor_coste:
                    mejor_coste = coste_actual
                    mejor_ciudad = ciudad

            if mejor_ciudad is not None:
                individuo.append(mejor_ciudad)
                pool.remove(mejor_ciudad)
            else:
                # Mecanismo de escape: elegir una ciudad aleatoria de las restantes
                ciudad_aleatoria = aleatorio.choice(pool)
                individuo.append(ciudad_aleatoria)
                pool.remove(ciudad_aleatoria)

        poblacion.append(individuo)
    return poblacion
