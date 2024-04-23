_Cписок команд для Windows:_

1) клонирование репозитория
```commandline
git init
git clone https://gitlab.akhcheck.ru/denis.barilov/miptpay.git
```
2) создание виртуальной среды

```commandline
python -m venv .venv
.venv\Scripts\activate
```
    Замечание: последняя команда может выдавать ошибку.
    Чтобы активировать виртуальную среду, нужно открыть терминал от имени администратора и выполнить команду
    
    Set-ExecutionPolicy RemoteSigned

    и повторить предыдущую команду.
3) установка зависимостей
```commandline
pip install poetry
poetry lock
poetry install
```
     Все необходимые модули подгрузятся в вашу среду.
4) запуск сервера Django
```commandline
python src\miptpaydj\manage.py makemigrations
python src\miptpaydj\manage.py migrate
poetry run setup
python src\miptpaydj\manage.py runserver
```
