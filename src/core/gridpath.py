import itertools
import math
import asyncio
import aiohttp
from collections.abc import Iterable
from time import sleep
from threading import Thread
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

from aiohttp import ClientTimeout

from core.vector import Vector2D
from core.toolkit import log_calls, retry, TimerContext, timer
from random import sample
from typing import Protocol, overload, TypedDict, Self, Generator

import typer

app = typer.Typer()

@app.callback()
def callback() -> None:
    """Gridpath CLI - simulazione di agenti su griglia."""
    pass


# Classe per la gestione di una piccola mappa a quadrati
class Grid(Iterable["Agent"]):
    def __init__(self,n: int=5) -> None:
        ### genera una nuova griglia
        if not isinstance(n, int):
            n = 5
        self._n = n if 9 > n > 1 else 9
        self._agenti: list[Agent] = []

    def is_legal(self,dx: int, dy: int) -> bool:
        x_in = 0 <= dx < self._n
        y_in = 0 <= dy < self._n
        return x_in and y_in

    def __add__(self, other: Agent) -> Grid:
        if not self.is_legal(other._x, other._y):
            raise ValueError(f"Posizione ({other._x}, {other._y}) fuori dai limiti della griglia")
        self._agenti.append(other)
        n_grid = type(self)(self._n)
        n_grid._agenti = list(self._agenti)  # shallow copy della lista, non deepcopy degli agenti
        n_grid += other
        return n_grid

    def __iadd__(self, other: Agent) -> Grid:
        x, y = other.coordinate()
        if not self.is_legal(x,y):
            raise ValueError(f"Posizione ({x}, {y}) fuori dai limiti della griglia")
        self._agenti.append(other)
        return self

    def __len__(self) -> int:
        return self._n ** 2

    def __iter__(self) -> Generator[Agent, None, None]:
        for x in self._agenti:
            yield x

    def __getitem__(self, item: str | tuple[int, int]) -> list[Agent]:
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


    def recap_agenti(self) -> None:
        with TimerContext():
            agenti_ord = sorted(self._agenti, key=lambda x: (x._x, x._y))
            for k, v in itertools.groupby(agenti_ord, key=lambda x: (x._x, x._y)):
                print(f'{k} -> {[x._nome for x in v]}')

    def __repr__(self) -> str:
        msg = ','.join(f'{x!r}' for x in self._agenti)
        return f'Grid({self._n!r},' + msg + ')'

    def reset(self) -> None:
        self._agenti.clear()

    def elimina_agente(self, agente: Agent) -> None:

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

    def __eq__(self, other:object) -> bool:
        if not isinstance(other, Agent):
            return NotImplemented
        return self._x == other._x and self._y == other._y and self._nome == other._nome

    def __repr__(self) -> str:
        return f'Agent({self._nome!r},{self._x!r},{self._y!r})'

    def __hash__(self) -> int:
        return hash((self._nome,self._x,self._y))

    def coordinate(self) -> tuple[int, int]:
        return self._x, self._y

    @log_calls
    def cambio_griglia(self, griglia: Grid) -> None:
        self._grid.elimina_agente(self)
        if not griglia.is_legal(*self.coordinate()):
            self._x, self._y = 0, 0
        self._grid += self

    @log_calls
    def move(self, mossa: tuple[int, int]) -> tuple[int,int]:
        dx, dy = mossa[0]+self._x, self._y +mossa[1]
        if self._grid.is_legal(dx,dy):
            self._x, self._y = dx, dy
            return self.coordinate()
        raise ValueError(f"Mossa {mossa} porta fuori dai limiti della griglia")


    def move_casual(self) -> None:
        scelta = [(0,1), (0,-1), (1,0), (-1,0)]
        self.move(*sample(scelta,1))

    def serialize(self) -> AgentState:
        return AgentState(nome=self._nome,
                          x=self._x, y=self._y,
                          grid=self._grid._n)


def download_res(tempo: int) -> None:
    sleep(tempo)

@timer
def scarica_risorse(tempi: list[int]) -> None:
    for t in tempi:
        download_res(t)
        print(f'finito {t} secondi')

@timer
def scarica_res_th(tempi: list[int]) -> None:
    lista_thread = []
    for t in tempi:
        th = Thread(target=download_res, args=(t,))
        th.start()
        lista_thread.append(th)
        print(f'finito {t} secondi')
    for th in lista_thread:
        th.join()

@timer
def scarica_res_pool(tempi: list[int]) -> None:
    with ThreadPoolExecutor(max_workers=2) as esecutore:
        finali = [esecutore.submit(download_res, t) for t in tempi]
        for futuro in as_completed(finali):
            eccezione = futuro.exception()
            if eccezione is not None:
                print(f'Rilevata eccezione: {type(eccezione).__name__}')


def pezzo_dist(x: tuple[Vector2D,Vector2D]) -> float:
    a,b = x
    return math.sqrt((a.x -b.x)**2 + (a.y-b.y)**2)

@timer
def calcola_dist(lista_vet:list[Vector2D]) -> float:
    combinazioni = list(itertools.combinations(lista_vet,2))
    somma = 0.0
    for x in combinazioni:
        somma += pezzo_dist(x)
    return somma

def somma_blocco(blocco: list[tuple[Vector2D, Vector2D]]) -> float:
    return sum(pezzo_dist(x) for x in blocco)

@timer
def calcola_dist_pool(lista_vet: list[Vector2D]) -> float:
    combinazioni = list(itertools.combinations(lista_vet, 2))
    n_workers = 4
    dim_blocco = len(combinazioni) // n_workers + 1
    blocchi = [combinazioni[i:i+dim_blocco] for i in range(0, len(combinazioni), dim_blocco)]
    with Pool(processes=n_workers) as pool:
        risultati = pool.map(somma_blocco, blocchi)
    return sum(risultati)

async def attesa(t_star: int)-> bool:
    await asyncio.sleep(t_star)
    return True

async def gestione_risorse(lista_tempi: list[int]) -> None:
    lista_task = [attesa(i) for i in lista_tempi]
    lista_risposte = await asyncio.gather(*lista_task)
    print(lista_risposte)

async def scraper_semplice(lista_url: list[str]) -> None:
    async with aiohttp.ClientSession() as client:
        lista_compiti = [fetcher(client, u) for u in lista_url]
        lista_risposte = await asyncio.gather(*lista_compiti,return_exceptions=True )
        for futuro in lista_risposte:
            if isinstance(futuro, Exception):
                print(f'Rilevata eccezione: {type(futuro).__name__}')
            else:
                print(f'Ricevuti {type(futuro)} caratteri')


async def fetcher(client: aiohttp.ClientSession, url: str, timeout: int = 60) -> str:
    async with client.get(url, timeout=ClientTimeout(timeout)) as resp:
        resp.raise_for_status()
        msg = await resp.text()
    return msg


def muovi_casual(a: Agent, n_mosse: int) -> tuple[tuple[int,int], int]:
    errori: int = 0
    for _ in range(n_mosse):
        try:
            a.move_casual()
        except ValueError as e:
            errori += 1
    dx, dy = a.coordinate()
    return (dx,dy), errori


def montecarlo_grid(g: Grid, n_agenti: int, n_mosse: int) -> tuple[dict[tuple[int,int], int], int]:
    dist_pos: dict[tuple[int, int], int] = {}
    errori: int = 0

    # creazione agenti
    centro: int = g._n // 2
    for i in range(n_agenti):
        _ = Agent(g, str(i), centro, centro)
    # preparazione sim

    for a in g:
        pos, er = muovi_casual(a,n_mosse)
        errori += er
        if pos in dist_pos.keys():
            dist_pos[pos] += 1
        else:
            dist_pos[pos] = 1

    return dist_pos, errori

@app.command()
def montecarlo(n: int, dim: int, n_agenti: int, n_mosse: int) -> tuple[dict[tuple[int,int], int], int]:
    dist_pos : dict[tuple[int,int], int] = {}
    errori : int = 0

    # fase 1: creazione elementi
    lista_g : list[Grid] = [Grid(dim) for _ in range(n)]
    # fase 2: avvio sim
    with ProcessPoolExecutor(max_workers=4) as pl:
        for d_p, er in pl.map(montecarlo_grid, lista_g, [n_agenti for _ in range(n)], [n_mosse for _ in range(n)]):
            errori += er
            if len(dist_pos) == 0:
                dist_pos = d_p
            else:
                for k in d_p.keys():
                    if k in dist_pos:
                        dist_pos[k] += d_p[k]
                    else:
                        dist_pos[k] = d_p[k]

    # fase 3: raccolta statistiche
    print(errori)
    print(dist_pos)
    return dist_pos, errori

if __name__ == "__main__":
    app()

