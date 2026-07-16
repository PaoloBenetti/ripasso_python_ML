from core.toolkit import timer, log_calls

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
