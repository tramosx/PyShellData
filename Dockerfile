FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
COPY between-msgs.sh /app/
COPY max-min-size.sh /app/
COPY order-by-username.sh /app/


RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python", "app.py"]
