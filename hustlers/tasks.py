from celery import shared_task


@shared_task(name="sum_two_numbers")
def add(x, y):
    print(x + y)