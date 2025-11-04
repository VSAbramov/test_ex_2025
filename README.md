# Миграции
Используется alembic

Инициализировать alembic:
```bash
alembic init alembic
```
поправить путь к файлу в `alembic.ini`

Сгенерировать миграцию для создания бд:
```bash
alembic revision -m "init db"
```

Сгенерировать миграцию (после изменения моделей SQLAlchemy):
```bash
alembic revision --autogenerate -m "migration description"
```

Применить миграцию (сначало проверить сгенерированный код в папке `versions`):
```bash
alembic upgrade head
```