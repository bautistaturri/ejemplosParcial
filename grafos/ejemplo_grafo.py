from collections import deque
class Grafo:
    def __init__(self):
        self.nodos = []
        self.matriz_adyacencia = []

    def agregar_nodo(self, etiqueta):
        if etiqueta not in self.nodos:
            self.nodos.append(etiqueta)
            # Agregar una nueva fila y columna a la matriz de adyacencia
            for fila in self.matriz_adyacencia:
                fila.append(0)
            self.matriz_adyacencia.append([0] * len(self.nodos))
        else:
            raise ValueError("El nodo ya existe en el grafo.")

    def agregar_arista(self, etiqueta1, etiqueta2):
        if etiqueta1 in self.nodos and etiqueta2 in self.nodos:
            i = self.nodos.index(etiqueta1)
            j = self.nodos.index(etiqueta2)
            self.matriz_adyacencia[i][j] = 1
            self.matriz_adyacencia[j][i] = 1
        else:
            raise ValueError("Uno o ambos nodos no existen en el grafo.")

    def eliminar_nodo(self, etiqueta):
        if etiqueta in self.nodos:
            index = self.nodos.index(etiqueta)
            self.nodos.pop(index)
            self.matriz_adyacencia.pop(index)
            for fila in self.matriz_adyacencia:
                fila.pop(index)
        else:
            raise ValueError("El nodo no existe en el grafo.")

    def eliminar_arista(self, etiqueta1, etiqueta2):
        if etiqueta1 in self.nodos and etiqueta2 in self.nodos:
            i = self.nodos.index(etiqueta1)
            j = self.nodos.index(etiqueta2)
            self.matriz_adyacencia[i][j] = 0
            self.matriz_adyacencia[j][i] = 0
        else:
            raise ValueError("Uno o ambos nodos no existen en el grafo.")

    def es_vecino_de(self, etiqueta1, etiqueta2):
        if etiqueta1 in self.nodos and etiqueta2 in self.nodos:
            i = self.nodos.index(etiqueta1)
            j = self.nodos.index(etiqueta2)
            return self.matriz_adyacencia[i][j] == 1
        else:
            raise ValueError("Uno o ambos nodos no existen en el grafo.")

    def vecinos_de(self, etiqueta):
        if etiqueta in self.nodos:
            index = self.nodos.index(etiqueta)
            vecinos = []
            for j, valor in enumerate(self.matriz_adyacencia[index]):
                if valor == 1:
                    vecinos.append(self.nodos[j])
            return vecinos
        else:
            raise ValueError("El nodo no existe en el grafo.")

    def __str__(self):
        grafo_str = "Nodos: " + str(self.nodos) + "\n"
        grafo_str += "Matriz de Adyacencia:\n"
        for fila in self.matriz_adyacencia:
            grafo_str += str(fila) + "\n"
        return grafo_str
    
    def BFS_principal(self):
        visitados = set()
        recorrido = []

        for nodo in self.nodos:
            if nodo not in visitados:
                cola = deque([nodo])
                self.BFS2(cola, visitados, recorrido)

        return recorrido

    def BFS2(self, cola, visitados, recorrido):
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                recorrido.append(nodo)
                vecinos = self.vecinos_de(nodo)
                for vecino in vecinos:
                    if vecino not in visitados:
                        cola.append(vecino)

# Ejemplo de uso
if __name__ == "__main__":
    grafo = Grafo()
    grafo.agregar_nodo("A")
    grafo.agregar_nodo("B")
    grafo.agregar_nodo("C")
    grafo.agregar_nodo("D")
    
    grafo.agregar_arista("A", "B")
    grafo.agregar_arista("A", "C")
    grafo.agregar_arista("B", "D")

    print(grafo)
    
    recorrido = grafo.BFS_principal()
    print("Recorrido BFS:", recorrido)