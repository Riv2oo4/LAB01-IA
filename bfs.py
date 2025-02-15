import pandas as pd
from collections import deque

file_path = "LAB01/funcion_de_costo.xlsx"
xls = pd.ExcelFile(file_path)
df_costos = xls.parse("Hoja1")  

class ColaFIFO:
    def __init__(self):
        self.datos = deque()

    def EMPTY(self):
        return len(self.datos) == 0

    def TOP(self):
        return self.datos[0] if not self.EMPTY() else None

    def POP(self):
        return self.datos.popleft() if not self.EMPTY() else None

    def ADD(self, elemento):
        self.datos.append(elemento)

    def __repr__(self):
        return f"ColaFIFO({list(self.datos)})"
    
class Nodo:
    def __init__(self, estado, accion=None, padre=None):
        self.estado = estado  
        self.accion = accion  
        self.padre = padre  

    def __repr__(self):
        return f"Nodo({self.estado})"


grafo = {}
for _, row in df_costos.iterrows():
    origen = row["Origen"]
    destino = row["Destino"]

    if origen not in grafo:
        grafo[origen] = []
    grafo[origen].append(destino)  


def bfs(inicio, objetivo, grafo):
    orden_correcto = ["Step Mill-4", "TreadMill-3", "ExBike-2", "Skipping Rope-1"]
    frontera = ColaFIFO()  
    frontera.ADD(Nodo(inicio))
    explorados = set()

    print(f"\nInicio de BFS desde {inicio} hasta {objetivo}\n")

    while not frontera.EMPTY():
        print(f"Frontera: {[nodo.estado for nodo in frontera.datos]}")
        nodo_actual = frontera.POP()
        estado_actual = nodo_actual.estado

        if estado_actual == objetivo:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.estado)
                nodo_actual = nodo_actual.padre
            print("\nCamino encontrado:", list(reversed(camino)))
            return list(reversed(camino))

        explorados.add(estado_actual)

        hijos = grafo.get(estado_actual, [])
        hijos_ordenados = sorted(hijos, key=lambda x: orden_correcto.index(x) if x in orden_correcto else len(orden_correcto))

        for vecino in hijos_ordenados:
            if vecino not in explorados:
                nuevo_nodo = Nodo(estado=vecino, accion=f"to {vecino}", padre=nodo_actual)
                frontera.ADD(nuevo_nodo)

        print(f"Visitados: {list(explorados)}\n")

    print("\nNo se encontró un camino.")
    return None  

camino = bfs("Warm-up activities", "Stretching", grafo)
