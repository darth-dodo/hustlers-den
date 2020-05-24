init:
	poetry shell

migrations:
	python manage.py makemigrations
	python manage.py migrate

copy-env-template:
	cp .env .env.template

create-env-vars:
	cp .env.template .env

shell:
	python manage.py shell_plus

server:
	python manage.py runserver

requirements:
	poetry export -f requirements.txt > requirements.txt