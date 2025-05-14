# Movie & series recommender service

## Описание проекта
Сервис для рекомендации фильмов и сериалов на основе взаимодействия с ними в реальном времени

Используемый стек:
- Python + FastAPI + uvicorn
- HTML + JS
- PostgresSQL + SQLAlchemy
- Redis
- RabbitMQ
- Docker + docker compose

## Как запустить

1) Склонировать проект:

```bash
git clone https://github.com/danilovsnnv/aith-ml-python
```

2) Заполнить `.env` файлы в директории `dotenv_files/`. Примеры заполнения можно посмотреть в файлах `.env.*.example`

4) Собрать и запустить контейнеры:

```bash
docker-compose run --build -d
```