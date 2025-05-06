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
