FROM python:3.10-slim-buster

WORKDIR /app

COPY main.py .
COPY utils /app/utils
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

