FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r req requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["gunicorn","myproject.wsgi:application","--bind","0.0.0.0:8000"]