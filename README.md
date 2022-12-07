# PyChan

## Instalowanie wymaganych pakietów
```python -m pip install -r req.txt```

Aby w pełni korzystać z muzycznych funkcji bota, należy oddzielnie pobrać [FFmpeg](https://ffmpeg.org/) i folder `ffmpeg` umieścić w folderze z projektem.

[Instalacja FFmpeg - system Windows](https://phoenixnap.com/kb/ffmpeg-windows)

[Instalacja FFmpeg - system Linux](https://phoenixnap.com/kb/install-ffmpeg-ubuntu)

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
    |   |   ├── Music     #   Kategoria
    │   │   ├── Science   #   ├── Functions
    │   │   ├── Settings  #   │   ├── komenda1.py
    │   │   ├── SKNIKOD   #   │   └── komenda2.py
    │   │   ├── Text      #   └── kategoria.py
    │   │   └── Utilities #
    │   ├── Decorators    # Dekoratory. Roszerzają komendy o dodatkowe funkcjonalności
    │   ├── Errors        # Globalny error handler projektu
    │   └── Listeners     # Obsługa wydarzeń niepowiązanych z systemem komend
    └── Database          # Obsługa bazy danych
