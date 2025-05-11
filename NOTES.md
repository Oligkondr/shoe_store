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

## Снять dump

```
docker exec -i shoe_store_db pg_dump -U user -d shoe_store_db -F c -f /var/lib/postgresql/db.dump
```

## Восстановить dump

```
docker exec -i shoe_store_db pg_restore -U user -d shoe_store_db -F c /var/lib/postgresql/db.dump
```

___

## Сгенерировать новую миграцию

```
alembic revision --autogenerate -m "Initial revision"
```

## Применить миграции

```
alembic upgrade head
```

___

## Скопировать файл из Docker

```
docker cp shoe_store_db:/var/lib/postgresql/dbp.dump .docker/dbp.dump
```
