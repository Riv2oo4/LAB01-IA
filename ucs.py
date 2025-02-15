import pandas as pd
import heapq

file_path = "LAB01/funcion_de_costo.xlsx"
xls = pd.ExcelFile(file_path)
df_costos = xls.parse("Hoja1")  
class Nodo:
    def __init__(self, estado, accion=None, padre=None, costo_acumulado=0):
        self.estado = estado  
        self.accion = accion  
        self.padre = padre 
        self.costo_acumulado = costo_acumulado  

    def __lt__(self, otro):
        return self.costo_acumulado < otro.costo_acumulado  

    def __repr__(self):
        return f"Nodo({self.estado}, Costo: {self.costo_acumulado})"

class ColaPrioridad:
    def __init__(self):
        self.datos = []

    def EMPTY(self):
        return len(self.datos) == 0

    def TOP(self):
        return self.datos[0] if not self.EMPTY() else None

    def POP(self):
        return heapq.heappop(self.datos) if not self.EMPTY() else None

    def ADD(self, prioridad, elemento):
        heapq.heappush(self.datos, (prioridad, elemento))

    def __repr__(self):
        return f"ColaPrioridad({self.datos})"


grafo = {}
for _, row in df_costos.iterrows():
    origen = row["Origen"]
    destino = row["Destino"]
    costo = row["Cost"]

    if origen not in grafo:
        grafo[origen] = []
    grafo[origen].append((destino, costo))  

def ucs(inicio, objetivo, grafo):
    frontera = ColaPrioridad()  
    frontera.ADD(0, Nodo(inicio, costo_acumulado=0))  
    explorados = {}
    print(f"\nInicio de UCS desde {inicio} hasta {objetivo}\n")
    
    while not frontera.EMPTY():
        print(f"Frontera: {[nodo.estado for _, nodo in frontera.datos]}")
        _, nodo_actual = frontera.POP()
        estado_actual = nodo_actual.estado

        if estado_actual == objetivo:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.estado)
                nodo_actual = nodo_actual.padre
            print("\nCamino encontrado:", list(reversed(camino)))
            return list(reversed(camino))
        if estado_actual in explorados and explorados[estado_actual] <= nodo_actual.costo_acumulado:
            continue

        explorados[estado_actual] = nodo_actual.costo_acumulado

        for vecino, costo in grafo.get(estado_actual, []):
            nuevo_costo = nodo_actual.costo_acumulado + costo
            nuevo_nodo = Nodo(estado=vecino, accion=f"to {vecino}", padre=nodo_actual, costo_acumulado=nuevo_costo)
            frontera.ADD(nuevo_costo, nuevo_nodo)
        print(f"Visitados con costo: {explorados}\n")

    print("\nNo se encontró un camino.")
    return None  
camino_ucs = ucs("Warm-up activities", "Stretching", grafo)
