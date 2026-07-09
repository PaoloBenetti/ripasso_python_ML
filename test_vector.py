from core.vector import Vector2D
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