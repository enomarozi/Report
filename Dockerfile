FROM python:3.11-slim

RUN apt-get update -y && apt-get install nmap -y

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["gunicorn","app_report.wsgi:application","--bind","0.0.0.0:80"]