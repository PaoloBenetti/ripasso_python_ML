# ripasso_mese1
Ripasso privato su pyton  

Giorno 1: 09/07  

Crea una classe Vector2D immutabile (usa @dataclass(frozen=True) oppure __slots__ manuale) con __repr__ non ambiguo, __eq__ per confronto per valore, __hash__ coerente. Scrivi 3-4 test che verificano v1 == v2, {v1, v2} in un set, repr(v1)  

Scoperte: la sintassi !r dopo una variabile richiama il metodo repr()  

Giorno 2: 10/07  
Crea una classe Polyline che contiene una lista di Vector2D e supporta len(p), p[0], p[1:3] (slicing che ritorna un'altra Polyline), iterazione implicita via __getitem__ (Python la fa da solo se non c'è __iter__)  

Scoperte:  
- Le classi dove non è implementato __iter__ si appoggiano a __getitem__, partono da index = 0 e avanzano fino a trovare un IndexError
- I test non devono eseguire codice ma verificare che i risultati ritornino
- In fase di ottimizzazione gli assert vengono ignorati dall'interprete, nel codice meglio usare raise
- Esistono gli oggetti Slice, e getitem li gestisce.

Giorno 3: 11/07  
Aggiungi a Vector2D: somma tra vettori, moltiplicazione per scalare (sia v * 2 che 2 * v), negazione. Testa anche il caso di tipo incompatibile (v + "ciao" deve sollevare TypeError, non un errore criptico)  

Scoperte:  
- la funzione sum() parte sempre da 0 e serve implementare __radd__ in modo da gestire questo caso
- ogni operatore con un problema di tipo (Typeerror) va ad invocare al versione con __roperando__
