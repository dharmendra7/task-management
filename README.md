# task-management

## Index

- [Index](#index)
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [For client use](#for-client-use)
- [Setup using docker](#setup-using-docker)

### Introduction

- Supports latest version of Python i.e. Python 3.11.1  along with Django 4.2.5 :zap:
- Implemented custom middleware that authenticates users based on a token included in the request headers. Users should be able to obtain this token by logging in through a dedicated API endpoint.:closed_lock_with_key:
- Used Celery to create an asynchronous task that sends email notifications to
project managers when a task is marked as completed.
- Build and run the application within Docker containers
- Used FormSets to allow users to add multiple tasks to a project through a web
form.
- Implemented API endpoints using Django Rest Framework for CRUD operations on
projects and tasks.

### Prerequisites

| Plugin | *Version*|
| ------ | ------ |
|  pip   | 22.3.1 |
| Python | 3.11  |
| Django | 4.2.5 |

### Installation

> ##### 1. Clone repository

```bash
git clone https://github.com/dharmendra7/task-management.git
```

> ##### 2. Create virtual environment and activate

```bash
python -m venev yourr-venv-name
```

> ##### 3. Setup The Project

```bash
pip install -r requirements.txt
```


> ##### 4. Setting up your Email Send details in .env

```bash
EMAIL_PORT=email port number
EMAIL_HOST_USER=enter your email 
EMAIL_HOST_PASSWORD=enter email password
EMAIL_HOST=enter host
EMAIL_BACKEND=enter backend config
EMAIL_USE_TLS=True or False
RECIPIENT_ADDRESS=enter recipient email address
```

> ##### 5. Create tables by Django migration

```bash
python manage.py migrate
```


> ##### 6. Following accounts will be available @ `/admin/login`

##### For client use

Email : admin@gmail.com
Password : Test@123

### Setup using docker
- [Docker](https://docs.docker.com/engine/install/)

> #### Setup
Start the dev server for local development:
```bash
docker-compose up -d
```

<br />
