# Kittygram

Сервис для публикации карточек котов с поддержкой лайков и избранного.

## Состав проекта

- `kittygram_favorite/` — бэкенд на Django + DRF
- `kittygram_frontend/` — фронтенд на React
- `docker-compose.yml` — конфигурация Docker Compose
- `nginx.conf` — конфигурация nginx

## Запуск через Docker

### 1. Клонируй репозиторий
```bash
git clone https://github.com/pademirov/kittygram_kurs.git
cd kittygram_kurs
```

### 2. Настрой переменные окружения
```bash
cp kittygram_favorite/.env.example kittygram_favorite/.env
```

Открой `kittygram_favorite/.env` и заполни переменные. `SECRET_KEY` можно сгенерировать командой:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Запусти проект
```bash
docker compose up --build
```

### 4. Примени миграции
```bash
docker compose exec backend python manage.py migrate
```

После этого проект будет доступен по адресам:
- Фронтенд: http://localhost/
- API: http://localhost/api/
- Swagger: http://localhost/api/docs/