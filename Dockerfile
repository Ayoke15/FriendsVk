FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN python manage.py makemigrations users
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]