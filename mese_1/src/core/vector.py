from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence, Iterator
import math
from typing import overload, Any, SupportsIndex, Protocol, Callable, TypedDict
import itertools


@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    def __eq__(self, other: object) -> bool:
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

    def __radd__(self, other: Vector2D) -> Vector2D:
        # compatibilita per versione built-in sum
        if other == 0:
            return self
        return self + other

    def __mul__(self, other: int | float) -> Vector2D:
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other: int | float) -> Vector2D:
        return self * other

    def __neg__(self) -> Vector2D:
        return Vector2D(- self.x, -self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'Vector2D({self.x!r},{self.y!r})'

    def __str__(self) -> str:
        return f'Vettore di coordinate ( {self.x}, {self.y})'

    def coordinate(self) -> tuple[float,float]:
        return self.x, self.y

class HasCoord(Protocol):
    x: float
    y: float


@dataclass
class Polyline[T: HasCoord](Sequence[T]):
    linea: list[T]

    def __len__(self) -> int:
        return len(self.linea)

    @overload
    def __getitem__(self, item: int) -> T:
        ...
    @overload
    def __getitem__(self, item: slice) -> Polyline[T]:
        ...

    def __getitem__(self, item: int | slice) -> T|Polyline[T]:
        if isinstance(item, slice):
            cls = type(self)
            return cls(self.linea[item])
        return self.linea[item]

    def __setitem__(self, key: SupportsIndex, value: T) -> None:
        self.linea[key] = value

    def distanze(self) -> Iterator[float]:
        for i in range(len(self) - 1):
            x_dist = (self[i + 1].x - self[i].x) ** 2
            y_dist = (self[i + 1].y - self[i].y) ** 2
            yield math.sqrt(x_dist + y_dist)


class FibonacciIterator:
    def __init__(self) -> None:
        self.f1 = 0
        self.f2 = 1

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        res = self.f1
        self.f1, self.f2 = self.f2, self.f1 + self.f2
        return res

def fib_generator(stop: int) -> Iterator[int]:
    f1, f2 = 0, 1
    for x in range(stop):
        yield f1
        f1, f2 = f2, f1 + f2

import sys
from random import randint
import itertools as it

def gen_multisource(*iterabili: Sequence[Any]) -> Iterator[Any]:
    # controllo che tutti gli elementi implementino un iteratore
    # non prevedere eccezione ma catturarla al momento opportuno
    # delego ad ogni iteratore
    for ite in iterabili:
        try:
            yield from ite
        except TypeError:
            raise TypeError(f'{ite!r} not iterable!') from None

# generatore infinito
class GenInfinito:

    def __iter__(self) -> Iterator[tuple[int, int,int]]:
        while True:
            a,b,c = randint(1,6), randint(1,6), randint(1,6)
            yield a,b,c
# utilizzo
for ex in it.islice(GenInfinito(), 2, 4):
    print(ex)


lista = [x**2 for x in range(1_000_000)]
generatore = (x**2 for x in range(1_000_000))

print(sys.getsizeof(lista))       # dell'ordine di diversi MB
print(sys.getsizeof(generatore))  # poche decine di byte, costante


# generazione dataset

categorie = ['film', 'libro', 'libro', 'film', 'film']
titoli = ['ubot15', 'ubot15', 'michi17', 'michi17','valerio']
valori = [5,3,2,2,1]

class RigaDataset(TypedDict):
    categoria: str
    titolo: str
    valore: int

dataset: list[RigaDataset] = [
    {'categoria': categorie[i], 'titolo': titoli[i], 'valore': valori[i]}
    for i in range(5)
]
# group by
# richiede ordinamento preventivo per chiave
ordinamento: Callable[[RigaDataset], str] = lambda x: x['categoria']
dataset_ordinato = sorted(dataset, key=ordinamento)
# g iteratore, per visualizzare lo metti in una lista, attenzione che viene consumato
for k, g in it.groupby(dataset_ordinato, key=ordinamento):
    print(f' {k} --> {list(g)}')

# islice

for x in it.islice(dataset, 1, 4):
    print(x)
import operator
# accumulate genera un iteratore da utilizzare
accumulo = list(it.accumulate(valori, operator.add))
for i in accumulo:
    print(i)



