import random

from algoritmos.cruzamiento.cruzamiento_ox2 import cruzamiento_OX2
from algoritmos.util.calcular_fitness import calcular_fitness

def recombinacion_ternaria(padre, obj, a1, a2,md):
    a1 = a1[0]
    a2 = a2[0]
    nuevo_padre=padre.copy()
    pos1 = random.randint(0, len(padre) - 2) #nos aseguramos que la posicion no es el ultimo elemento
    pos2 = pos1+1
    nuevo_padre[pos1], nuevo_padre[pos2] = nuevo_padre[pos2], nuevo_padre[pos1]
    
    #buscamos conteindo de la posicion1 del padre en aleatorio1
    contenido_p_pos1 = nuevo_padre[pos1]
    contenido_p_pos2 = nuevo_padre[pos2]
    for i in range(len(a1)):
        if(a1[i]==contenido_p_pos1):
            pos1_a1 = i          
            break 
    contenido_a1_pos=padre[pos1_a1]
    
     #buscamos conteindo de la posicion1 del aleario1 en padre
    for i in range(len(padre)):
        if(padre[i]==contenido_a1_pos):
            pos2_a1 = i          
            break 
    nuevo_padre = a1.copy()
    nuevo_padre[pos1_a1], nuevo_padre[pos2_a1] = nuevo_padre[pos1_a1], nuevo_padre[pos2_a1]
    #-----------------------------------------
    
    #buscamos conteindo de la posicion2 del padre en aleatorio2
    
    for i in range(len(a2)):
        if(a2[i]==contenido_p_pos2):
            pos1_a2 = i          
            break 
    
    contenido_a2_pos=nuevo_padre[pos1_a2]

    for i in range(len(padre)):
        if(a2[i]==contenido_a2_pos):
            pos2_a2 = i          
            break 
    
    nuevo_padre[pos1_a2], nuevo_padre[pos2_a2] = nuevo_padre[pos1_a2], nuevo_padre[pos2_a2]
    hijo1,hijo2 =  cruzamiento_OX2(padre,obj,random)
    coste_hijo1 = calcular_fitness(hijo1,md)
    coste_hijo2 = calcular_fitness(hijo2,md)
    
    if (coste_hijo1<coste_hijo1): 
        return hijo1,coste_hijo1
    else:
        return hijo2,coste_hijo2

