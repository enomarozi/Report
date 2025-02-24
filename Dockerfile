FROM python:3.11-slim

RUN apt-get update -y && apt-get install nmap -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["gunicorn","app_report.wsgi:application","--bind","0.0.0.0:80","workers","4","--threads","2","--timeout","420"]