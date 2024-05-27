from typing import Generic, TypeVar, List
from functools import reduce

T = TypeVar('T')

class ArbolN(Generic[T]):
    def __init__(self, dato: T):
        self._dato: T = dato
        self._subarboles: List[ArbolN[T]] = []
       
    @property
    def dato(self) -> T:
        return self._dato

    @dato.setter
    def dato(self, valor: T):
        self._dato = valor

    @property
    def subarboles(self) -> "List[ArbolN[T]]":
        return self._subarboles
    
    @subarboles.setter
    def subarboles(self, subarboles: "List[ArbolN[T]]"):
        self._subarboles = subarboles

    def insertar_subarbol(self, subarbol: "ArbolN[T]"):
        self.subarboles.append(subarbol)

    def es_hoja(self) -> bool:
        return self.subarboles == []
    
    def altura(self) -> int:
        def altura_n(bosque: List[ArbolN[T]]) -> int:
            if not bosque:
                return 0
            else:
                return max(bosque[0].altura(), altura_n(bosque[1:]))
        
        return 1 + altura_n(self.subarboles)
        
    def __len__(self) -> int:
        if self.es_hoja():
            return 1
        else:
            return 1 + sum([len(subarbol) for subarbol in self.subarboles])

    def __str__(self):
        def mostrar(t: ArbolN[T], nivel: int):
            tab = '.' * 4
            indent = tab * nivel
            out = indent + str(t.dato) + '\n'
            for subarbol in t.subarboles:
                out += mostrar(subarbol, nivel + 1)
            return out
            
        return mostrar(self, 0)

    def preorder(self) -> List[T]:
        return reduce(lambda recorrido, subarbol: recorrido + subarbol.preorder(), self.subarboles, [self.dato])

    def preorder2(self) -> List[T]:
        recorrido = [self.dato]
        for subarbol in self.subarboles:
            recorrido += subarbol.preorder2()
        return recorrido
    
    def preorder3(self) -> List[T]:
        def preorder_n(bosque: List[ArbolN[T]]) -> List[T]:
            return [] if not bosque else bosque[0].preorder3() + preorder_n(bosque[1:])
        return [self.dato] + preorder_n(self.subarboles)
    
    def __eq__(self, otro: "ArbolN[T]") -> bool:
        if self.dato != otro.dato:
            return False
        if len(self.subarboles) != len(otro.subarboles):
            return False
        return all(a == b for a, b in zip(self.subarboles, otro.subarboles))

    def bfs(self) -> List[T]:
        resultado = []
        cola = [self]
        while cola:
            actual = cola.pop(0)
            resultado.append(actual.dato)
            cola.extend(actual.subarboles)
        return resultado
    
    def posorder(self) -> List[T]:
        resultado = []
        for subarbol in self.subarboles:
            resultado += subarbol.posorder()
        resultado.append(self.dato)
        return resultado

    def nivel(self, x: T) -> int:
        def nivel_n(bosque: List[ArbolN[T]], x: T, nivel_actual: int) -> int:
            for subarbol in bosque:
                if subarbol.dato == x:
                    return nivel_actual + 1
                nivel_encontrado = nivel_n(subarbol.subarboles, x, nivel_actual + 1)
                if nivel_encontrado != -1:
                    return nivel_encontrado
            return -1

        if self.dato == x:
            return 0
        return nivel_n(self.subarboles, x, 0)

    def copy(self) -> "ArbolN[T]":
        nuevo_arbol = ArbolN(self.dato)
        nuevo_arbol.subarboles = [subarbol.copy() for subarbol in self.subarboles]
        return nuevo_arbol
    
    def sin_hojas(self) -> "ArbolN[T]":
        if self.es_hoja():
            return None
        nuevo_arbol = ArbolN(self.dato)
        nuevo_arbol.subarboles = [subarbol.sin_hojas() for subarbol in self.subarboles if not subarbol.es_hoja()]
        return nuevo_arbol
    
    def recorrido_guiado(self, direcciones: List[int]) -> T:
        actual = self
        for direccion in direcciones:
            if direccion < 0 or direccion >= len(actual.subarboles):
                raise IndexError("Dirección fuera de rango")
            actual = actual.subarboles[direccion]
        return actual.dato

def main():
    t = ArbolN(1)
    n2 = ArbolN(2)
    n3 = ArbolN(3)
    n4 = ArbolN(4)
    n5 = ArbolN(5)
    n6 = ArbolN(6)
    n7 = ArbolN(7)
    n8 = ArbolN(8)
    n9 = ArbolN(9)
    t.insertar_subarbol(n2)
    t.insertar_subarbol(n3)
    t.insertar_subarbol(n4)
    n2.insertar_subarbol(n5)
    n2.insertar_subarbol(n6)
    n4.insertar_subarbol(n7)
    n4.insertar_subarbol(n8)
    n7.insertar_subarbol(n9)
    
    print(t)

    print(f'Altura: {t.altura()}')
    print(f'Nodos: {len(t)}')

    print(f'BFS: {t.bfs()}')
    print(f'DFS preorder : {t.preorder()}')
    print(f'DFS preorder2: {t.preorder2()}')
    print(f'DFS preorder3: {t.preorder3()}')
    print(f'DFS posorder: {t.posorder()}')

    print(f'Nivel de 9: {t.nivel(9)}')
    print(f'Nivel de 13: {t.nivel(13)}')

    t2 = t.copy()
    t3 = t2.sin_hojas()
    print(t)
    print(t2)
    print(t3)
    print(f't == t2 {t == t2}')

    print(f'recorrido_guiado [2,0,0]: {t2.recorrido_guiado([2,0,0])}')

if __name__ == '__main__':
    main()
