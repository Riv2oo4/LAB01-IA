import heapq
import pandas as pd

file_path_costos = "LAB01/funcion_de_costo.xlsx"
xls_costos = pd.ExcelFile(file_path_costos)
df_costos = xls_costos.parse("Hoja1")  
file_path_heuristica = "LAB01/heuristica.xlsx"
xls_heuristica = pd.ExcelFile(file_path_heuristica)
df_heuristica = xls_heuristica.parse("Hoja1")  

heuristica = {}
for _, row in df_heuristica.iterrows():
    heuristica[row["Activity"]] = row["Recovery time after burning 300cal (minutes)"]

print("\n Valores de heurística:")
for nodo, valor in heuristica.items():
    print(f"{nodo}: {valor}")

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


class Nodo:
    def __init__(self, estado, accion=None, padre=None, costo_acumulado=0, heuristica=0):
        self.estado = estado
        self.accion = accion
        self.padre = padre
        self.costo_acumulado = costo_acumulado  
        self.heuristica = heuristica  
        self.f = self.costo_acumulado + self.heuristica  
    def __lt__(self, otro):
        return self.f < otro.f  
    def __repr__(self):
        return f"Nodo({self.estado}, Costo: {self.costo_acumulado}, Heurística: {self.heuristica}, f: {self.f})"

grafo_a_estrella = {}
for _, row in df_costos.iterrows():
    origen = row["Origen"]
    destino = row["Destino"]
    costo = row["Cost"]

    if origen not in grafo_a_estrella:
        grafo_a_estrella[origen] = []
    grafo_a_estrella[origen].append((destino, costo))  

print("\nGrafo construido para A* (con costos):")
for nodo, vecinos in grafo_a_estrella.items():
    print(f"{nodo}: {vecinos}")


def a_star(inicio, objetivo, grafo, heuristica):
    frontera = ColaPrioridad()  
    frontera.ADD(0, Nodo(inicio, costo_acumulado=0, heuristica=heuristica[inicio])) 
    explorados = {}

    print(f"\nInicio de A* desde {inicio} hasta {objetivo} \n")

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
            nuevo_nodo = Nodo(estado=vecino, 
                              accion=f"to {vecino}", 
                              padre=nodo_actual, 
                              costo_acumulado=nuevo_costo, 
                              heuristica=heuristica.get(vecino, float('inf')))  
            frontera.ADD(nuevo_nodo.f, nuevo_nodo)

        print(f"Visitados con costo: {explorados}\n")

    print("\nNo se encontró un camino.")
    return None  
camino_a_star = a_star("Warm-up activities", "Stretching", grafo_a_estrella, heuristica)
