# 🚀 Dockerized Stock Market Data Pipeline using Dagster

A **fully containerized ETL pipeline** that fetches, processes, and stores stock market data using **Dagster**, **Python**, **PostgreSQL**, and **Docker**.

This project demonstrates:

1. Workflow orchestration with **Dagster**  
2. Containerization using **Docker & Docker Compose**  
3. Automated stock data ingestion from an external API  
4. Data cleaning and insertion into **PostgreSQL**  
5. End-to-end **ETL pipeline** execution in containers  

## ✨ Features

- ✅ Fetches **daily stock prices** from AlphaVantage API  
- ✅ Parses **JSON → Structured rows**  
- ✅ Inserts cleaned data into **PostgreSQL**  
- ✅ Supports **scheduled runs** via Dagster Daemon  
- ✅ Fully **Dockerized** for easy setup & reproducibility  
- ✅ Includes **SQL schema** for automatic table creation  
- ✅ Easily extendable for multiple stock symbols
  

## 📁 Project Structure

```
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
```

## 🔧 Environment Setup

Create a `.env` file in the project root with the following variables:
.env file

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=stockdb

ALPHAVANTAGE_API_KEY=YOUR_API_KEY_HERE
STOCK_SYMBOL=MSFT
```

## 🐳 Run the Project

### 1️⃣ Start All Services

Build and start the containers:

     docker compose up --build

This launches:
- Dagster Webserver  
- Dagster Daemon  
- PostgreSQL Database  

### 2️⃣ Open Dagster UI

Visit the Dagster UI at  

👉 [http://localhost:3000](http://localhost:3000)  

You should see the repository and pipeline listed.

### 3️⃣ Trigger a Pipeline Run

In the Dagster UI:

         stock_pipeline → Launch Run

This will start the ETL process to fetch and store stock data.

### 4️⃣ View Data in PostgreSQL

Open a terminal and connect to the database:

                 docker exec -it dockerized-dagster-stock-pipeline-postgres-1 bash psql -U postgres -d stockdb
                 
Run a sample query:

                SELECT * FROM stock_data LIMIT 20;
                
### 🛠 Stop All Services
To stop and remove containers, run:

               docker compose down
               

## 📚 Technology Stack

| Component | Purpose |
|------------|----------|
| **Dagster** | Workflow orchestration & scheduling |
| **Python** | Fetching & parsing stock data |
| **PostgreSQL** | Persistent data storage |
| **Docker Compose** | Multi-service containerization |
| **AlphaVantage API** | Stock market data source |


## 🌟 Future Improvements

Potential enhancements for later versions:
1. Support for multiple stock symbols  
2. Enhanced logging & monitoring  
3. Grafana dashboard for stock trend visualization  
4. Apache Airflow version for comparison  

![Dagster Pipeline Overview](image.png)

