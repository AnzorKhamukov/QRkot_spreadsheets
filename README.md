# Приложение для Благотворительного фонда поддержки котиков QRKot.
## Описание 
### QRkot - это API Благотворительного фонда поддержки котиков. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
## Возможности
### В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам. Настроено автоматическое создание первого суперпользователя при запуске проекта.
# Установка
### Склонируйте репозиторий:
```https://github.com/AnzorKhamukov/cat_charity_fund```
### Активируйте venv и установите зависимости:
```python3 -m venv venv```
```source venv/bin/activate```
```pip install -r requirements.txt```
### Создайте в корневой директории файл .env:
```
APP_TITLE=Приложение QRKot.
DESCRIPTION=Спасем котиков вместе!
DATABASE_URL=sqlite+aiosqlite:///./<название базы данных>.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>
EMAIL=email # ваш личный гугл-аккаунт
TYPE=service_account
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY="..."
CLIENT_EMAIL=...
CLIENT_ID=...
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=...
```
### Примените миграции для создания базы данных SQLite:
```alembic upgrade head```
## Управление:
### Для локального запуска выполните команду:
```uvicorn app.main:app --reload```
### Сервис будет запущен и доступен по следующим адресам:
+ http://127.0.0.1:8000 - API
+ http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
+ http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc
### После запуска доступны следующие эндпоинты:
+ Регистрация и аутентификация:
+ /auth/register - регистрация пользователя
+ /auth/jwt/login - аутентификация пользователя (получение jwt-токена)
+ /auth/jwt/logout - выход (сброс jwt-токена)

>.Пользователи:
+ /users/me - получение и изменение данных аутентифицированного пользователя
+ /users/{id} - получение и изменение данных пользователя по id

>. Благотворительные проекты:
+ /charity_project/ - получение списка проектов и создание нового
+ /donation/my - получение списка всех пожертвований аутентифицированного пользователя

## Пример запроса и ответа:
>. Регистрация пользователя:
>>. POST-запрос /auth/register
>>>>. Тело запроса:
```
{  
   "email": "user@example.com",
   "password": "string",
   "is_active": true,
   "is_superuser": false,
   "is_verified": false
}
```

>>>>. Ответ:
```
{
   "id": null,
   "email": "user@example.com",
   "is_active": true,
   "is_superuser": false,
   "is_verified": false
}
```

>. Получение всех пожертвований:
>>. GET-запрос /donation/
>>>>. Ответ:
```
[    
   {
       "full_amount": 0,
       "comment": "string",
       "id": 0,
       "create_date": "2019-08-24T14:15:22Z",
       "user_id": 0,
       "invested_amount": 0,
       "fully_invested": true,
       "close_date": "2019-08-24T14:15:22Z"
   }
]
```