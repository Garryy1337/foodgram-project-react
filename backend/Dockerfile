FROM python:3.7-slim

WORKDIR /app_back
COPY ../requirements.txt /app_back/
RUN pip3 install -r /app_back/requirements.txt --no-cache-dir
COPY ../ /app_back/
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
