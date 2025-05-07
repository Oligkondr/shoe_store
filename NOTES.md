## Установить все зависимости

```
pip install -r requirements.txt
```

## Сгенерировать файл со всеми зависимостями

**!!! Обязательно выполните предыдущую команду !!!**\
**Файл создается заново с библиотеками которые у вас установленны, а не дописывает их.**

```
pip freeze > requirements.txt
```

___
alembic revision --autogenerate -m "Initial revision"\
alembic upgrade head

docker exec -i shoe_store_db pg_dump -U user -d shoe_store_db -F c -f /var/lib/postgresql/data/db.dump

docker exec -i shoe_store_db pg_restore -U user -d shoe_store_db -F c /var/lib/postgresql/data/db.dump