
# YLab_University_DZ_1



## Развёртка

Клонируем репозиторий заходим в директорию

```bash
  git clone https://github.com/Pelmexaxa/YLab_University_DZ_1.git
  cd .\YLab_University_DZ_1\
```

Сборка и запуск
```bash
  docker-compose build
  docker-compose up
```

### Для проверки
Запросы на сервер идут по адресу:
`localhost:8000`

Переменную LOCAL_URL (в postman) нужно указать:
`localhost:8000`

Доступ на документацию:
`http://localhost:8000/docs`


### PgAdmin (не обязательно)
В репозитории присутствует PgAdmin:

`http://localhost:5050/browser/`

Данные PostgreSQL:
- Пароль - pgdz1pswrd
- Название базы - dz1
- Пользователь - dz1user

![PG1](https://i.imgur.com/aMozWDM.png)

В имя хоста нужно указать название контейнера в PostgreSQL:
`postgres_container`

![PG2](https://i.imgur.com/EYlAnlX.png)
## Стек

Фреймворк: [FastAPI](https://fastapi.tiangolo.com)

ОRM для работы с PostgreSQL : [Tortoise ORM](https://tortoise.github.io)

Инструмент для сборки проекта: [Docker](https://www.docker.com)



## Authors

- [@pelmexaxa](https://www.github.com/pelmexaxa)

