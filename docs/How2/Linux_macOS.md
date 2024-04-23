_Cписок команд для Linux/macOS:_

1) клонирование репозитория
```commandline
git init
git clone https://gitlab.akhcheck.ru/denis.barilov/miptpay.git
```
2) создание виртуальной среды

```commandline
sudo apt-get install python3.10-venv
python3 -m venv .venv
source .venv/bin/activate
```
3) установка зависимостей
```commandline
pip install poetry
poetry lock
poetry install
```
     Все необходимые модули подгрузятся в вашу среду.
4) запуск сервера Django
```commandline
python3 src/miptpaydj/manage.py makemigrations
python3 src/miptpaydj/manage.py migrate
poetry run setup
python3 src/miptpaydj/manage.py runserver
```
