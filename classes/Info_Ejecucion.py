class Info_Ejecucion:
    def __init__(self,nombre_lugar,tipo , comentario,dimension,ewt) :
        self.nombre_lugar = nombre_lugar
        self.tipo = tipo
        self.comentario = comentario
        self.dimension = dimension
        self.ewt = ewt
        self.nodos = []
    
    def add_nodo(self,nodo):
        self.nodos.append(nodo)