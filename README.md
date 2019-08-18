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
- Create development Postgres Database using the command `createdb den_db` and permissions for user as mentioned in the `den/settings/dev.py` eg.
    - `$ createdb den_db`
    - `$ psql -U <user> or $ psql postgres`
    - `# CREATE ROLE den_app WITH LOGIN PASSWORD 'your-awesome-password';`
    - `# GRANT ALL PRIVILEGES ON DATABASE den_db TO den_app;`
    - `# \q`


- Create a superuser using the command `python manage.py createsuperuser`
- Run the local server using the command `python manage.py runserver`
- Hop on to the site and go to `<your-localhost-with-port>/admin`
- Use the above credentials to log into the admin panel

## Demo
- The Backend sandbox can be accessed using Django Admin Panel and [Jet](https://github.com/geex-arts/django-jet) at [https://hustlers-den.herokuapp.com/](https://hustlers-den.herokuapp.com/) with the following credentials:
  - Username: admin@hden.com
  - password: `sharing-is-caring`
 - The Database Schema diagram can be found over [here](https://github.com/darth-dodo/hustlers-den/blob/master/hustlers-den-schema.png) 

## API Documentation
- [Static API Documentation using the OpenAPI spec can be found over here](https://hustlers-den.herokuapp.com/docs)
- [Interactive API Documentation generated using Swagger can be found here](https://hustlers-den.herokuapp.com/swagger-docs)

## Educational Resources
- While working on anything, we tend to come across educational resources which help us in getting better and understanding a problem as well as it's solution on a deeper level
- The [Educational Resources](https://github.com/darth-dodo/hustlers-den/blob/master/EducationalResources.md) file is a place we have listed down the resources we referred to while working on this project for giving a deeper context and through learning to the reader if required.


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
- [x] Add more docstrings application wide
- [x] Create a list of Educational Resources
- [x] [Custom Middleware for Error Handler](https://github.com/darth-dodo/hustlers-den/pull/23)
- [x] Auto assign user permissions
- [x] [Implement Django Management Commands for generation seed database](https://github.com/darth-dodo/hustlers-den/pull/24)
- [x] [Knowledge Packets module]((https://github.com/darth-dodo/hustlers-den/pull/25))
- [x] [Implement Celery Integration](https://github.com/darth-dodo/hustlers-den/pull/26) for resetting the Sandbox Database every 24 hours
- [x] [Base Service Class for MVCS approach](https://github.com/darth-dodo/hustlers-den/pull/29)
- [x] [Knowledge Resource creation and update using Model ViewSets and custom Permission Classes](https://github.com/darth-dodo/hustlers-den/pull/32) 
    - [x] Only the creator can modify the his/her contributions
    - [x] SuperUsers can update anything
    - [x] Custom Permission Class 
    - [x] Error Handling for custom Permission denied error exception
- [ ] [Hustler Sign up via REST api](https://github.com/darth-dodo/hustlers-den/tree/epic/user-management)
    - [x] [Make an Abstract ViewSet for Hustler](https://github.com/darth-dodo/hustlers-den/pull/31)
    - [x] [ViewSet for Hustler with Access Control](https://github.com/darth-dodo/hustlers-den/pull/33)
    - [ ] Service to create django user, hustler and assign permissions group
    - [ ] Integrate the service in endpoint
    - [ ] Endpoint can be anonymous and require user verification from super user
    - [ ] Endpoint can be consumed by super users for autoverified new user
    - [ ] Adding `IsVerified` Permission to the viewsets
- [ ] Audit trail or Django Simple History integration
- [ ] Documentation about Base Service with usage example for Wiki
- [ ] Documentation about Custom Middleware with usage example for Wiki
- [ ] Weekly Newsletter implementation
    - [ ] Integrate Sendgrid
    - [ ] Weekly emails based on User interests
    - [ ] User preferences/settings
    - [ ] Create newsletter template
- [ ] Slack Bot
    - [ ] Custom Slack App
    - [ ] Explore Dialogs for adding resources
    - [ ] Publish Slack bot
- [ ] Discussion module
- [ ] Test Cases
  - [ ] Unit Tests
  - [ ] Integration Tests
- [ ] [Try out Django Watchman (for checking out system monitoring)](https://github.com/mwarkentin/django-watchman)
- [ ] Add ElasticSearch and relevant search indexes to be consumed by the ViewSets


## Future Scope
- [ ] Move the App to a Demo environment in a separate Heroku App using "Heroku Deploy" Button
- [ ] Browser extension to add resources
- [ ] Custom roles and permissions
- [ ] Light Weight Dashboard
- [ ] Export data in CSV using custom Admin actions
