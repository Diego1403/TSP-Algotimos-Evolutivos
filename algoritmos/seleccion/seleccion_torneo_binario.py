# Función para realizar la selección de torneo binario en la población
def seleccion_torneo_binario(poblacion,kbest,aleatiorio):
    pool_selection = poblacion[:kbest]
    padre1 = aleatiorio.sample(pool_selection, kbest)[0][0]
    padre2 = aleatiorio.sample(pool_selection, kbest)[0][0]
    return padre1, padre2
