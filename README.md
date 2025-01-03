http://127.0.0.1:80/api/v1/user/registration - POST, регистрация. В теле username + password. Можно ещё и почту

http://127.0.0.1:80/api/v1/user/check/{username} - GET, проверка зарегистрированного пользователя.

http://127.0.0.1:80/api/v1/auth/login - POST, получение пары access и refresh JWT. В теле username + password. access действует 15 минут, refresh 30 дней. 

http://127.0.0.1:80/api/v1/auth/refresh - POST, получение новой пары access и refresh JWT. В теле вводится "token": <refresh token>. access токен не примет.

http://127.0.0.1:80/api/v1/auth/status - GET, проверка токена на валидность и время жизни. В теле вводится "token": <access OR refresh>

На следующие запросы нужен access JWT в заголовке Authorization: Bearer <access>

http://127.0.0.1:80/api/v1/record - POST, создание записи. В теле вводится title: <название>. Можно ещё и description - описание статьи. Создать можно максимум 10 записей.

http://127.0.0.1:80/api/v1/record - GET, получение всех записей (лимит 10 записей). В query string можно вести count=<число> - получение определённого количество записей (но максимум 10). Либо title=<название> - конкретную статью с определённым названием.

http://127.0.0.1:80/api/v1/my_records - GET, получение всех своих записей.

http://127.0.0.1:80/api/v1/record/<int> - DELETE, удаление записи. Удалить можно только свою запись, иначе статус 403.

http://127.0.0.1:80/api/v1/record/<int> - PATCH, частичное обновление записи. В теле вводятся те же данные, что и при создании записи. Обновить можно только свою запись, иначе статус 403. Такие поля, как id, date_created и owner обновить нельзя.
