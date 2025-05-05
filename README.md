### Как запустить локальный сервер:

1. [Download Docker](https://www.docker.com/products/docker-desktop/)

2. Скопировать ***.env.example*** в ***.env***

3. Запустить контейнер:

    ```
    $ docker-compose up -d
    ```

4. Применить миграции:
    ```
    $ alembic upgrade head
    ```
5. Запустить uvicorn:
    ```
    $ uvicorn app.main:app
    ```

**Документация (Swagger UI):**
http://127.0.0.1:8000/docs