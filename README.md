# Hustlers Den - Knowledge Resource Aggregator for Teams

![knowledge](https://media.giphy.com/media/TI32JwHmWQEi4/giphy.gif)

## Index
- [Summary](#summary)
- [Installation](#installation)
- [Demo](#demo)
- [API Documentation](#api-documentation)
- [Educational Resources](#educational-resources)
- [ToDos](#todos)
- [Feature Roadmap](#feature-roadmap)
- [Future Scope](#future-scope)

## Summary
[Hustlers Den](https://hustlers-den.herokuapp.com/) is a knowledge resource aggregation platform. The motivation to build this project was to ease out the process of sharing educational resources amongst a team as compared to the alternative of messages getting lost in the wild while using Slack channels. The project is built using [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/). The API documentation is done using [Swagger Documentation](https://hustlers-den.herokuapp.com/swagger-docs/).

In case of any questions, queries or suggestions please reach out to [@darth-dodo](https://github.com/darth-dodo).

Cheers!

![librarian](https://media.giphy.com/media/l0HlMEi55YsfXyzMk/source.gif)
--

## Installation
### Local instructions
- Make sure you have a [Postgres](http://postgresguide.com/) version greater than 9.6
- Clone the repo
- Create your `.env` file by using `.env.example` as template and substituting values based on your environment
- Use [Pyenv](https://github.com/pyenv/pyenv) to install and set Python to version 3.7.x
- Run `pipenv install`
- Activate the virtualenv using `pipenv shell`
- Create development Postgres Database using the command `createdb den_db` as mentioned in the `den/settings/dev.py`
- Create a superuser using the command `python manage.py createsuperuser`
- Run the local server using the command `python manage.py runserver`
- Hop on to the site and go to `<your-localhost-with-port>/admin`
- Use the above credentials to log into the admin panel

## Demo
- The Backend sandbox can be accessed using Django Admin Panel and [Jet](https://github.com/geex-arts/django-jet) at [https://hustlers-den.herokuapp.com/](https://hustlers-den.herokuapp.com/) with the following credentials:
  - Username: admin@hden.com
  - password: `sharing-is-caring`

## API Documentation
- [Static API Documentation using the OpenAPI spec can be found over here](https://hustlers-den.herokuapp.com/docs)
- [Interactive API Documentation generated using Swagger can be found here](https://hustlers-den.herokuapp.com/swagger-docs)

## Educational Resources
- TBD


## ToDos
- [ ] Add more docstrings application wide
- [ ] Create a list of Educational Resources
- [ ] Seed data script
- [ ] Using custom querysets
- [ ] Custom Middleware for Error Handler
- [ ] Base Service Class for MVSC approach
- [ ] Auto assign user permissions

## Feature Roadmap

- [x] Setting up django project
- [x] [Adding knowledge store](https://github.com/darth-dodo/hustlers-den/pull/2)
- [x] [Adding users](https://github.com/darth-dodo/hustlers-den/pull/5)
- [x] [Adding users to knowledge store](https://github.com/darth-dodo/hustlers-den/pull/6)
- [x] Setup [Django REST Framework](http://www.django-rest-framework.org/)
- [x] Setup Hustler serializer
- [x] Setup [JWT](https://github.com/GetBlimp/django-rest-framework-jwt), Session and Basic auth using DRF
- [x] Custom JWT payload generator
- [x] Read only viewsets based on auth token for knowledge base
- [x] Appropriate [filters and searches](https://github.com/carltongibson/django-filter)
- [x] [Swagger + Coreapi for better REST API interface](https://github.com/darth-dodo/hustlers-den/pull/10)
- [x] [Django Debug Toolbar, Query Count Middlewares and Django Power Shell for efficient debugging](https://github.com/darth-dodo/hustlers-den/pull/11)
- [x] Eager Loading for Serializers to prevent N+1 queries
- [x] Deploy on Heroku/PA
- [ ] Implement Django Management Commands for generation seed database
- [ ] Implement Celery Integration for resetting the Sandbox Database every 24 hours
- [ ] Hustler Sign up via REST api
- [ ] Hustler Activation flow via Admin Panel and REST API
- [ ] Discussion module
- [ ] Knowledge Packets module
- [ ] [Try out Django Watchman (for checking out services)](https://github.com/mwarkentin/django-watchman)


## Future Scope
- [ ] Weekly Newsletter implementation
- [ ] Slack Bot
- [ ] Browser extension to add resources
- [ ] Custom roles and permissions
- [ ] Light Weight Dashboard
- [ ] Export data in CSV using custom Admin actions
