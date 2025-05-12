## Участники проекта:
Кондрашин Олег — Backend

Шишов Михаил — Teamlead | Frontend

Фаткулин Александр — Frontend

[Презентация проекта](https://docs.google.com/presentation/d/e/2PACX-1vR71YDftdE4JyDjTp0RTta_bF6j2IOql9ZRqYEp-037a0occjwHvk1QAMTmEWpkkNvUaziLqgIHllzU/pub?start=false&loop=false&delayms=3000)

# Подготовка:

1. [Download Docker](https://www.docker.com/products/docker-desktop/)


2. Скопировать ***.env.example*** в ***.env***


3. Запустить контейнер:

 ```
 docker-compose up -d
 ```

4. Восстановить dump:

```
docker exec -i shoe_store_db pg_restore -U user -d shoe_store_db -F c /var/lib/postgresql/db.dump
```

5. Установить все зависимости:

```
pip install -r requirements.txt
```

# Как запустить приложение:

1. Запустить ***uvicorn*** сервер:

 ```
 uvicorn app.main:app
 ```

2. Запустить приложение:

```
cd frontend | python main.py
```
или
```
python3 ./frontend/main.py
```

___
**Документация по api(Swagger UI):**
http://127.0.0.1:8000/docs
