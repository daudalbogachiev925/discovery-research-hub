# discovery-research-hub
Описание: платформа для customer discovery. Хранение интервью, кластеризация инсайтов, Jobs-to-be-Done анализ, генерация гипотез, связывание с фичами.  Стек: Python, FastAPI, PostgreSQL, spaCy, sentence-transformers, scikit-learn, Streamlit, Docker.

# discovery-research-hub

Платформа customer discovery.

## Возможности
- Хранение интервью и транскриптов
- Автоизвлечение инсайтов (маркеры боли)
- Кластеризация инсайтов через sentence-transformers
- Jobs-to-be-Done генерация
- Streamlit-дашборд

## Быстрый старт
cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Тесты
pytest tests/ -v

## Лицензия
MIT
