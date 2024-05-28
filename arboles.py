from typing import Generic, Optional, TypeVar,List,Callable


T = TypeVar('T')

class NodoAB(Generic[T]):
    def __init__(self, dato: T, si: Optional['ArbolBinario[T]'] = None, sd: Optional['ArbolBinario[T]'] = None):
        self.dato: T = dato
        self.si: 'ArbolBinario[T]' = ArbolBinario() if si is None else si
        self.sd: 'ArbolBinario[T]' = ArbolBinario() if sd is None else sd

class ArbolBinario(Generic[T]):
    def __init__(self):
        self.raiz: Optional[NodoAB[T]] = None
        self.antecesor: Optional['ArbolBinario[T]'] = None

    def set_raiz(self, nueva_raiz: Optional[NodoAB[T]]) -> None:
        """
        Establece la raíz del árbol como el nodo dado.
        """
        self.raiz = nueva_raiz
    
    def es_vacio(self) -> bool:
        return self.raiz is None

    @staticmethod
    def crear_nodo(dato: T, si: Optional['ArbolBinario[T]'] = None, sd: Optional['ArbolBinario[T]'] = None) -> 'ArbolBinario[T]':
        t = ArbolBinario()
        t.raiz = NodoAB(dato, si, sd)
        if si:
            si.antecesor = t
        if sd:
            sd.antecesor = t
        return t

    def insertar_si(self, si: 'ArbolBinario[T]'):
        if self.es_vacio():
            raise TypeError('Árbol vacío')
        self.raiz.si = si
        self.raiz.si.antecesor = self

    def insertar_sd(self, sd: 'ArbolBinario[T]'):
        if self.es_vacio():
            raise TypeError('Árbol vacío')
        self.raiz.sd = sd
        self.raiz.sd.antecesor = self


    def si(self) -> 'ArbolBinario[T]':
        if self.es_vacio():
            raise TypeError('Árbol vacío')
        return self.raiz.si

    def sd(self) -> 'ArbolBinario[T]':
        if self.es_vacio():
            raise TypeError('Árbol vacío')
        return self.raiz.sd

    def dato(self) -> T:
        if self.es_vacio():
            raise TypeError('Árbol vacío')
        return self.raiz.dato

    def es_hoja(self) -> bool:
        return not self.es_vacio() and self.si().es_vacio() and self.sd().es_vacio()

    def altura(self) -> int:
        if self.es_vacio():
            return 0
        else:
            return 1 + max(self.si().altura(), self.sd().altura())

    def __len__(self) -> int:
        if self.es_vacio():
            return 0
        else:
            return 1 + len(self.si()) + len(self.sd())
        
    
    def nivel_nodo(self, valor: T, nivel: int = 0) -> int:
        if self.es_vacio():
            return -1
        if self.raiz.dato == valor:
            return nivel
        si_nivel = self.si().nivel_nodo(valor, nivel + 1)
        if si_nivel != -1:
            return si_nivel
        return self.sd().nivel_nodo(valor, nivel + 1)
    
    def __eq__(self, other: 'ArbolBinario[T]') -> bool:
        if self.es_vacio() and other.es_vacio():
            return True
        if self.es_vacio() or other.es_vacio():
            return False
        if self.raiz.dato != other.raiz.dato:
            return False
        return self.si() == other.si() and self.sd() == other.sd()
    



    def recorrido_guiado(self, instrucciones: List[str]) -> Optional[T]:
        if self.es_vacio():
            return None
        if not instrucciones:
            return self.dato()
        if instrucciones[0] == 'izquierda':
            return self.si().recorrido_guiado(instrucciones[1:])
        elif instrucciones[0] == 'derecha':
            return self.sd().recorrido_guiado(instrucciones[1:])
        else:
            raise ValueError(f"Instrucción no válida: {instrucciones[0]}")
        

    '''
    DFS (Depth First Search) siempre se recorre un subárbol completo antes de recorrer el o los restantes.

    Los algoritmos de recorrido en profundidad utilizan recursión múltiple y se apoyan en la pila de ejecución.


    DFS (Depth-First Search): Este tipo de recorrido utiliza una pila 
    (puede ser la pila de la ejecución en el caso de la recursión o una pila explícita en la implementación iterativa)
      para almacenar los nodos que deben ser visitados. DFS explora tan profundo como sea posible a lo largo de cada rama antes de retroceder.
    '''
    def preorder(self, resultado: List[T]):
        if not self.es_vacio():
            resultado.append(self.dato())
            self.si().preorder(resultado)
            self.sd().preorder(resultado)

    def inorder(self, resultado: List[T]):
        if not self.es_vacio():
            self.si().inorder(resultado)
            resultado.append(self.dato())
            self.sd().inorder(resultado)

    def postorder(self, resultado: List[T]):
        if not self.es_vacio():
            self.si().postorder(resultado)
            self.sd().postorder(resultado)
            resultado.append(self.dato())

    
    #inorden con cola
    '''
    
    algoritmo que devuelva el recorrido de un árbol desde las hojas hasta la raíz, y de izquierda a derecha.
    '''
    def bottom_up(self) -> List[T]:
        resultado = []
        self.postorder(resultado)
        return resultado[::-1]  # Invertir la lista para obtener el recorrido de abajo hacia arriba
    
    '''
BFS (Breadth First Search) es completamente diferente a las anteriores, ya que se recorren los nodos de un árbol por niveles. 


Esta estrategia tiene una ventaja respecto al recorrido en profundidad, 
si estuviéramos buscando un nodo que cumpla cierto requisito dentro de un árbol,
 la búsqueda a lo ancho garantiza que se encontrará (si existiera) el nodo correspondiente más cercano a la raíz.



 BFS (Breadth-First Search): Utiliza una cola explícita para almacenar los subárboles que quedan por recorrer. 
 En BFS, los nodos se procesan en el orden en que son descubiertos,
   primero se procesan todos los nodos del nivel actual antes de pasar al siguiente nivel.
'''

    def bfs(self) -> List[T]:
        resultado = []
        def recorrer(q: List['ArbolBinario[T]']):
            if q:
                actual = q.pop(0)  # desencolar árbol visitado
                if not actual.es_vacio():
                    resultado.append(actual.dato())
                    q.append(actual.si())  # encolar subárbol izquierdo
                    q.append(actual.sd())  # encolar subárbol derecho
                recorrer(q)

        q: List['ArbolBinario[T]'] = []
        q.append(self)  # encolar raíz
        recorrer(q)
        return resultado


# Ejemplo de uso
if __name__ == "__main__":
    # Crear un árbol binario con un solo nodo
    arbol = ArbolBinario.crear_nodo(10)

    # Insertar subárboles
    arbol.insertar_si(ArbolBinario.crear_nodo(5))
    arbol.insertar_sd(ArbolBinario.crear_nodo(15))
    arbol.si().insertar_si(ArbolBinario.crear_nodo(3))
    arbol.si().insertar_sd(ArbolBinario.crear_nodo(7))
    arbol.sd().insertar_si(ArbolBinario.crear_nodo(20))
    arbol.sd().insertar_sd(ArbolBinario.crear_nodo(25))


    # Crear otro árbol binario igual
    arbol2 = ArbolBinario.crear_nodo(10)
    arbol2.insertar_si(ArbolBinario.crear_nodo(5))
    arbol2.insertar_sd(ArbolBinario.crear_nodo(15))

    # Obtener el nivel de un nodo
    valor = 7
    nivel = arbol.nivel_nodo(valor)
    print(f"El nivel del nodo con valor {valor} es: {nivel}")

    # Verificar igualdad de árboles
    print(arbol == arbol2)  



    # Recorrido guiado
    instrucciones = ['izquierda', 'derecha']
    contenido = arbol.recorrido_guiado(instrucciones)
    print(f"El contenido del nodo accesible utilizando el camino {' -> '.join(instrucciones)} es: {contenido}")


    

    # Generar listas de recorridos
    preorder_result = []
    arbol.preorder(preorder_result)
    print("Recorrido Preorder:", preorder_result)

    inorder_result = []
    arbol.inorder(inorder_result)
    print("Recorrido Inorder:", inorder_result)

    postorder_result = []
    arbol.postorder(postorder_result)
    print("Recorrido Postorder:", postorder_result)


    # Generar lista del recorrido bottom-up
    bottom_up_result = arbol.bottom_up()
    print("Recorrido Bottom-Up:", bottom_up_result)

     # Recorrido BFS
    bfs_result = arbol.bfs()
    print("Recorrido BFS:", bfs_result)