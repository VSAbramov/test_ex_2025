# Миграции
Используется alembic

Нужно перейти в папку `migrations`:
```bash
cd migrations
```

и из неё вызывать следующие комманды для миграции

Инициализировать alembic:
```bash
alembic init alembic
```
поправить путь к бд в `alembic.ini` (ключ `sqlalchemy.url`), в сгенерированном файле `env.py` поправить значение переменной `target_metadata`

Сгенерировать миграцию для создания и изменения бд:
```bash
alembic revision --autogenerate -m "init db"
```

Применить миграцию (сначало проверить сгенерированный код в папке `versions`):
```bash
alembic upgrade head
```