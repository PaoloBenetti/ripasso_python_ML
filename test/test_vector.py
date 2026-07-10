from core.vector import Vector2D, Polyline
import pytest
import dataclasses

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
