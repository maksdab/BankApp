# Django AI  
Wymagania:
- python 3.10 (python --version)
- Django==4.0
- Pillow
- numpy
- pandas
- tensorflow==2.8.0
- tensorflow-hub
- protobuf==3.20

## Ustawienie środowiska
```sh
python -m venv .venv
```

## Aktywacja zmiennej środowiskowej (Windows) 
### Założenie - pracuje na CMDER
```sh
.venv/Scripts/activate
```
### Założenie - pracuje na gitbash
```sh
source .venv\Scripts\activate
lub
source .venv/Scripts/activate
```
## Aktywacja zmiennej środowiskowej (Mac/Unix) 
### Założenie - pracuje na gitbash
```sh
source .venv/bin/activate
```

Jak jest aktywna wirtualna zmienna środowiskowa to przechodzimy do instalacji
(czyli w terminalu koło kursora jest w nawiasie .venv)

## Instalacja
```sh
pip install -r requirements.txt
```

## Uruchomienie
```sh
python manage.py runserver
```