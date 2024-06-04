# API for PyMDB app

## О проекте:

Проект PyMDB собирает отзывы пользователей на произведения. Произведения делятся на категории, жанры и т.д.  Пользователи могут оставлять комментарии к отзывам.


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:greg2707/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:


* Если у вас Linux/macOS

    ```
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    ```

* Если у вас windows

    ```
    python -m venv venv
    source venv/scripts/activate
    python -m pip install --upgrade pip
    ```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции и запустить проект:

  * Если у вас Linux/macOS

    ```
    python3 manage.py migrate
    python3 manage.py runserver
    ```

  * Если у вас windows
  
    ```
    python manage.py migrate
    python manage.py runserver
    ```


### Документация к API по адресу `http://localhost:8000/redoc/`


## Примеры запросов к API:

- Просмотр списка произведений:
``` GET /api/v1/titles/ ```

- Добавление новой категории:  
``` POST /api/v1/categories/ ```  

- Просмотр списка жанров:  
``` GET /api/v1/genres/{slug} ```

- Просмотр данных о конкретном произведении:
``` GET /api/v1/titles/{titles_id}/ ```
  
- Просмотр списка отзывов:  
``` GET /api/v1/titles/{title_id}/reviews/ ``` 

- Просмотр данных юзера:  
``` GET /api/v1/users/{username}/ ``` 


## Использованные технологии:
- Python
- Django
- Django REST framework


## Информация об авторах:
- Кирилл Воробьев
- Виталий Дроздов [VitaliyDrozdov](https://github.com/VitaliyDrozdov)
- Григорий Грачев

