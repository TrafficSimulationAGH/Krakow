# Obwodnica IV
Symulacja dyskretna ruchu drogowego na obwodnicy IV Krakowa.

## Struktura
Foldery:
- *doc*: zawiera polską dokumentację LaTeX projektu oraz propozycję rozwiązania (*proposal*)
- *automata*: zawiera implementację rozwiązania w formie paczki Python 3
- *automata/tests*: zawiera podstawowe testy jednostkowe

## Uruchomienie
Program główny: `python automata/__init__.py`

Testy: `python automata/tests/__init__.py`

Importowanie:

```
$ python
>>> import automata
>>> automata.main()

>>> import automata.tests
>>> automata.tests.main()
```

## Tutorial Git
Przeniesiony do wiki.
