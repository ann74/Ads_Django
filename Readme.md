### 1. Создание пользователя

**Request:**  POST /user/
```
{
    "password": "zxcvb68",
    "username": "oleg68"
}
```

### 2. Авторизация по JWT

**Request:**  POST /user/token/
```
{
    "password": "rthg125",
    "username": "petr555"
}
```
**Request:**  POST /user/token/refresh/
```
{
    "refresh": "JWT_token refresh из предыдущего запроса"
}
```

