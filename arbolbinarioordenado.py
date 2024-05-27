from typing import TypeVar, Optional, Protocol, Tuple
from arboles import ArbolBinario, NodoAB

# Definimos un protocolo para tipos comparables
class Comparable(Protocol):
    def __lt__(self: 'T', otro: 'T') -> bool: ...
    def __le__(self: 'T', otro: 'T') -> bool: ...
    def __gt__(self: 'T', otro: 'T') -> bool: ...
    def __ge__(self: 'T', otro: 'T') -> bool: ...
    def __eq__(self: 'T', otro: 'T') -> bool: ...
    def __ne__(self: 'T', otro: 'T') -> bool: ...

# Definimos una variable de tipo que está limitada a tipos que implementan Comparable
T = TypeVar('T', bound=Comparable)

# Nodo para el árbol binario ordenado
class NodoABO(NodoAB[T]):
    def __init__(self, dato: T):
        super().__init__(dato, ArbolBinarioOrdenado(), ArbolBinarioOrdenado())
    
    def __lt__(self, otro: "NodoABO[T]") -> bool:
        return isinstance(otro, NodoABO) and self.dato < otro.dato
    
    def __gt__(self, otro: "NodoABO[T]") -> bool:
        return isinstance(otro, NodoABO) and self.dato > otro.dato

    def __eq__(self, otro: "NodoABO[T]") -> bool:
        return isinstance(otro, NodoABO) and self.dato == otro.dato

# Árbol binario ordenado
class ArbolBinarioOrdenado(ArbolBinario[T]):
    @staticmethod
    def crear_nodo(dato: T) -> "ArbolBinarioOrdenado[T]":
        nuevo = ArbolBinarioOrdenado()
        nuevo.set_raiz(NodoABO(dato))
        return nuevo
    
    def es_ordenado(self) -> bool:
        def es_ordenado_interna(
            arbol: "ArbolBinarioOrdenado[T]", 
            minimo: Optional[T] = None, 
            maximo: Optional[T] = None
        ) -> bool:
            if arbol.es_vacio():
                return True
            if (minimo is not None and arbol.dato() <= minimo) or (maximo is not None and arbol.dato() >= maximo):
                return False
            return es_ordenado_interna(arbol.si(), minimo, arbol.dato()) and es_ordenado_interna(arbol.sd(), arbol.dato(), maximo)
        
        return es_ordenado_interna(self)
    
    def es_hoja(self) -> bool:
        return self.si().es_vacio() and self.sd().es_vacio()
    
    def insertar_si(self, arbol: "ArbolBinarioOrdenado[T]"):
        si = self.si()
        super().insertar_si(arbol)
        if not self.es_ordenado():
            super().insertar_si(si)
            raise ValueError("El árbol a insertar no es ordenado o viola la propiedad de orden del árbol actual")
    
    def insertar_sd(self, arbol: "ArbolBinarioOrdenado[T]"):
        sd = self.sd()
        super().insertar_sd(arbol)
        if not self.es_ordenado():
            super().insertar_sd(sd)
            raise ValueError("El árbol a insertar no es ordenado o viola la propiedad de orden del árbol actual")
    
    def insertar(self, valor: T):
        if self.es_vacio():
            self.set_raiz(NodoABO(valor))
        elif valor == self.dato():
            raise ValueError("No se admiten repetidos!")
        elif valor < self.dato():
            self.si().insertar(valor)
        else:
            self.sd().insertar(valor)

    def pertenece(self, valor: T) -> bool:
        def buscar_interna(arbol: "ArbolBinarioOrdenado[T]") -> bool:
            if arbol.es_vacio():
                return False
            elif valor == arbol.dato():
                return True
            return buscar_interna(arbol.si()) or buscar_interna(arbol.sd())
        
        return buscar_interna(self)
    
    def max(self) -> "ArbolBinarioOrdenado[T]":
        if self.es_vacio():
            raise ValueError("El árbol no tiene elementos")
        elif not self.sd().es_vacio():
            return self.sd().max()
        else:
            return self

    def max_con_pred(self) -> Tuple[Optional["ArbolBinarioOrdenado[T]"], Optional["ArbolBinarioOrdenado[T]"]]:
        if self.es_vacio():
            return None, None
        elif self.sd().es_vacio():
            return self, None
        elif self.sd().sd().es_vacio():
            return self.sd(), self
        else:
            return self.sd().max_con_pred()

    def eliminar(self, valor: T) -> None:
        if self.es_vacio():
            return
        elif self.dato() == valor:
            if self.es_hoja():
                self.raiz = None
            elif not self.sd().es_vacio() and not self.si().es_vacio():
                self.si().max().insertar_sd(self.sd())
                self.raiz = self.si().raiz
            elif not self.si().es_vacio():
                self.raiz = self.si().raiz
            else:
                self.raiz = self.si().raiz
        elif self.dato() < valor:
            self.sd().eliminar(valor)
        else:
            self.si().eliminar(valor)

    def __str__(self) -> str: 
        def recorrer(t:ArbolBinario[T], nivel:int) -> str:
            tab = '.' * 4 * nivel
            if t.es_vacio():
                return tab + 'AV\n' # Árbol Vacío (AV)
            else:
                tab += str(t.dato()) + "\n"
                tab += recorrer(t.si(),nivel+1)
                tab += recorrer(t.sd(),nivel+1)
                return tab
        return recorrer(self,0)

# Función principal para probar el funcionamiento del árbol binario ordenado
def main():
    t: ArbolBinarioOrdenado[int] = ArbolBinarioOrdenado()
    t.insertar(10)
    t.insertar(5)
    t.insertar(15)
    t.insertar(2)
    t.insertar(7)
    t.insertar(12)
    t.insertar(17)
    t.insertar(20)
    t.insertar(13)
    print(t.es_ordenado())
    print(t)

    t2: ArbolBinarioOrdenado[int] = ArbolBinarioOrdenado()
    t2.insertar(8)
    # t2.insertar(11)  # Descomentar para probar la excepción al violar el orden
    t2.insertar(6)
    t.insertar_si(t2)
    print(t)
    print(f'Ordenado?: {t.es_ordenado()}')

    print(f'Tiene 10: {t.pertenece(10)}')

    print("se elimino")
    t.eliminar(10)
    print(t)

if __name__ == "__main__":
    main()
