import itertools
from collections.abc import Iterable
from enum import Enum
from copy import deepcopy

from core.toolkit import log_calls, retry, TimerContext
from random import sample
from typing import Protocol,, TypedDict


# Classe per la gestione di una piccola mappa a quadrati
class Grid(Iterable):
    def __init__(self,n=5):
        ### genera una nuova griglia
        if not isinstance(n, int):
            n = 5
        self._n = n if 9 > n > 1 else 9
        self._agenti = list()

    def is_legal(self,dx, dy):
        x_in = 0 <= dx < self._n
        y_in = 0 <= dy < self._n
        return x_in and y_in

    def __add__(self, other) -> Grid:
        if not isinstance(other, Agent):
            return NotImplemented
        n_grid = type(self)(self._n)
        n_grid._agenti = list(self._agenti)  # shallow copy della lista, non deepcopy degli agenti
        n_grid += other
        return n_grid

    def __iadd__(self, other: Coordinates) -> Grid:
        x, y = other.coordinate()
        if not self.is_legal(x,y):
            raise ValueError(f"Posizione ({x}, {y}) fuori dai limiti della griglia")
        self._agenti.append(other)
        return self

    def __len__(self):
        return self._n ** 2

    def __iter__(self):
        for x in self._agenti:
            yield x

    def __getitem__(self, item):
        # caso dei nomi
        lista_agenti = []
        if isinstance(item, str):
            for i in self._agenti:
                if i._nome == item:
                    lista_agenti.append(i)
        elif isinstance(item, tuple):
            # si tratta di coordinate
            for i in self._agenti:
                if i.coordinate() == item:
                    lista_agenti.append(i)

        else:
            raise TypeError(f"Chiave non supportata: {type(item).__name__}")
        return lista_agenti


    def recap_agenti(self):
        with TimerContext():
            agenti_ord = sorted(self._agenti, key=lambda x: (x._x, x._y))
            for k, v in itertools.groupby(agenti_ord, key=lambda x: (x._x, x._y)):
                print(f'{k} -> {[x._nome for x in v]}')

    def __repr__(self):
        msg = ','.join(f'{x!r}' for x in self._agenti)
        return f'Grid({self._n!r},' + msg + ')'

    def reset(self):
        self._agenti.clear()

    def elimina_agente(self, agente):

        self._agenti.remove(agente)


class Coordinates(Protocol):

    def coordinate(self) -> tuple[int,int]: ...


class AgentState(TypedDict):
    nome: str
    x: int
    y: int
    grid: int


# Classe per implementazione agenti
class Agent:
    def __init__(self, griglia : Grid, nome : str, x: int, y: int):
        self._nome = nome
        self._x , self._y = x, y
        self._grid = griglia
        self._grid += self

    def __eq__(self, other):
        if not isinstance(other, Agent):
            return NotImplemented
        return self._x == other._x and self._y == other._y and self._nome == other._nome

    def __repr__(self):
        return f'Agent({self._nome!r},{self._x!r},{self._y!r})'

    def __hash__(self):
        return hash((self._nome,self._x,self._y))

    def coordinate(self) -> tuple[int, int]:
        return self._x, self._y

    @log_calls
    def cambio_griglia(self, griglia: Grid):
        self._grid.elimina_agente(self)
        if not griglia.is_legal(*self.coordinate()):
            self._x, self._y = 0, 0
        self._grid += self

    @log_calls
    def move(self, mossa):
        dx, dy = mossa[0]+self._x, self._y +mossa[1]
        if self._grid.is_legal(dx,dy):
            self._x, self._y = dx, dy
            return self.coordinate()
        raise ValueError(f"Mossa {mossa} porta fuori dai limiti della griglia")

    @retry(exceptions=(ValueError,))
    def move_casual(self):
        scelta = [(0,1), (0,-1), (1,0), (-1,0)]
        self.move(*sample(scelta,1))

    def serialize(self) -> AgentState:
        return AgentState(nome=self._nome,
                          x=self._x, y=self._y,
                          grid=self._grid._n)






