import inspect

from core.toolkit import timer, log_calls, retry, auto_repr, memoization
import pytest

def test_timer_preserva_meta():
    @timer
    def somma(a,b):
        """Somma due numeri"""
        return a+b

    assert somma.__name__ == 'somma'
    assert somma.__doc__ == "Somma due numeri"

def test_timer_res_corretto():
    @timer
    def somma(a, b):
        """Somma due numeri"""
        return a + b
    assert somma(2,3) == 5

def test_timer_supporta_kwargs():
    @timer
    def saluta(nome, saluto="Ciao"):
        return f"{saluto}, {nome}!"
    assert saluta("Marco", saluto="Salve") == "Salve, Marco!"

def test_log_res_corretto():
    @timer
    def somma(a, b):
        """Somma due numeri"""
        return a + b

    assert somma(2,3) == 5

@auto_repr
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def test_auto_repr_contiene_nome_classe_e_attributi():
    p = Punto(1, 2)
    assert repr(p) == "Punto(x=1, y=2)"

def test_retry_ritorna_risultato_dopo_fallimenti_transitori():
    calls = {"count": 0}
    @retry(times=3, exceptions=(ValueError,))
    def flaky():
        calls["count"] += 1
        if calls["count"] < 3:
            raise ValueError("fallisce apposta")
        return "ok"
    assert flaky() == "ok"
    assert calls["count"] == 3

def test_retry_rilancia_dopo_aver_esaurito_i_tentativi():
    @retry(times=2, exceptions=(ValueError,))
    def sempre_fallisce():
        raise ValueError("nope")
    with pytest.raises(ValueError):
        sempre_fallisce()

def test_retry_rispetta_il_parametro_times():
    calls = {"count": 0}
    @retry(times=2, exceptions=(ValueError,))
    def sempre_fallisce():
        calls["count"] += 1
        raise ValueError("nope")
    with pytest.raises(ValueError):
        sempre_fallisce()
    assert calls["count"] == 2  # non 3: verifica che `times` sia rispettato

def test_retry_non_intercetta_eccezioni_non_previste():
    calls = {"count": 0}
    @retry(times=3, exceptions=(ValueError,))
    def solleva_type_error():
        calls["count"] += 1
        raise TypeError("imprevisto")
    with pytest.raises(TypeError):
        solleva_type_error()
    assert calls["count"] == 1  # non deve ritentare su un'eccezione non prevista

def test_memoi_restituzioe_risutato():
    @memoization
    def somma(a, b):
        """Somma due numeri"""
        return a + b
    info = inspect.getclosurevars(somma).nonlocals
    assert len(info['registro']) == 0
    tmp_1 = somma(2,3)
    assert tmp_1 == 5
    tmp = somma(1,2)
    info = inspect.getclosurevars(somma).nonlocals
    assert len(info['registro']) == 2
    tmp = somma(2,3)
    info = inspect.getclosurevars(somma).nonlocals
    assert len(info['registro']) == 2
    assert tmp == tmp_1

def test_memoi_kwargs():
    @memoization
    def somma(a, b):
        """Somma due numeri"""
        return a + b
    tmp = somma(2,b=3)
    tmp_2 = somma(2,b=10)
    assert tmp != tmp_2
