# DjaIF

DjaIF, simple **Dja**ngo-powered **I**nteractive **F**iction engine.

This project is a software that I'am developing during [this series of YouTube streams (in Russian)](https://www.youtube.com/playlist?list=PLUFoWyWge7mrNDtYx-1pzpUWDWg7kcXQq).

### How to

1. Get [poetry](https://python-poetry.org/).
1. Clone.
1. `poetry install`.
1. `poetry run python manage.py migrate`.
1. `poetry run python manage.py createsuperuser --name=admin` and set password to `admin` (TODO: make the password optional).
1. `poetry run python manage.py runserver`.
