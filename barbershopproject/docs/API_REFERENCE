# Полное описание API

## Оглавление
- [Модели данных](#модели-данных)
  - [Hall](#hall)
  - [Service](#service)
  - [Client](#client)
  - [Employee](#employee)
  - [Visit](#visit)
- [Эндпоинты API](#эндпоинты-api)
  - [Аутентификация](#аутентификация-1)
  - [Клиенты](#клиенты)
  - [Сотрудники](#сотрудники)
  - [Залы](#залы)
  - [Услуги](#услуги)
  - [Записи](#записи)
- [Примеры запросов](#примеры-запросов)

---

## Модели данных

### Hall
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| id | Integer | Авто | Уникальный ID зала |
| name | String | Да | Название зала |
| description | Text | Да | Описание зала |
| capacity | Integer | Да | Вместимость (макс. одновременных визитов) |
| location | String | Да | Адрес/местоположение |
| start_time | Time | Да | Время начала работы (формат HH:MM:SS) |
| end_time | Time | Да | Время окончания работы (формат HH:MM:SS) |

### Service
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| id | Integer | Авто | Уникальный ID услуги |
| name | String | Да | Название услуги |
| description | Text | Да | Подробное описание |
| price | Decimal | Да | Стоимость (макс. 10 цифр, 2 знака после запятой) |
| duration | Time | Да | Продолжительность (формат HH:MM:SS) |

### Client
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| user | FK(User) | Да | Связь с пользователем |
| phone_number | String | Нет | Номер телефона (формат: +7XXXXXXXXXX) |
| date_of_birth | Date | Нет | Дата рождения |
| gender | String | Да | Пол (Мужской/Женский) |

### Employee
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| user | FK(User) | Да | Связь с пользователем |
| phone_number | String | Нет | Номер телефона (формат: +7XXXXXXXXXX) |
| position | String | Да | Должность |
| halls | M2M(Hall) | Да | Залы, в которых работает |
| services | M2M(Service) | Да | Услуги, которые оказывает |

### Visit
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| client | FK(Client) | Да | Клиент |
| employee | FK(Employee) | Да | Мастер |
| service | FK(Service) | Да | Услуга |
| hall | FK(Hall) | Авто | Зал (выбирается автоматически) |
| date | Date | Да | Дата визита |
| time | Time | Да | Время начала (формат HH:MM:SS) |
| status | String | Да | Статус (Запланирована/Выполнена) |
| created_at | DateTime | Авто | Время создания записи |

---

## Эндпоинты API

### Аутентификация

#### Получение токена
```
POST /api-token-auth/
Content-Type: application/x-www-form-urlencoded

username=user&password=pass123
```

### Клиенты

#### Регистрация клиента
```
POST /registration/client/
Content-Type: application/json

{
  "user": {
    "username": "client1",
    "password": "pass123",
    "password2": "pass123",
    "email": "client@example.com",
    "first_name": "Иван",
    "last_name": "Иванов"
  },
  "phone_number": "+79161234567",
  "date_of_birth": "1990-01-01",
  "gender": "Мужской"
}
```

#### Получение профиля
```
GET /client/profile/
Authorization: Token <ваш_токен>
```

### Сотрудники

#### Список сотрудников
```
GET /employee/list/
Authorization: Token <ваш_токен>
```

### Залы

#### Список залов
```
GET /hall/show/
Authorization: Token <ваш_токен>
```

#### Создание зала (только админ)
```
POST /hall/add/
Authorization: Token <ваш_токен>
Content-Type: application/json

{
  "name": "VIP зал",
  "description": "Комфортабельный зал с панорамным видом",
  "capacity": 3,
  "location": "2 этаж, кабинет 205",
  "start_time": "09:00:00",
  "end_time": "21:00:00"
}
```

### Услуги

#### Список услуг
```
GET /service/show/
Authorization: Token <ваш_токен>
```

### Записи

#### Получение свободных слотов
```
GET /get_available_time/?employee=1&service=2&date=2025-07-15
Authorization: Token <ваш_токен>
```

#### Бронирование визита
```
POST /book/visit/
Authorization: Token <ваш_токен>
Content-Type: application/json

{
  "employee": 1,
  "service": 2,
  "date": "2025-07-15",
  "time": "14:00:00"
}
```

#### Просмотр своих записей (клиент)
```
GET /visit/show/client/
Authorization: Token <ваш_токен>
```

#### Просмотр записей сотрудника
```
GET /visit/show/employee/
Authorization: Token <ваш_токен>
```

---

## Примеры ответов

### Успешная аутентификация
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Ошибка валидации
```json
{
  "phone_number": [
    "Введите корректный номер телефона в формате +7XXXXXXXXXX"
  ]
}
```

### Список свободных слотов
```json
{
  "available_time": [
    "10:00",
    "11:30",
    "13:00",
    "14:30",
    "16:00"
  ]
}
```

---

## Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешный запрос |
| 201 | Успешное создание |
| 400 | Ошибка валидации |
| 401 | Не авторизован |
| 403 | Доступ запрещён |
| 404 | Объект не найден |
| 500 | Ошибка сервера |

---
Документация актуальна на 01.07.2025
