# GRIDPATH  
Piccola libreria di allenamento che gestisce una piccola griglia quadrata e degli agenti che si muovono in essa.

## Esempio d'uso

​```python
from core.gridpath import Grid, Agent

g = Grid(5)
a = Agent(g, "pippo", 2, 2)
b = Agent(g, "pluto", 0, 0)

a.move((0, 1))       # sposta pippo, solleva ValueError se esce dai limiti
a.move_casual()       # mossa casuale con retry automatico su mosse illegali

print(g[(2, 3)])       # trova agenti per coordinate
print(g["pippo"])      # trova agenti per nome

g.recap_agenti()       # stampa raggruppamento agenti per posizione, con timing
g.is_leagl(6,7)        # verifica se una mossa rientra tra quelle permesse

g.elimina_agente(b)  # meccanismo per eliminare un agente
g.reset()            # elimina tutti gli agenti presenti all'interno della griglia
​```

## Note di design
- `Grid.__add__` crea una nuova griglia (non muta l'originale); `Grid.__iadd__` muta in place — 
  usato internamente da `Agent` quando si registra su una griglia
- Le mosse fuori dai limiti sollevano `ValueError` invece di fallire silenziosamente
