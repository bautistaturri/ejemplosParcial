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


class NavegadorWeb(Grafo):
    def __init__(self):
        super().__init__()

    def agregar_pagina(self, url):
        self.agregar_nodo(url)

    def agregar_enlace(self, url1, url2):
        self.agregar_arista(url1, url2)

    def navegar_desde(self, url_inicial):
        if url_inicial not in self.nodos:
            raise ValueError("La página inicial no existe en el grafo.")
        
        visitados = set()
        recorrido = []
        cola = deque([url_inicial])
        
        while cola:
            url_actual = cola.popleft()
            if url_actual not in visitados:
                visitados.add(url_actual)
                recorrido.append(url_actual)
                vecinos = self.vecinos_de(url_actual)
                for vecino in vecinos:
                    if vecino not in visitados:
                        cola.append(vecino)
        
        return recorrido

# Ejemplo de uso
if __name__ == "__main__":
    navegador = NavegadorWeb()
    navegador.agregar_pagina("https://pagina1.com")
    navegador.agregar_pagina("https://pagina2.com")
    navegador.agregar_pagina("https://pagina3.com")
    navegador.agregar_pagina("https://pagina4.com")
    
    navegador.agregar_enlace("https://pagina1.com", "https://pagina2.com")
    navegador.agregar_enlace("https://pagina1.com", "https://pagina3.com")
    navegador.agregar_enlace("https://pagina2.com", "https://pagina4.com")
    
    print(navegador)
    
    recorrido = navegador.navegar_desde("https://pagina3.com")
    print("Recorrido BFS desde https://pagina3.com:", recorrido)
