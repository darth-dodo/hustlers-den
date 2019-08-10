# Celery
- Run Celery Worker with Redis server as the broker
```
celery -A den worker -l info
```
- Run Celery Beat
```
celery -A den beat -l info
```
- Run Celery Beat with Database Scheduler
```
celery -A den beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```