# dentist-flask

Клієнт-серверний вебзастосунок стоматологічного кабінету: запис на прийом,
перегляд записів та відгуки пацієнтів з автоматичним аналізом тональності.

**Стек:** Python 3.12, Flask 3, PostgreSQL (Neon), Hugging Face Inference API,
Gunicorn, Render, GitHub Actions.

**Адреса:** https://dentist-flask.onrender.com

## Можливості

- форма запису на прийом, збереження заявок у PostgreSQL;
- список записів із можливістю видалення;
- відгуки пацієнтів: кожен відгук аналізує модель
  `cardiffnlp/twitter-xlm-roberta-base-sentiment` (Hugging Face) і визначає
  тональність — позитивна, нейтральна або негативна;
- діаграма розподілу тональності відгуків;
- JSON API для записів, послуг і відгуків.

## Маршрути

| Метод | Шлях | Призначення |
|---|---|---|
| GET | / | форма запису |
| POST | /book | збереження заявки |
| GET | /appointments | список записів |
| POST | /appointments/<id>/delete | видалення запису |
| GET | /reviews | відгуки, форма та діаграма |
| POST | /reviews | збереження відгуку з аналізом ШІ |
| GET | /api/appointments | записи у JSON |
| GET | /api/services | послуги у JSON |
| GET | /api/reviews | відгуки у JSON |
| GET | /api/reviews/stats | статистика тональності у JSON |

## Змінні оточення

| Змінна | Призначення |
|---|---|
| `DATABASE_URL` | рядок підключення до PostgreSQL |
| `HF_TOKEN` | токен Hugging Face з правом Inference |
| `SECRET_KEY` | ключ сесій Flask (необов'язково) |

## Запуск локально

```bash
pip install -r requirements.txt
set DATABASE_URL=postgresql://...
set HF_TOKEN=hf_...
python app.py
```

## Розгортання

Push у гілку `main` запускає workflow GitHub Actions: перевірка коду й тести,
після чого — виклик Deploy Hook Render. Детальніше про процес командної
роботи — у [CONTRIBUTING.md](CONTRIBUTING.md).