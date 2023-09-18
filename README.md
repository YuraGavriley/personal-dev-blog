## Personal Development Blog

A personal website-resume with blog features.

#### About the Project

#### Functionality of the Project:

  - Managing Posts by CRUD operations;
  - Registration via Google;
  - Writing comments by registered users;
  - Saving Posts for read-later section via sessions;
  - Viewing up-to-date information about the Developer.

#### Languages and Technologies
Built with Django, Python, CSS, HTML.

## Project Status

#### In Development

This project is currently in development. The main functionality is working properly. Some minor changes are in progress.

## Installation and Setup Instructions

Clone down this repository. You will need Python, pip, poetry, git installed on your machine.

###### 1. Clone this repo

```git clone https://github.com/YuraGavriley/personal-dev-blog```

###### 3. Set up a virtual environment

```python -m venv <name_of_environment>```

###### 4. Activate virtual environment in project folder

```<name_of_environment>\Scripts\activate```

###### 5. Install poetry (if you haven't done it yet)

```pip install poetry```

###### 6. Install all dependencies with poetry

```poetry install```

###### 7. Go to 'main_app' folder and execute all migrations

```python manage.py makemigrations```

```python manage.py migrate```

###### 8. Create superuser for admin dashboard and follow tips in console

```python manage.py createsuperuser```

###### 10. Run the server

```python manage.py runserver```
