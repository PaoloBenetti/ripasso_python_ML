from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence


@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    def __eq__(self, other:Vector2D) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other:Vector2D) -> Vector2D: #versione semplice
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    '''
    def __add__(self, other): versione n dim
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector2D(a+b for a,b in pairs)
        except TypeError:
            return NotImplemented
    '''

    def __radd__(self, other) -> Vector2D:
        # compatibilita per versione built-in sum
        if other == 0:
            return self
        return self + other

    def __mul__(self, other: int | float) -> Vector2D:
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other) -> Vector2D:
        return self * other

    def __neg__(self) -> Vector2D:
        return Vector2D(- self.x, -self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'Vector2D({self.x!r},{self.y!r})'

    def __str__(self) -> str:
        return f'Vettore di coordinate ( {self.x}, {self.y})'

@dataclass
class Polyline(Sequence):
    linea: list[Vector2D]

    def __len__(self) -> int:
        return len(self.linea)

    def __getitem__(self, item: int|slice) -> Vector2D|Polyline:
        if isinstance(item, slice):
            cls = type(self)
            return cls(self.linea[item])
        return self.linea[item]

    def __setitem__(self, key: int[slice], value: Vector2D|list[Vector2D]) -> None:
        if not isinstance(value, Vector2D): # in fase ottimizzazione gli assert spariscono
            raise TypeError(f"Expected Vector2D, got {type(value).__name__}")
        self.linea[key] = value

class FibonacciIterator:
    def __init__(self):
        self.f1 = 0
        self.f2 = 1

    def __iter__(self):
        return self

    def __next__(self):
        res = self.f1
        self.f1, self.f2 = self.f2, self.f1 + self.f2
        return res

def fib_generator(stop):
    f1, f2 = 0, 1
    for x in range(stop):
        yield f1
        f1, f2 = f2, f1 + f2


import itertools as it
# generazione dataset
dataset = []
categorie = ['film', 'libro', 'libro', 'film', 'film']
titoli = ['ubot15', 'ubot15', 'michi17', 'michi17','valerio']
valori = [5,3,2,2,1]
for i in range(5):
    pippo = {'categoria': categorie[i], 'titolo': titoli[i], 'valore': valori[i]}
    dataset.append(pippo)
# group by
# richiede ordinamento preventivo per chiave
dataset_ordinato = sorted(dataset, key=lambda x: x['categoria'])
# g iteratore, per visualizzare lo metti in una lista, attenzione che viene consumato
for k, g in it.groupby(dataset_ordinato, key=lambda x : x['categoria']):
    print(f' {k} --> {list(g)}')

# islice

for x in it.islice(dataset, 1, 4):
    print(x)
import operator
# accumulate genera un iteratore da utilizzare
accumulo = list(it.accumulate(valori, operator.add))
for i in accumulo:
    print(i)

