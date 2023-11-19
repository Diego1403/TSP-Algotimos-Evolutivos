

# Función para realizar el cruzamiento OX2 entre dos padres para producir dos descendientes
def cruzamiento_OX2(padre1, padre2,random):
    size = min(len(padre1), len(padre2))
    hijo1, hijo2 = [-1]*size, [-1]*size
    indices = sorted(random.sample(range(size), 2))
    set1, set2 = set(padre1[indices[0]:indices[1]]), set(padre2[indices[0]:indices[1]])

    hijo1[indices[0]:indices[1]], hijo2[indices[0]:indices[1]] = padre1[indices[0]:indices[1]], padre2[indices[0]:indices[1]]
    
    pos1, pos2 = indices[1], indices[1]
    
    for i in range(size):
        if padre2[(i+indices[1])%size] not in set1:
            hijo1[pos1%size] = padre2[(i+indices[1])%size]
            pos1 += 1
        if padre1[(i+indices[1])%size] not in set2:
            hijo2[pos2%size] = padre1[(i+indices[1])%size]
            pos2 += 1

    return hijo1, hijo2