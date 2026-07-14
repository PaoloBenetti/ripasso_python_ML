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

Giorno 4: 12/07
Fai ereditare Polyline da collections.abc.Sequence (implementando solo __getitem__ e __len__ ottieni gratis __contains__, __iter__, index, count) — capisci cosa ti dà "gratis" l'ABC    

Scoperte:
- in fa riferimento ai metodi ereditati __contains__
- Duck typing: in teoria non si fa riferimento al tipo in maniera vincolante ma si lascia che sia il programmatore o la libreria a gestirlo.

Giorno 5: 13/07
Rileggi il codice scritto nei 4 giorni, aggiungi type hints (from __future__ import annotations + annotazioni base), verifica che tutti i test passino, fai un piccolo refactor se qualcosa è ripetuto  

Scoperte:
- annotazioni in cui un metodo di una classe ritorna la stessa classe richiede che all'inizio ci sia form __ future __ import annotations
- Per contratto se due oggetti sono uguali, i loro hash devono essere uguali. Se implemento una funzione __ eq __ allora devo riallineare __ hash __ per forza, sicoome in precedenza il metodo è basato su id 

__Settimana 2__   
Giorno 1: 13/07  
Scrivi un iteratore custom FibonacciIterator (classe con __next__) che genera Fibonacci senza limite superiore, poi confrontalo con la versione "sbagliata" che rimaterializza tutto in una lista  

Scoperte:  
- Un iterabile è un oggetto che costruisce un iteratore con la chiamata __ iter __ , un iteratore è una classe che implementa next e gestisce il flusso di accesso
- StopIteration è l'eccezione da sollevare per mettere fine all'iteratore, altrimenti si avrà un accesso infinito

Giorno 2: 14/07
Riscrivi FibonacciIterator come funzione generatore (def fib(): yield ...). Confronta leggibilità e uso di memoria (sys.getsizeof) tra [x**2 for x in range(1_000_000)] e (x**2 for x in range(1_000_000))    

Scoperte:
- Python adotta la convenzione per cui tutti i nomi di funzione sono minuscoli e possono usare underscore
- lazy fa riferimento a yield, quindi generazione e consumo di un elemento alla volta

Giorno 3: 14/07
Prendi un dataset "finto" (lista di dict con campi tipo {"categoria": ..., "valore": ...}) e usa groupby (con dati pre-ordinati!) per aggregare per categoria, islice per paginare, accumulate per somme cumulative  

Scoperte:
- groupby non funziona come sql e pretende che il vettore sia già ordinato, per ottenere risultati logici
- Attenzione a ricordarsi quando sono ritornati dei generatori
- Un generatore, una volta consumato, è inutilizzabile
