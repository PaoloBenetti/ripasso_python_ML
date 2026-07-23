from core.gridpath import Agent, Grid
import inspect
import pytest

def test_grid_creazione():
    g = Grid(7)
    h = Grid(-2)
    i = Grid('ciao')
    assert len(g) == 49 and isinstance(g._agenti,list)
    assert len(h) == 81 and isinstance(h._agenti,list)
    assert  len(i) == 25 and isinstance(i._agenti,list)

def test_grid_repr():
    g = Grid(3)
    a = Agent(g, 'pippo', 1, 1)
    assert repr(g) == 'Grid(3,Agent(\'pippo\',1,1))'

def test_grid_add_iter():
    g = Grid(3)
    a = Agent(g, 'pippo', 1, 1)
    lista = list(g)
    assert g._agenti == lista
    assert inspect.isgenerator(iter(g))
    assert a in lista

def test_grid_getitem():
    g = Grid(3)
    a = Agent(g, 'pippo', 1, 1)
    b = Agent(g, 'pappo', 1, 2)
    assert a in g['pippo']
    assert b in g[(1,2)]

def test_grid_remove():
    g = Grid(3)
    a = Agent(g, 'pippo', 1, 1)
    b = Agent(g, 'pappo', 1, 2)
    g.elimina_agente(b)
    assert len(g._agenti) == 1 and b not in list(g)

# test per agente
def test_agente_eq():
    g = Grid(3)
    a = Agent(g, 'pippo', 1,1)
    b = Agent(g, 'pippo', 1,1)
    c = Agent(g, 'pippo', 1,2)
    assert a == b
    assert not a==c
    assert not a == 'ciao'

def test_agente_repr_hash():
    g = Grid(3)
    a = Agent(g, 'pippo', 1, 1)
    b = Agent(g, 'pippo', 1, 1)
    assert repr(a) == 'Agent(\'pippo\',1,1)'
    assert hash(a) == hash(b)

def test_agente_coord_move():
    g = Grid(3)
    a = Agent(g, 'pippo', 1, 1)
    b = Agent(g, 'pippo', 1, 2)
    assert a.coordinate() == (1,1)
    assert a.move((0,1)) == (1,2)

def test_move_fuori_griglia_solleva_errore():
    g = Grid(3)
    a = Agent(g, 'pippo', 2, 2)
    with pytest.raises(ValueError):
        a.move((1, 1))  # porterebbe a (3,3), fuori dai limiti

def test_add_posizione_illegale_solleva_errore():
    g = Grid(3)
    with pytest.raises(ValueError):
        Agent(g, 'pippo', 5, 5)  # posizione fuori dai limiti fin dalla creazione

def test_move_casual_esaurisce_tentativi_e_solleva(monkeypatch):
    g = Grid(2)
    a = Agent(g, 'pippo', 0, 0)
    mosse_sempre_illegali = iter([[(-1, 0)], [(0, -1)], [(-1, 0)]])
    monkeypatch.setattr(
        'core.gridpath.sample',
        lambda popolazione, k: next(mosse_sempre_illegali)
    )
    with pytest.raises(ValueError):
        a.move_casual()
