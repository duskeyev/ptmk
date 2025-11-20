## PTMK CLI

### Требования
- Python 3.12+
- Poetry 1.8+
- PostgreSQL 15+ (локально или в контейнере)

### Установка зависимостей
```bash
poetry install
```

### Настройка окружения
Создайте `.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pg
DB_USER=postgres
DB_PASSWORD=pass
```

### Тестовый Postgres
Devcontainer/Codespaces запускает контейнер `postgres:16` автоматически. Локально можно поднять через docker-compose:
```bash
docker compose -f docker-compose.devcontainer.yml up -d
```

### Запуск CLI
```bash
poetry run python src/ptmk/main.py <mode>
```

Режимы:
1. создать таблицу
2. добавить сотрудника вручную
3. вывести уникальных сотрудников
4. заполнить базу тестовыми данными
5. выборка по критерию + время
6. сравнение до/после индекса (10 прогонов)
7. удалить индекс

### Пример
```bash
poetry run python src/ptmk/main.py 2 "Ivanov Petr Sergeevich" "2009-07-12" "Male"
poetry run python src/ptmk/main.py 4
poetry run python src/ptmk/main.py 6
```

