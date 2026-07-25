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

Giorno 4: 15/07
Scrivi un generatore che combina più sorgenti dati (es. più liste/file) con yield from, e un generatore infinito di batch casuali che usi solo con islice per limitarlo  

Scoperte:
- Spesso non serve anticipare l'errore ma catturarlo nel momento in cui avviene (try except)
- Utilizza TypeError come eccezione da elevare

Giorno 5: 15/07  
Prendi la Polyline della settimana 1 e aggiungi un metodo che genera lazy tutte le distanze tra punti consecutivi (generator, non lista). Scrivi un test che verifica che l'oggetto ritornato sia effettivamente un generatore (non una lista)  

Scoperte:
- Il test può verificare il tipo ma deve anche verificare che il funzionamento sia corretto

__Settimana 3__  
Giorno 1: 16/07  
Scrivi @timer (misura tempo di esecuzione) e @log_calls (logga argomenti e risultato) senza functools.wraps, poi rifallo con — confronta help(funzione_decorata) prima e dopo  

Scoperte:
- l'operatore * va prima ogni volta che devi inserire argomenti da una lista e doppio se da dizionario
- __ doc __ registra la stringa inserita come commento all'inizio del corpo di una funzione """ pippo """
- filter, se lasci None la funzione di confronto, ritorna solo i valori non falsi

Giorno 2: 16/07  
Scrivi @retry(times=3, exceptions=(ValueError,)) che ritenta l'esecuzione di una funzione. Poi scrivi un decoratore di classe @auto_repr che aggiunge un __repr__ automatico basato sugli attributi dell'istanza  

Scoperte:
- Il test andrebbe scritto durante la scrittura del codice, non dopo. Comunque per verificare
- di solito hai a che fare con istanze, che non hanno attributo __ name __ . utilizza type(a) per ricavare la classe e poi richiamare il nome
- try except accetta una tupla di eccezioni
- ritorna sempre nei decoratori
- Fallire silenziosamente (return none) è un disastro

Giorno 3: 17/07  
Implementa memoize da zero con una closure e un dizionario cache, poi confrontalo con functools.lru_cache — stesso comportamento? Cosa manca alla tua versione (es. gestione argomenti unhashable)?  

Scoperte:  
- Le chiavi dei dizionari devo essere hashabili, quindi le tuple vanno ordinate. Trucco, rendi tutto una tupla (lista, tupla(dizionario))
- Inspect.getclosure serve a controllolare le variabili libere, basta lasciare il nome della funzione a cui è stato applicato il decoratore
- @cache sfrutta risultati già ottenuti per ottimizzare (anche @lru_cache)


Giorno 4: 17/07  
Scrivi un context manager Timer (a classe) che stampa il tempo trascorso all'uscita del blocco with, anche in caso di eccezione. Riscrivilo con @contextmanager e confronta  

Scoperte:
- il blocco try except finally può escludere except;
- La gestione del contesto con with prevede __ enter __ da eseguire all'inizio e __ end __ da eseguire alla fine;
- gestione controllo può essere gestita tramite classe o funzione con @ contextmanager

Giorno 5: 19/07  
Metti insieme in un modulo toolkit.py: @timer, @retry, @log_calls, memoize/lru_cache, context manager Timer e uno per gestione risorse (es. apertura/chiusura "finta" di una connessione). Questo modulo lo riuserai nei prossimi mesi  

Scoperte:  
- Ricorda che per un context manager funzione serve il @ contextmanager e il piano try .. finally con yield;
- Una variabile closure viene mantenuta finchè il suo reference counter non scende a zero,
- ritorna un valore falso permette all'eccezione di propagarsi nel context manager


__Settimana 4__  
costruire una piccola libreria che sfrutti tutto ciò che hai fatto nelle settimane 1-3, non solo giustapposto ma integrato  

Giorni 20/07 -> 23/07  

Scoperte:  
- __ iadd __ è il metodo che si occupa dell'implace +=
- deepcopy va usato con attenzione: se un oggetto contiene altri oggetti, anche questi vengono duplicati, meglio shallow copy e poi copia riferimenti
- NotImplemented serve dentro alcuni metodi per segnalare il non saper fare qualcosa e passare a quello dell'altro, normalmente serve usare Raise
- Ricorda che se un test fa uso di meccaniche random, dei fissare il seed o forzare tramite monkeypatch un certo tipo di azione

__Mese 2__

__settimana 1__  
Giorno 1: 24/07  
Installa mypy, crea un mypy.ini (o sezione in pyproject.toml) con strict = true, lancialo su vector.py/gridpath.py/toolkit.py del Mese 1. Non correggere ancora nulla: fai solo l'inventario di cosa segnala  

  
Giorno 2: 24/07  
Scrivi un Protocol per "qualcosa che ha coordinate" (es. HasCoordinates con un metodo coordinate() -> tuple[int,int]) e usalo come type hint in una funzione che accetta sia Agent sia altri oggetti "simili" senza richiedere eredità esplicita  

Scoperte  
- Protocoll verifica se quelle classi implementano i metodi corretti
- duck typing statico sarà una cosa sempre opzionale in python

Giorno 3: 25/07  
Scrivi una funzione generica primo_o_default[T](lista: list[T], default: T) -> T, e/o rendi Polyline-style container generico rispetto al tipo contenuto (se ti va di generalizzare oltre Vector2D)  

Scoperte:  
- La verifica del tipo non avviene se non in modo statico
- O cotrolli tutti i tipi durante il programma, o lasci il type hint e poi elimini i controlli dove hai variabili e cose generiche
- Typevar ora ha la sintassi [T]
