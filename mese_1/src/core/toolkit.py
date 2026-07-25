import functools
import time
from functools import lru_cache
from contextlib import contextmanager
from dataclasses import dataclass,field
from typing import Callable, Any, Generator, Literal, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')


def timer(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def call(*args: P.args, **kwargs: P.kwargs) -> R:
        t0 = time.perf_counter()
        risultato = func(*args, **kwargs)
        t_f = time.perf_counter() - t0
        print(f'Execution lasted {t_f} seconds')
        return risultato
    return call

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def call(*args: P.args, **kwargs: P.kwargs) -> R:
        risultato = func(*args, **kwargs)
        lista_arg = ' ,'.join(repr(arg) for arg in args)
        lista_kwargs = ' ,'.join(f'{k}={v!r}' for k,v in kwargs.items())
        lista_fin = ' ,'.join(filter(None, [lista_arg, lista_kwargs]))
        print(f'nome_func: {func.__name__},  Args: {lista_fin}, Result: {risultato}')
        return risultato
    return call

def retry(times: int = 3, exceptions: tuple[type[BaseException], ...] = (ValueError,)) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def tentativo(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def esecuzione(*args: P.args, **kwargs: P.kwargs) -> R: # effettuo i tentativi fino a ottenere un risultato
            ult_ecc : BaseException | None = None
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e: # accetta tuple
                    ult_ecc = e
                    print(f'Found exception {type(e).__name__} in trial {i+1}')

            assert ult_ecc is not None
            raise ult_ecc # altrimenti fallisce silenziosamente, meglio di no

        return esecuzione
    return tentativo



def auto_repr[T](cls: type[T]) -> type[T]:

    def n_repr(x: object) -> str:
        lista_attr = [a for a in dir(x)
                      if not callable(getattr(x, a)) and not a.startswith('_')]
        msg = ', '.join(f'{a}={getattr(x,a)!r}' for a in lista_attr)
        msg = f'{type(x).__name__}(' + msg + ')'
        return msg

    cls.__repr__ = n_repr # type: ignore

    return cls

def memoization(func: Callable[P, R]) -> Callable[P, R]:
    registro: dict[tuple[Any, ...], R]= {}
    def corpo(*args: P.args, **kwargs: P.kwargs) -> R:
        chiave= (args, tuple(sorted(kwargs.items()))) # trasformare in tupla ordiata, per non avere ciavi diverse ma equivaleti
        if chiave in registro:
            return registro[chiave]
        res = func(*args, **kwargs)
        registro[chiave] = res
        return res

    return corpo

def memoization_2(func: Callable[P, R]) -> Callable[P, R]:
    @lru_cache
    def corpo(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return corpo # type: ignore[return-value]

class TimerContext:

    def __enter__(self) -> TimerContext:
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type: BaseException, exc_val: int, exc_tb: str) -> Literal[False]:
        elap_time = time.perf_counter() - self.start
        print(f'Tempo esecuzione : {elap_time}')
        # non propagare ulteriormente eccezione
        return False

@contextmanager
def timercontext() -> Generator[float,None, None]:
    t_start = time.perf_counter()
    try:
        yield t_start
    finally:
        print(f'Tempo trascorso: {time.perf_counter() - t_start}')

@dataclass
class FakeResource:
    dati: list[Any] = field(default_factory=list)
    aperta: bool = True

@contextmanager
def gestione_risorse() -> Generator[FakeResource, None, None]:
    risorsa = FakeResource()
    try:
        yield risorsa
    finally:
        risorsa.aperta = False
