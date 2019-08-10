# Celery
- Run Celery Worker with Redis server as the broker
```
celery -A den worker -l info
```
- Run Celery Beat
```
celery -A den beat -l info
```
