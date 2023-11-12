# Проект Foodgram

**Foodgram** - продуктовый помощник.

[![Django-app workflow](https://github.com/Garryy1337/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Garryy1337/foodgram-project-react/actions/workflows/main.yml)

### Описание проекта
Пользователи **Foodgram** могут публиковать рецепты (**Recipes**), подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать в формате .txt сводный список продуктов (**Ingredients**), необходимых для приготовления одного или нескольких выбранных блюд.

Для удобства навигации по сайту рецепты размечены тэгами (**Tags**)

### Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Инструкция для разворачивания проекта на удаленном сервере:

- Склонируйте проект из репозитория:

```
$ git clone https://github.com/Garryy1337/foodgram-project-react.git
```

- Выполните вход на удаленный сервер

- Установите DOCKER на сервер:
```
apt install docker.io 
```

- Установитe docker-compose на сервер:
```
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

- Отредактируйте конфигурацию сервера NGNIX:
```
Локально измените файл ..infra/nginx.conf - замените данные в строке server_name на IP-адрес удаленного сервера
```

- Скопируйте файлы docker-compose.yml и nginx.conf из директории ../infra/ на удаленный сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yaml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
- Запустите приложение в контейнерах:

```
docker-compose up -d --build
```

- Выполните миграции:

```
docker-compose exec backend python manage.py migrate
```

- Создайте суперпользователя:

```
docker-compose exec backend python manage.py createsuperuser
```

- Выполните команду для сбора статики:

```
docker-compose exec backend python manage.py collectstatic --no-input
```

- Команда для заполнения тестовыми данными:
```
docker-compose exec backend python manage.py get_of_ingredients --path data/
```

- Команда для остановки приложения в контейнерах:

```
docker-compose down -v
```

### Для запуска на локальной машине:

- Склонируйте проект из репозитория:

```
$ git clone https://github.com/Garryy1337/foodgram-project-react.git
```

- В папке ../infra/ переименуйте файл example.env в .env и заполните своими данными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<...> # секретный ключ django-проекта из settings.py
DEBUG=False
ALLOWED_HOSTS=<server_name>, <server_ip>, localhost, backend, 127.0.0.1

```

- Создайте и запустите контейнеры Docker (по инструкции выше).

После запуска проект будут доступен по адресу: [http://localhost/](http://localhost/)

Документация будет доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)

### Особенности заполнения данными:

- Добавьте теги для для рецептов через админ-панель проекта [http://localhost/admin/](http://localhost/admin/), т.к. это поле является обязательным для сохранения рецепта и добавляется только админом.

***

## Ресурсы API Foodgram

**AUTH**: получение/удаление токена авторизации.

**USERS**: пользователи: регистрация, просмотр/изменение личного профиля, просмотр пользовательских профилей, подписка/отписка на пользователей.

**TAGS**: теги категории рецептов (создаются и редактируюся пользователями с правами администратора).

**RECIPES**: рецепты. У каждого авторизованного пользователя есть возможность добавлять рецепт в "Избранное" и в "Список покупок".
Каждый рецепт содержит следующие поля:
```
- Автор публикации (пользователь).
- Название.
- Картинка.
- Текстовое описание.
- Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
- Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
- Время приготовления в минутах.
```

**INGREDIENTS**: ингредиенты.
Поля:
```
- Название.
- Количество.
- Единицы измерения.
```

### Пользовательские роли

**Права анонимного пользователя:**
- Создание аккаунта.
- Просмотр: рецепты на главной, отдельные страницы рецептов, страницы пользователей.
- Фильтрация рецептов по тегам.

**Права авторизованного пользователя (USER):**
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

**Права администратора (ADMIN):**
Все права авторизованного пользователя +
- Изменение пароля любого пользователя,
- Создание/блокирование/удаление аккаунтов пользователей,
- Редактирование/удаление любых рецептов,
- Добавление/удаление/редактирование ингредиентов.
- Добавление/удаление/редактирование тегов.

**Администратор Django** — те же права, что и у роли Администратор.

### Алгоритм регистрации пользователей

Для добавления нового пользователя нужно отправить POST-запрос на эндпоинт:

```
POST /api/users/
```

- В запросе необходимо передать поля:

1. ```email``` - (string) почта пользователя;
2. ```username``` - (string) уникальный юзернейм пользователя;
3. ```first_name``` - (string) имя пользователя;
4. ```last_name``` - (string) фамилия пользователя;
5. ```password``` - (string) пароль пользователя.

Пример запроса:

```
{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```

Далее необходимо получить авторизационный токен, отправив POST-запрос на эндпоинт:

```
POST /api/auth/token/login/
```

- В запросе необходимо передать поля:

1. ```password``` - (string) пароль пользователя;
2. ```email``` - (string) почта пользователя.

Пример запроса:

```
{
"password": "Qwerty123",
"email": "vpupkin@yandex.ru"
}
```

Пример ответа:

```
{
  "auth_token": "string"
}
```

Поученный токен всегда необходимо передавать в заголовке (```Authorization: Token TOKENVALUE```) для всех запросов, которые требуют авторизации.

### Изменение пароля текущего пользователя:

```
POST /api/users/set_password/
```

Пример запроса:

```
{
  "new_password": "string",
  "current_password": "string"
}
```

### Удаление токена пользователя:

```
POST /api/auth/token/logout/
```

### Регистрация пользователей админом

Пользователя может создать администратор через админ-зону сайта. Получение токена осуществляется способом, описанным выше.

#### Примеры использования API для неавторизованных пользователей:

Для неавторизованных пользователей работа с API доступна в режиме чтения.

```
GET /api/users/- получить список всех пользователей.
GET /api/tags/- получить список всех тегов.
GET /api/tags/{id}/ - получить тег по ID.
GET /api/recipes/- получить список всех рецептов.
GET /api/recipes/{id}/ - получить рецепт по ID.
GET /api/users/subscriptions/ - получить список всех пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
GET /api/ingredients/ - получить список ингредиентов с возможностью поиска по имени.
GET /api/ingredients/{id}/ - получить ингредиент по ID.
```

#### Пример GET-запроса:
```
GET /api/recipes/
```

#### Пример ответа:
- код ответа сервера: 200 OK
- тело ответа:

```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

#### Пример GET-запроса с фильтрацией по наименованию:
```
GET /api/ingredients/?name=абри
```

#### Пример ответа:
- код ответа сервера: 200 OK
- тело ответа:

```
[
    {
        "id": 1,
        "name": "абрикосовое варенье",
        "measurement_unit": "г"
    },
    ...
        {
        "id": 6,
        "name": "абрикосы консервированные",
        "measurement_unit": "г"
    }
]
```

#### Пример POST-запроса:
```
POST /api/recipes/
```
Авторизация по токену.
Запрос от имени пользователя должен выполняться с заголовком "Authorization: Token TOKENVALUE"

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

#### Пример ответа:
- код ответа сервера: 201
- тело ответа:

```
{
"id": 0,
"tags": [
{}
],
"author": {
"email": "user@example.com",
"id": 0,
"username": "string",
"first_name": "Вася",
"last_name": "Пупкин",
"is_subscribed": false
},
"ingredients": [
{
"id": 0,
"name": "Картофель отварной",
"measurement_unit": "г",
"amount": 1
}
],
"is_favorited": true,
"is_in_shopping_cart": true,
"name": "string",
"image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
"text": "string",
"cooking_time": 1
}
```

После запуска проект будут доступен по адресу: [http://localhost/](http://localhost/)

Документация будет доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)

***

Проект развернут на [http://crycat.ddns.net](http://crycat.ddns.net)

Доступ в админ-панель:

```
http://crycat.ddns.net/admin
login: admin (admin@admin.com)
pass: admin
```

### Автор

Григорий Рогов
