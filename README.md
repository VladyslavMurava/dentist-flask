# dentist-flask

Клієнт-серверний вебзастосунок запису на прийом до стоматолога.

Flask + PostgreSQL (Neon), розгорнуто на Render.

## Запуск

```bash
pip install -r requirements.txt
set DATABASE_URL=postgresql://...
python app.py
```n
## Маршрути

- GET  /                          форма запису
- POST /book                      збереження заявки
- GET  /appointments              список записів
- POST /appointments/<id>/delete  видалення запису
- GET  /api/appointments          JSON зі списком записів
- GET  /api/services              JSON з послугами
