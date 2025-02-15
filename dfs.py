import pandas as pd

file_path = "LAB01/funcion_de_costo.xlsx"
xls = pd.ExcelFile(file_path)
df_costos = xls.parse("Hoja1")   
class PilaLIFO:
    def __init__(self):
        self.datos = []

    def EMPTY(self):
        return len(self.datos) == 0

    def TOP(self):
        return self.datos[-1] if not self.EMPTY() else None

    def POP(self):
        return self.datos.pop() if not self.EMPTY() else None

    def ADD(self, elemento):
        self.datos.append(elemento)

    def __repr__(self):
        return f"PilaLIFO({self.datos})"
    
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

def dfs(inicio, objetivo, grafo):
    frontera = PilaLIFO()  
    frontera.ADD(Nodo(inicio))
    explorados = set()

    print(f"\nInicio de DFS desde {inicio} hasta {objetivo}\n")

    while not frontera.EMPTY():
        print(f"Frontera: {[nodo.estado for nodo in frontera.datos]}")
        nodo_actual = frontera.POP()
        estado_actual = nodo_actual.estado
        if estado_actual == objetivo:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.estado)
                nodo_actual = nodo_actual.padre
            print("\nCamino encontrado: ", list(reversed(camino)))
            return list(reversed(camino))

        explorados.add(estado_actual)
        hijos = grafo.get(estado_actual, [])

        for vecino in reversed(hijos):  
            if vecino not in explorados:
                nuevo_nodo = Nodo(estado=vecino, accion=f"to {vecino}", padre=nodo_actual)
                frontera.ADD(nuevo_nodo)

        print(f"Visitados:  {list(explorados)}\n")

    print("\nNo se encontró un camino.")
    return None  

camino_dfs = dfs("Warm-up activities", "Stretching", grafo)
