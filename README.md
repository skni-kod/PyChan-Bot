# PyChan

## Instalowanie wymaganych pakietów  
```python -m pip install -r req.txt```

Aby w pełni korzystać z muzycznych funkcji bota, należy oddzielnie pobrać [FFmpeg](https://ffmpeg.org/).

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
```text
├── main.py              # Punkt wejścia
├── config.py            # Plik konfiguracyjny, należy go ręcznie utworzyć na podstawie config.py.sample
└── pychan               # Moduł zawierający całą funkcjonalność bota
    ├── core.py          # Sedno sprawy
    ├── help.py          # Generator pomocy
    ├── checks.py        # Niestandardowe filtry dla komend
    ├── errors.py        # Obsługa wszelkich błędów
    ├── status.py        # W co PyChan teraz gra?
    ├── database.py      # Obsługa bazy danych
    ├── listeners.py     # Obsługa wydarzeń niepowiązanych z systemem komend
    ├── decorators.py    # Dekoratory. Rozszerzają komendy o dodatkowe funkcjonalności
    └── commands         # Katalog zawiera komendy pogrupowane kategoriami
        ├── games        
        │   ├── lol.py
        │   ├── osrs.py
        │   ├── osu.py
        │   └── tft.py
        ├── media
        ├── science
        ├── sknikod
        ├── text
        └── utilities
```
