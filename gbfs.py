import pandas as pd
import heapq
file_path_costos = "LAB01/funcion_de_costo.xlsx"
xls_costos = pd.ExcelFile(file_path_costos)
df_costos = xls_costos.parse("Hoja1")  

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

    def __lt__(self, otro):
        """ Comparación para la cola de prioridad (GBFS usa heurística). """
        return self.heuristica < otro.heuristica  

    def __repr__(self):
        return f"Nodo({self.estado}, Heurística: {self.heuristica})"


grafo = {}
for _, row in df_costos.iterrows():
    origen = row["Origen"]
    destino = row["Destino"]

    if origen not in grafo:
        grafo[origen] = []
    grafo[origen].append(destino)  

print("\nGrafo construido para GBFS (sin costos):")
for nodo, vecinos in grafo.items():
    print(f"{nodo}: {vecinos}")

file_path_heuristica = "LAB01/heuristica.xlsx"
xls_heuristica = pd.ExcelFile(file_path_heuristica)
df_heuristica = xls_heuristica.parse("Hoja1") 

heuristica = {}
for _, row in df_heuristica.iterrows():
    heuristica[row["Activity"]] = row["Recovery time after burning 300cal (minutes)"]


def gbfs(inicio, objetivo, grafo, heuristica):
    frontera = ColaPrioridad()
    frontera.ADD(heuristica[inicio], Nodo(inicio, heuristica=heuristica[inicio]))  
    explorados = set()

    print(f"\nInicio de GBFS desde {inicio} hasta {objetivo}\n")

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

        explorados.add(estado_actual)

        for vecino in grafo.get(estado_actual, []):  
            if vecino not in explorados:
                nuevo_nodo = Nodo(estado=vecino, 
                                  accion=f"to {vecino}", 
                                  padre=nodo_actual, 
                                  heuristica=heuristica.get(vecino, float('inf')))  
                frontera.ADD(nuevo_nodo.heuristica, nuevo_nodo)

        print(f"Visitados: {list(explorados)}\n")

    print("\nNo se encontró un camino.")
    return None  

camino_gbfs = gbfs("Warm-up activities", "Stretching", grafo, heuristica)
