from python:3.10-alpine

WORKDIR /app

EXPOSE 8000

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]