# Función para mutación usando el algoritmo 2-opt
def mutar_2opt(aleatiorio,individuo):
    size = len(individuo)
    a, b = aleatiorio.sample(range(size), 2)
    if a > b:
        a, b = b, a
    individuo[a:b] = reversed(individuo[a:b])
    return individuo
