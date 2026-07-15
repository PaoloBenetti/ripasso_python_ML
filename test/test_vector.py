from core.vector import Vector2D, Polyline, FibonacciIterator, fib_generator, GenInfinito, gen_multisource
import pytest
import dataclasses
from itertools import islice
import inspect

def test_uguaglianza_e_com():
    assert Vector2D(2,2) == Vector2D(2,2)
    assert Vector2D(2,3) != Vector2D(2,2)
    assert (Vector2D(2,2) == 23) is False
    assert (Vector2D(2,2) == 'ciaone') is False

def test_repr(): # deve verificare che il test faccia quanto pattuito, una stringa uivoca
    v1 = Vector2D(1,2)
    assert repr(v1) == 'Vector2D(1,2)'


def test_hash(): # gli hash di due uguali devono essere uguali
    v1 , v2 = Vector2D(1,2), Vector2D(1,2)
    assert hash(v1) == hash(v2)

def test_frozen(): # verifica immutabilita
    v1 = Vector2D(1,2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        v1.x = 89

def test_add_onlyvec():
    v1 = Vector2D(1,2)
    with pytest.raises(TypeError):
        x = v1 + 6

def test_mul_onlyvec():
    v1 = Vector2D(1,2)
    with pytest.raises(TypeError):
        x = v1 * 'ciao'

def test_vec_add():
    v1 , v2 = Vector2D(1,2), Vector2D(1,2)
    v3 = Vector2D(2,4)
    assert (v3 == (v1 + v2))

def test_vec_mult():
    v1, s = Vector2D(1, 2), 3
    res = Vector2D(3, 6)
    assert (res == (v1 * s))

def test_vec_neg():
    v1 = Vector2D(1,2)
    vr = Vector2D(-1, -2)
    assert vr == -v1

def test_add_sum():
    lista = [Vector2D(1,2), Vector2D(1,2), Vector2D(1,3)]
    res = sum(lista)
    assert res == Vector2D(3,7)

def test_poly_exist():
    ingresso = [Vector2D(1,1), Vector2D(12,2)]
    pippo = Polyline(ingresso)
    assert isinstance(pippo, Polyline)

def test_poly_len():
    ingresso = [Vector2D(1, 1), Vector2D(12, 2)]
    pippo = Polyline(ingresso)
    assert (len(pippo) == 2)

def test_poly_get_set():
    ingresso = [Vector2D(1, 1), Vector2D(12, 2)]
    pippo = Polyline(ingresso)
    assert (pippo[1] == Vector2D(12, 2))
    pippo[0] = Vector2D(2, 2)
    assert (pippo[0] == Vector2D(2, 2))

def test_poly_iter():
    ingresso = [Vector2D(1, 1), Vector2D(12, 2)]
    pippo = Polyline(ingresso)
    # Polyline non ha __iter__: qui verifico che il fallback di Python
    # su __getitem__ (indice crescente finché non arriva IndexError) funzioni
    risultato = list(pippo)
    assert risultato == ingresso

def test_poly_slice_ritorna_polyline():
    ingresso = [Vector2D(1, 1), Vector2D(2, 2), Vector2D(3, 3)]
    pippo = Polyline(ingresso)
    sotto = pippo[0:2]
    assert isinstance(sotto, Polyline) # verifico che la classe sia giust
    assert sotto.linea == [Vector2D(1, 1), Vector2D(2, 2)] # verifico contenuto

def test_poly_index_out_of_range():
    pippo = Polyline([Vector2D(4, 1)])
    with pytest.raises(IndexError):
        pippo[5]

def test_poly_in():
    ingresso = [Vector2D(1, 1), Vector2D(2, 2), Vector2D(3, 3)]
    pippo = Polyline(ingresso)
    assert Vector2D(1, 1) in pippo
    assert Vector2D(0, 1) not in pippo

def test_poly_index():
    ingresso = [Vector2D(1, 1), Vector2D(2, 2), Vector2D(3, 3)]
    pippo = Polyline(ingresso)
    assert pippo.index(Vector2D(3, 3)) == 2

def test_poly_count():
    ingresso = [Vector2D(1, 1), Vector2D(1, 1), Vector2D(3, 3)]
    pippo = Polyline(ingresso)
    assert pippo.count(Vector2D(1, 1)) == 2

def test_poly_reversed():
    ingresso = [Vector2D(1, 1), Vector2D(2, 2), Vector2D(3, 3)]
    pippo = Polyline(ingresso)
    assert list(reversed(pippo)) == [Vector2D(3, 3), Vector2D(2, 2), Vector2D(1, 1)]


def test_fib_lista():
    fin = FibonacciIterator()
    gen = list(islice(fin, 8))
    assert gen == [0,1,1,2,3,5,8,13]

def test_fib_gen():
    gen = [x for x in fib_generator(8)]
    assert gen == [0,1,1,2,3,5,8,13]

def test_fib_gen_e_generatore():
    gen = fib_generator(8)
    assert inspect.isgenerator(gen)

def test_gen_infinito_produce_generatori_indipendenti():
    g = GenInfinito()
    iteratore1 = iter(g)
    iteratore2 = iter(g)
    assert iteratore1 is not iteratore2

def test_multisource_combina_in_ordine():
    risultato = list(gen_multisource([1, 2], (3, 4), range(5, 7)))
    assert risultato == [1, 2, 3, 4, 5, 6]

def test_multisource_con_non_iterabile_solleva_typeerror():
    with pytest.raises(TypeError):
        list(gen_multisource([1, 2], 42))  # 42 non è iterabile
