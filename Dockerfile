FROM python:3.10-slim

# Install curl and ping
RUN apt-get update && apt-get install -y curl iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create DAGSTER_HOME directory
RUN mkdir -p /app/dagster_home
ENV DAGSTER_HOME=/app/dagster_home

COPY . .

EXPOSE 3000

CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
