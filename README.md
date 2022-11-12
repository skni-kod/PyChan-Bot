# PyChan

## Instalowanie wymaganych pakietów
```python -m pip install -r req.txt```

## Konfiguracja
Skopiuj plik `config.py.sample` i zmień jego nazwę na `config.py`.  
Wypełnij `config.py` odpowiednimi wartościami.

## Uruchamianie bota
Uruchom terminal w katalogu PyChan i wpisz `python main.py`

## Używanie bota
Po zaproszeniu bota na serwer można użyć komendy `help` aby wyświetlić listę wszystkich komend.

## Struktura projektu
    PyChan
    ├── main.py           # Ingresja bota, tutaj wszystko się zaczyna
    ├── config.py         # Plik konfiguracyjny, należy go ręcznie utworzyć na podstawie config.py.sample
    ├── Core              # Katalog zawierający „Rdzeń” PyChan'a, wszystko co jest związane z Discordem
    │   ├── Commands      # Katalog zawierający komendy.
    │   │   ├── Games     # Każda komenda ma przydzieloną kategorię
    │   │   ├── Images    # Struktura katalogów kategorii: 
    │   │   ├── Science   #   Kategoria
    │   │   ├── Settings  #   ├── Functions
    │   │   ├── SKNIKOD   #   │   ├── komenda1.py
    │   │   ├── Text      #   │   └── komenda2.py
    │   │   └── Utilities #   └── kategoria.py
    │   ├── Decorators    # Dekoratory. Roszerzają komendy o dodatkowe funkcjonalności
    │   ├── Errors        # Globalny error handler projektu
    │   └── Listeners     # Obsługa wydarzeń niepowiązanych z systemem komend
    └── Database          # Obsługa bazy danych
