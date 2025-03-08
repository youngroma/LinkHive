FROM python:3.10-slim

WORKDIR /refhive

COPY requirements.txt /refhive/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /refhive/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
