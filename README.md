🚀 Dockerized Stock Market Data Pipeline using Dagster

A fully containerized ETL pipeline that fetches, processes, and stores stock market data using
Dagster + Python + PostgreSQL + Docker.

This project demonstrates:

01.Workflow orchestration with Dagster
02.Containerization with Docker & Docker Compose
03.Automated stock data ingestion from an external API
04.Loading cleaned data into PostgreSQL
05.End-to-end ETL pipeline running in containers

📁 Project Structure

dockerized-dagster-stock-pipeline/
│── fetcher/
│   ├── __init__.py
│   └── fetch_and_store.py
│
│── pipelines/
│   ├── __init__.py
│   └── stock_pipeline.py
│
│── sql/
│   └── create_table.sql
│
│── dagster_repository.py
│── workspace.yaml
│── docker-compose.yml
│── Dockerfile
│── requirements.txt
│── .env
│── README.md



📌 Features

✔ Fetches daily stock prices
✔ Parses JSON → Structured rows
✔ Inserts into PostgreSQL
✔ Automated scheduled runs via Dagster Daemon
✔ Full Dockerization for reproducibility
✔ Includes SQL table creation file
✔ Easy to extend for multiple stocks


🔧 Environment Setup

Create .env file
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=stockdb

ALPHAVANTAGE_API_KEY=YOUR_API_KEY_HERE
STOCK_SYMBOL=MSFT


🐳 Run the Project

1️⃣ Start all Docker services
            docker compose up --build
   This starts:
      01.Dagster Webserver
      02.Dagster Daemon
      03.PostgreSQL
    
2️⃣ Open Dagster UI

   👉 http://localhost:3000

   You will see the repository and pipeline listed.

3️⃣ Trigger pipeline run

    In the Dagster UI:
    stock_pipeline → Launch Run

4️⃣ Viewing Data in PostgreSQL
           Open a terminal and run:
           docker exec -it dockerized-dagster-stock-pipeline-postgres-1 bash psql -U postgres -d stockdb

           Query sample:
           SELECT * FROM stock_data LIMIT 20;

🛠 Stopping Services
           docker compose down
        

                         ![alt text](image.png)

📚 Technology Stack

| Component            | Purpose                              |
| -------------------- | ------------------------------------ |
| **Dagster**          | Workflow orchestration & scheduling  |
| **Python**           | Fetching & parsing stock market data |
| **PostgreSQL**       | Persistent storage                   |
| **Docker Compose**   | Multi-service containerization       |
| **AlphaVantage API** | Stock market data source             |


⭐ Future Improvements

Here are enhancements you can add later:
01.Support multiple stock symbols
02.Add logging & monitoring
03.Add Grafana dashboard for stock trends
04.Add Airflow version for comparison
