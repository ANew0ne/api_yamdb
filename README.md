# API для проекта Yatube
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Аутентификация по JWT-токену.  

Методы применяемые в API: GET, POST, PUT, PATCH, DELETE.  

Данные передаются в формате JSON.  

# Стек технологии
- Проект написан на Python с использованием веб-фреймворка Django REST Framework.
- Библиотека Simple JWT - работа с JWT-токеном.
- База данных - SQLite.
- Система управления версиями - git.

```
Python 3.9.18
Django 3.2.16
asgiref 3.7.2
atomicwrites 1.4.1
attrs 23.1.0
certifi 2023.11.17
charset-normalizer 2.0.12
colorama 0.4.6
django-filter 23.5
djangorestframework 3.12.4
idna 3.6
iniconfig 2.0.0
packaging 23.2
pluggy 0.13.1
py 1.11.0
PyJWT 2.1.0
pytest 6.2.4
pytest-django 4.4.0
pytest-pythonpath 0.7.3
pytz 2023.3.post1
requests 2.26.0
sqlparse 0.4.4
toml 0.10.2
typing_extensions 4.8.0
urllib3 1.26.18
```

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ANew0ne/api_yamdb.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

----
### Примечание:
Обратите внимание из проекта исключён фронтенд и view-функции приложения rewiews.  
После запуска сервера в браузере на http://127.0.0.1:8000/, страница выдаст ошибку "Page not found (404)".  
Полная документация (redoc.yaml) доступна по адресу http://127.0.0.1:8000/redoc/  

# Примеры http-запроса и ответов API

## http-запрос (POST)
```
    url = http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
        {
         "text": "string",
         "score": 1
        }
```

## Варианты Ответов API

### Статус - код 201 
```
    {
     "id": 0,
     "text": "string",
     "author": "string",
     "score": 1,
     "pub_date": "2019-08-24T14:15:22Z"
    }
```

### Статус - код 400
```
   {
    "field_name": [
    "string"
   ]
   }
```

Команда разработки:
[Алексей Астапов](https://github.com/aleksei-astapoff)  
[Денис Поддубный](https://github.com/ANew0ne)  
[Шукурилло Каримов](https://github.com/gratefultolord)