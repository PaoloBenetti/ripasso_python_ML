import functools
import time

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

