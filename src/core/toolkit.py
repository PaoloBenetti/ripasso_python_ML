import functools
import time
from functools import lru_cache
from contextlib import contextmanager

def timer(func):
    @functools.wraps(func)
    def call(*args, **kwargs):
        t0 = time.perf_counter()
        risultato = func(*args, **kwargs)
        t_f = time.perf_counter() - t0
        print(f'Execution lasted {t_f} seconds')
        return risultato
    return call

def log_calls(func):
    @functools.wraps(func)
    def call(*args, **kwargs):
        risultato = func(*args, **kwargs)
        lista_arg = ' ,'.join(repr(arg) for arg in args)
        lista_kwargs = ' ,'.join(f'{k}={v!r}' for k,v in kwargs.items())
        lista_fin = ' ,'.join(filter(None, [lista_arg, lista_kwargs]))
        print(f'nome_func: {func.__name__},  Args: {lista_fin}, Result: {risultato}')
        return risultato
    return call

def retry(times=3, exceptions=(ValueError,)):
    def tentativo(func):
        @functools.wraps(func)
        def esecuzione(*args, **kwargs): # effettuo i tentativi fino a ottenere un risultato
            ult_ecc = None
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e: # accetta tuple
                    ult_ecc = e
                    print(f'Found exception {type(e).__name__} in trial {i+1}')

            raise ult_ecc # altrimenti fallisce silenziosamente, meglio di no

        return esecuzione
    return tentativo

def auto_repr(cls):

    def n_repr(x):
        lista_attr = [a for a in dir(x)
                      if not callable(getattr(x, a)) and not a.startswith('_')]
        msg = ', '.join(f'{a}={getattr(x,a)!r}' for a in lista_attr)
        msg = f'{type(x).__name__}(' + msg + ')'
        return msg

    cls.__repr__ = n_repr

    return cls

def memoization(func):
    registro = {}
    def corpo(*args, **kwargs):
        chiave = (args, tuple(sorted(kwargs.items()))) # trasformare in tupla ordiata, per non avere ciavi diverse ma equivaleti
        if chiave in registro:
            return registro[chiave]
        res = func(*args, **kwargs)
        registro[chiave] = res
        return res

    return corpo

def memoization_2(func):
    @lru_cache
    def corpo(*args, **kwargs):

        return func(*args, **kwargs)

    return corpo

class TimerContext:

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elap_time = time.perf_counter() - self.start
        print(f'Tempo esecuzione : {elap_time}')
        # non propagare ulteriormente eccezione
        return False

@contextmanager
def timercontext():
    t_start = time.perf_counter()
    try:
        yield t_start
    finally:
        print(f'Tempo trascorso: {time.perf_counter() - t_start}')
