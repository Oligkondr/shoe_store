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
