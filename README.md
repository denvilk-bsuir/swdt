# Testing system

[![Build Docker](https://github.com/denvilk-bsuir/swdt/actions/workflows/build.yml/badge.svg)](https://github.com/denvilk-bsuir/swdt/actions/workflows/build.yml)
[![Codecov](https://github.com/denvilk-bsuir/swdt/actions/workflows/codecov.yml/badge.svg)](https://github.com/denvilk-bsuir/swdt/actions/workflows/codecov.yml)
[![codecov](https://codecov.io/gh/denvilk-bsuir/swdt/graph/badge.svg?token=52BPY3443A)](https://codecov.io/gh/denvilk-bsuir/swdt)

__Контест система__. Система позволяет проверять студентов/учеников/сотрудников на соответствие нужным знаниям в различных направлениях с помощью: открытых/закрытых вопросов, запуска написанного кода на тестах, дописывания кода в существующий модуль.

---

## Table of contents
1. [Requirements](#requirements)
2. [Getting started](#getting-started)
3. [Migrations](#migrations)
4. [Variables](#variables)

---

## Requirements
For running project you need:
- Docker compose

Or you can run project manually. Requirements for manual run:
- Python 3.12
- PostgreSQL
- RabbitMQ
- GNU C++20

Clone repository with command:
```sh
git clone https://github.com/denvilk-bsuir/swdt
```

---

## Getting started
### Common steps:
0.1. Enter directory:
```sh
cd source
```

### Docker
1. Build docker images:
```sh
make build
```
2. Configure env from [Variables](#variables).

2.1. Prepare variables for RabbitMQ (if running rabbitmq locally):
```sh
export UID=$(id -u)
export GID=$(id -g)
```
3. Run project:
```sh
docker-compose -f docker-compose.dev.yaml up
```

### Run manually

1. Create venv:
```sh
python3 -m venv .venv
```
2. Activate venv:
```sh
source .venv/bin/activate
```
3. Install dependencies:
```sh
pip install -r web/requirements.txt
```
4. Configure env from [Variables](#variables).
5. Run web server:
```sh
./web/manage.py runserver
```
6. Run runner:
```sh
./web/manage.py runner
```

---

## Migrations
For apply migrations to database you can use commands:
- Docker
```sh
docker run -d /app/manage.py migrate --env-file .runner.env
```
- Manually
```sh
./web/manage.py migrate
```
__NOTE__: Apply variables for postgres before migration.

## Variables

__.rabbit.env__:
```.env
RABBITMQ_DEFAULT_USER=<rabbit_username>
RABBITMQ_DEFAULT_PASS=<rabbit_password>
```

__.postgres.env__:
```.env
POSTGRES_PASSWORD="<postgres_password>"
PGDATA="/data/postgres"
```

__.runner.env__:
```.env
TESTLIB=/app/testlib.h
PG_HOST=<postgres_host>
PG_PORT=<postgres_port>
PG_PASSWORD=<postgres_password>
RMQ_HOST=<rabbit_host>
RMQ_PASSWORD=<rabbit_password>
RMQ_USER=<rabbit_username>
TEMP_DIR_DELETE=False
```