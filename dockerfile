FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

# postgresql credentials
ENV DB_HOST: db
ENV DB_PORT: 5432
ENV DB_NAME: mydb
ENV DB_USER: myuser
ENV DB_PASSWORD: mypassword

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
