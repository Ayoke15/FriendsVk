﻿
# Документация по сервису дружбы на Django

## Обзор

Этот сервис представляет собой простую систему дружбы на Django и Django Rest Framework. Он позволяет пользователям отправлять запросы в друзья, принимать или отклонять эти запросы, просматривать список друзей и состояние запросов.

## Запуск

Для запуска этого сервиса используется контейнер Docker.
1.  Соберите Docker-образ:

`docker build -t friends-django-app .` 

2.  Затем запустите Docker-контейнер:

`docker run -p 8000:8000 friends-django-app` 

После этого приложение должно быть доступно на порту `8000`.

## Запуск тестов

Для запуска тестов выполните скрипт `tests.py` в вашем окружении:

`python tests.py` 

Убедитесь, что у вас установлен Python и все необходимые зависимости (requirements.txt) для выполнения тестов.